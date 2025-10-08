<script lang="ts">
	import { query } from '$app/server';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	let AIqueryValue = '';
	let AIquery = '';
	let AIresults: any = null;
	let AIloading = false;

	async function fetchResults(q: string) {
		AIloading = true;
		try {
			const res = await fetch('http://127.0.0.1:5000/chat', {
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
			console.log(AIresults);
		} catch (e) {
			AIresults = { error: 'Failed to fetch results' };
		}
		AIloading = false;
	}

	onMount(() => {
		const urlQuery = $page.url.searchParams.get('query') || '';
		AIquery = urlQuery;
		AIqueryValue = urlQuery;
		if (AIquery) fetchResults(AIquery);
	});

	// function search(q: string) {
	// 	goto(`/results?query=${encodeURIComponent(q)}`);
	// 	// fetchResults will be triggered by onMount after navigation
	// }
</script>

<main>
	<div class="flex gap-10 p-10">
		<div
			class="flex-1 text-[3vh] font-black tracking-wide uppercase transition-all hover:scale-105"
			style="font-family: LT Avocado"
		>
			<a href="/">Omni Search</a>
		</div>

		<div class="flex flex-6 gap-0">
			<input
				type="text"
				bind:value={AIqueryValue}
				placeholder="Search"
				class="input w-full rounded-l-full border-1 p-4 pl-10"
			/>
			<button
				class="cursor-pointer rounded-r-full bg-black p-4 px-10 text-white hover:bg-gray-900"
				style="font-family: LT Avocado"
				type="button"
				on:click={() => fetchResults(AIqueryValue)}
			>
				SEARCH
			</button>
		</div>
	</div>
	<div class="w-[75%]">
		{#if AIloading}
			<div class="mt-10 text-lg">Loading...</div>
		{:else if AIresults}
			<div class="mt-10 flex flex-col gap-6 p-10">
				{#if AIresults.error}
					<div class="text-red-600">{AIresults.error}</div>
				{:else if AIresults.results}
					{#each AIresults.results as result}
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
						<pre>{JSON.stringify(AIresults, null, 2)}</pre>
					</div>
				{/if}
			</div>
		{/if}
	</div>
</main>
