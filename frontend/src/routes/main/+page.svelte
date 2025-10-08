<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

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
			const res = await fetch(`http://127.0.0.1:8000/local-deep?query=${encodeURIComponent(q)}`);
			Lresults = await res.json();
			console.log(Lresults);
			computeGroupedLocal();
		} catch (e) {
			Lresults = { error: 'Failed to fetch results' };
		}
		Lloading = false;
	}

	onMount(() => {
		const urlQuery = $page.url.searchParams.get('query') || '';
		Lquery = urlQuery;
		LqueryValue = urlQuery;
		if (Lquery) fetchLocalResults(Lquery);
	});
</script>

<div class="">
	<div class="w-full p-10">
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
						{groupedLocal.length} folders — showing up to 4 files each
					</div>
					<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
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
