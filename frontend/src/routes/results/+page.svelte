<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let queryValue = '';
	let query = '';
	let results: any = null;
	let loading = false;

	async function fetchResults(q: string) {
		loading = true;
		try {
			const res = await fetch(`http://127.0.0.1:8000/search?query=${encodeURIComponent(q)}`);
			results = await res.json();
			console.log(results);

			// If the primary search returns no results, fall back to gquery endpoint
			const noResults =
				!results ||
				(Array.isArray(results.results) && results.results.length === 0) ||
				(Array.isArray(results) && results.length === 0);
			if (noResults) {
				console.log('No results from /search, falling back to /gquery');
				await fetchGQuery(q);
			}
		} catch (e) {
			results = { error: 'Failed to fetch results' };
		}
		loading = false;
	}

	async function fetchGQuery(q: string) {
		// separate loading flag not needed; reuse loading for main results
		try {
			const res = await fetch(`http://127.0.0.1:8000/gquery?query=${encodeURIComponent(q)}`);
			const gres = await res.json();
			console.log('gquery results', gres);
			// set results to the fallback results
			results = gres;
		} catch (e) {
			// if fallback fails, keep previous results or set error
			results = { error: 'Failed to fetch fallback results' };
		}
	}

	let LqueryValue = '';
	let Lquery = '';
	let Lresults: any = null;
	let Lloading = false;

	// groupedLocal will be derived from Lresults.results when available
	let groupedLocal: {
		key: string;
		files: { folder: string; subfolder: string; file: string }[];
	}[] = [];

	function computeGroupedLocal() {
		groupedLocal = [];
		if (!Lresults) return;
		const entries = Array.isArray(Lresults)
			? Lresults
			: Array.isArray(Lresults.results)
				? Lresults.results
				: [];
		if (!entries.length) return;
		const map: Map<string, { folder: string; subfolder: string; file: string }[]> = new Map();
		// entries is an array of objects like { folder, subfolder, file }
		for (const item of entries) {
			// Prefer grouping by subfolder if present, otherwise by folder
			const key = item.subfolder && item.subfolder.length ? item.subfolder : item.folder || 'root';
			if (!map.has(key)) map.set(key, []);
			map.get(key)!.push({ folder: item.folder, subfolder: item.subfolder, file: item.file });
		}
		for (const [key, files] of map.entries()) {
			groupedLocal.push({ key, files: files.slice(0, 4) });
		}
	}

	async function fetchLocalResults(q: string) {
		Lloading = true;
		try {
			const res = await fetch(`http://127.0.0.1:8000/local?query=${encodeURIComponent(q)}`);
			Lresults = await res.json();
			console.log(Lresults);
			computeGroupedLocal();
		} catch (e) {
			Lresults = { error: 'Failed to fetch results' };
		}
		Lloading = false;
	}

	let AIqueryValue = '';
	let AIquery = '';
	let AIresults: any = null;
	let AIloading = false;

	async function fetchAIResults(q: string) {
		AIloading = true;
		try {
			const res = await fetch('http://127.0.0.1:8000/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					session_id: 'user123',
					message: `${q}`
				})
			});
			AIresults = await res.json();
			console.log(AIresults['reply']);
		} catch (e) {
			AIresults = { error: 'Failed to fetch results' };
		}
		AIloading = false;
	}

	onMount(() => {
		const urlQuery = $page.url.searchParams.get('query') || '';
		query = urlQuery;
		queryValue = urlQuery;
		if (query) fetchResults(query);

		AIquery = urlQuery;
		AIqueryValue = urlQuery;
		if (AIquery) fetchAIResults(AIquery);

		Lquery = urlQuery;
		LqueryValue = urlQuery;
		if (Lquery) fetchLocalResults(Lquery);
	});

	function search(q: string) {
		goto(`/results?query=${encodeURIComponent(q)}`);
		// fetchResults will be triggered by onMount after navigation
	}
</script>

<main>
	<div class="flex flex-col gap-10 p-10 md:flex-row">
		<div
			class=" flex-1 text-[1vh] font-black tracking-wide uppercase transition-all hover:scale-105 md:text-[3vh]"
			style="font-family: LT Avocado"
		>
			<a href="/">Omni Search</a>
		</div>

		<div class="flex flex-6 gap-0">
			<input
				type="text"
				bind:value={queryValue}
				placeholder="Search"
				class="input w-full rounded-l-full border-1 p-4 pl-10"
			/>
			<button
				class="cursor-pointer rounded-r-full bg-black p-4 px-10 text-white hover:bg-gray-900"
				style="font-family: LT Avocado"
				type="button"
				on:click={() => {
					search(queryValue);
				}}
			>
				SEARCH
			</button>
		</div>
	</div>
	<div>
		<div class="flex flex-col">
			<div class="grid grid-cols-1 gap-10 px-10 md:grid-cols-2">
				<div class="flex w-full items-center rounded-xl border-1 p-10">
					<div class="w-[75%]">
						{#if AIloading}
							<div class="mt-10 text-lg">Loading...</div>
						{:else if AIresults}
							<div class="py-2 text-xl font-bold">AI Summary</div>
							{AIresults['reply']}
						{/if}
					</div>
				</div>
				<div class="w-full rounded-xl border-1 p-10">
					{#if Lloading}
						<div class="mt-4 text-lg">Loading local results...</div>
					{:else if Lresults}
						{#if Lresults.error}
							<div class="text-red-600">{Lresults.error}</div>
						{:else if Lresults.results && Lresults.results.length}
							<!-- groupedLocal is computed in the script -->
							<div class="py-2 text-xl font-bold">Local File Search</div>
							<div>
								<div class="mb-3 text-sm text-gray-500">
									{groupedLocal.length} folders — showing up to 3 files each
								</div>
								<div class="pt-1 pb-2 font-bold text-gray-600 uppercase">
									<a href="/main?query={queryValue}">Go Deeper</a>
								</div>
								<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
									{#each groupedLocal as group}
										<div class="rounded-md border bg-white p-4">
											<div class="mb-2 truncate text-sm font-semibold text-gray-600">
												{group.key}
											</div>
											<ul class="space-y-2 text-sm">
												{#each group.files as file}
													<li class="flex items-center justify-between">
														<div class="truncate">{file.file}</div>
														<div class="ml-4 text-xs text-gray-500">
															{file.subfolder ? file.subfolder.split('/').pop() : file.folder}
														</div>
													</li>
												{/each}
											</ul>
										</div>
									{/each}
								</div>
							</div>
						{:else}
							<div class="text-gray-600">No local results found</div>
						{/if}
					{/if}
				</div>
			</div>
			<div class="m-10 rounded-xl border-1 p-10">
				<div class="w-[75%]">
					{#if loading}
						<div class="mt-10 text-lg">Loading...</div>
					{:else if results}
						<div class="flex flex-col gap-4">
							{#if results.error}
								<div class="text-red-600">{results.error}</div>
							{:else if results.results}
								{#each results.results as result}
									<div class=" flex flex-col bg-white p-6">
										<a class="mb-2 text-2xl font-bold" href={result.url}>
											{result.title}
										</a>
										<a class="link text-md mb-2 text-gray-500 underline" href={result.url}>
											{result.url}
										</a>
										<div class="pt-2 text-gray-900">
											{result.snippet}
										</div>
									</div>
								{/each}
							{:else}
								<div class="rounded-lg border bg-white p-6 shadow">
									<pre>{JSON.stringify(results, null, 2)}</pre>
								</div>
							{/if}
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
</main>
