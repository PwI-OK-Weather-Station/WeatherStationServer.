<script>
	import Sensor from './Sensor.svelte';

	export let data;

	let index = 0;
	$: sensor = data.sensors[index];
	let config;


	
</script>

{#if sensor}
	<h1>Sensors</h1>
	<div class="wrapper">
		<ul class="sensors">
			{#each data.sensors as s, i}
				<li class="sensor" class:active={i == index} on:click={() => (index = i)}>
					<b>{s.device_id}</b>
					{s.device_name}
				</li>
			{/each}
		</ul>
		<Sensor {sensor} {config} />
	</div>
{/if}

<style>
	.wrapper {
		display: flex;
	}

	ul {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	li {
		cursor: pointer;
		border: 2px solid #fff;
		padding: 1rem;
		min-width: 200px;
	}
	li:hover {
		border: 2px solid rgba(0, 0, 0, 0.25);
	}
	li.active {
		border: 2px solid #000;
	}
</style>
