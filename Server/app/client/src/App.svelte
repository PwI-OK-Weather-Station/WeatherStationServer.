<script>
	import Navbar from './panels/navbar.svelte'
	import Login from './panels/login.svelte'
	import Devices from './panels/devices.svelte'
	let name;
	let menu
</script>

<Navbar bind:menu={menu}/>
<main>
	{#if menu == 0}
		<h1>Hello {menu}!</h1>
		<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
	{:else if menu == 1}
			<Devices />
	{:else if menu == 4}
		<Login />
	{/if}
</main>
	

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>