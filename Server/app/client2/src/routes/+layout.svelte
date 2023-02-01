<script>
	import '$lib/global.css';
	import { goto } from '$app/navigation';

	import api from '$lib/api';
	import { user } from '$lib/stores';

	const logout = async () => {
		try {
			await api.post('/logout');
			$user = null;
			goto('/');
		} catch (err) {
			console.log(err);
			alert('Logout failed');
		}
	};

	const auth = async () => {
		try {
			$user = await api.get('/auth');
		} catch (err) {
			logout();
		}
	};
	if(document.cookie.match(/^(.*;)?\s*token\s*=\s*[^;]+(.*)?$/)){
		auth();
	}
</script>

<nav>
	<div>
		<a href="/" class="home">WeatherStation</a>
		<a href="/sensors">Sensors</a>
		{#if $user}
			<a href="/addDevice" class="admin">Add device</a>
		{/if}
	</div>

	<div>
		{#if $user}
			<span>{$user.name}</span>
			<button on:click={logout}>Logout</button>
		{:else}
			<a href="/login">Login</a>
		{/if}
	</div>
</nav>

<main>
	<slot />
</main>

<style>
	nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		background-color: var(--c-main-light);
	}
	nav div {
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}
	.home {
		font-size: 1.25rem;
		font-weight: bold;
	}
	.admin {
		color: var(--c-main);
	}

	main {
		padding: 1rem;
	}
</style>
