<script>
	import { goto } from '$app/navigation';

	import api from '$lib/api';
	import { user } from '$lib/stores';

	export let show;

	let nameSensor;
	let publicSensor = false;
    let indoor = true;

	const login = async () => {
		try {
			let x = await api.post('/device', { name: nameSensor, public: publicSensor, indoor: indoor });
			goto('/sensors');
		} catch (error) {
			console.log(error);
			alert('Failed to add sensor');
		}
	};

	const hide = () => (show = false);
	
</script>

<div class="wrapper">
	<div class="login">
		<h1>Add new device</h1>
		<form on:submit|preventDefault={login}>
			<input type="text" bind:value={nameSensor} placeholder="Device name" />
            <ul>
                <li class:active={publicSensor} on:click={() => {publicSensor = !publicSensor}}>
                    <p class={publicSensor?"colored":""}>
                    { publicSensor? "Public": "Private" }
                    </p>
                </li>
                <li class:active={indoor} on:click={() => {indoor = !indoor; console.log(indoor)}}>
                    <p class={indoor?"colored":""}>
                        {indoor? "Indoor": "Outdoor"}
                    </p>
                </li>
            </ul>
			<button type="submit">Add device</button>
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

    ul {
		gap: 0.5rem;
	}
	li {
		cursor: pointer;
		border: 2px solid #eaeaea;
		padding: 1rem;
		min-width: 200px;
	}
	li:hover {
		border: 2px solid rgba(0, 0, 0, 0.25);
	}
	li.active {
		border: 2px solid var(--c-main);
	}
    .wrapper .colored {
		color: var(--c-main);
		font-weight: bold;
	}
</style>


