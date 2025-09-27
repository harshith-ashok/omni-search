<script lang="ts">
	import { goto } from '$app/navigation';
	let queryValue = '';

	function search(query: string) {
		goto(`/results?query=${encodeURIComponent(query)}`);
	}
	function gsearch(query: string) {
		goto(`/gresults?query=${encodeURIComponent(query)}&num_results=5`);
	}
</script>

<main>
	<div class="flex h-screen flex-col items-center justify-center">
		<div
			class="text-[6vh] font-black tracking-wide uppercase transition-all hover:scale-105"
			style="font-family: LT Avocado"
		>
			<a href="/">Omni Search</a>
		</div>
		<div>
			<ul class="flex gap-4 pb-5 tracking-wide uppercase">
				<li class="rounded-md p-1 transition-all duration-230 hover:bg-black hover:text-white">
					<a href="/profile">Profile</a>
				</li>
				<li class="rounded-md p-1 transition-all duration-230 hover:bg-black hover:text-white">
					<a href="/settings">Settings</a>
				</li>
			</ul>
		</div>
		<div class="flex gap-0">
			<input
				type="text"
				bind:value={queryValue}
				autofocus
				class="input w-128 rounded-l-full border-1 p-4 pl-10"
			/>
			<button
				class="cursor-pointer border-y-1 p-4 px-4 text-black transition-all hover:border-black hover:bg-black hover:text-white"
				style="font-family: LT Avocado"
				type="button"
				aria-label="google"
				on:click={() => gsearch(queryValue)}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="16"
					height="16"
					fill="currentColor"
					class="bi bi-google"
					viewBox="0 0 16 16"
				>
					<path
						d="M15.545 6.558a9.4 9.4 0 0 1 .139 1.626c0 2.434-.87 4.492-2.384 5.885h.002C11.978 15.292 10.158 16 8 16A8 8 0 1 1 8 0a7.7 7.7 0 0 1 5.352 2.082l-2.284 2.284A4.35 4.35 0 0 0 8 3.166c-2.087 0-3.86 1.408-4.492 3.304a4.8 4.8 0 0 0 0 3.063h.003c.635 1.893 2.405 3.301 4.492 3.301 1.078 0 2.004-.276 2.722-.764h-.003a3.7 3.7 0 0 0 1.599-2.431H8v-3.08z"
					/>
				</svg>
			</button>
			<button
				class="cursor-pointer rounded-r-full bg-black p-4 px-10 text-white transition-all hover:bg-gray-900"
				style="font-family: LT Avocado"
				type="button"
				on:click={() => search(queryValue)}
			>
				SEARCH
			</button>
		</div>
	</div>
</main>
