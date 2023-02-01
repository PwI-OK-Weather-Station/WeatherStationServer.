<script>
	import { goto } from '$app/navigation';

	import api from '$lib/api';
	import { user } from '$lib/stores';

	export let show;

	let email;
	let password;

	const login = async () => {
		try {
			$user = await api.post('/login', { email, password });
			goto('/');
		} catch (error) {
			console.log(error);
			alert('Login failed');
		}
	};

	const hide = () => (show = false);
	
</script>

<div class="wrapper">
	<div class="login">
		<h1>Login</h1>
		<form on:submit|preventDefault={login}>
			<input type="email" bind:value={email} placeholder="email" />
			<input type="password" bind:value={password} placeholder="password" />
			<button type="submit">Login</button>
		</form>
	</div>
</div>

<style>
	.wrapper {
		display: flex;
		justify-content: center;
		width: 100%;
	}
	.login {
		width: 300px;
		border: 2px solid #000;
		padding: 2rem;
	}

	.login h1 {
		text-align: center;
	}

	.login input {
		display: block;
		width: 100%;
		margin-bottom: 10px;
		padding: 10px;
	}

	.login button {
		width: 100%;
		padding: 10px;
	}
</style>
