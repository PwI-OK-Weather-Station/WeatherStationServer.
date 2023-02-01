<script>
	import api from '$lib/api';
	import { user } from '$lib/stores';
	import Chart from '$lib/Chart.svelte';

	export let sensor;
	export let config;
	$: permissions = !!config && config.owner_id == $user.uid;

	let count = 10;
	let measurements = [];
	let mType = 'humidity';
	$: mLast = measurements[measurements.length - 1];
	
	async function fetchMeasurements(sensor) {
		const data = await api.get(`/device/${sensor.device_id}/${count}`);
		measurements = data.measurements;
	}
	async function fetchConfig(sensor) {		
		try{
			const data = await api.get(`/device/${sensor.device_id}/config`);
			if(!data.hasOwnProperty('Error')){
				config = data;
			}
			else{
				config = null;
			}
		}
		catch (err){
			config = null;
		}	
	}
	$: fetchMeasurements(sensor);
	$: fetchConfig(sensor)
	
	async function toggleIndoor() {
		const data = await api.post(`/device/${sensor.device_id}/config`, {
			indoor: !sensor.indoor
		});
		sensor.indoor = data.indoor;
	}
	async function togglePublic() {
		const data = await api.post(`/device/${sensor.device_id}/config`, {
			is_public: !sensor.is_public
		});
		sensor.is_public = data.is_public;
	}
</script>

<div class="wrapper">
	<div class="title">
		<h2>{sensor.device_name} <span class="id">id: {sensor.device_id}</span></h2>
		{#if permissions}
			<b>Token</b>: {config.token}
		{/if}
	</div>

	<div class="info">
		<p><b>Owner</b>: {sensor.owner_name} <span class="id">id: {sensor.owner_id}</span></p>
		{#if sensor.indoor}
			<p class="colored">
				INDOOR
			</p>
		{:else}
			<p>OUTDOOR</p>
		{/if}
		{#if permissions}<button on:click={toggleIndoor}>Toggle</button>{/if}
		{#if sensor.is_public}
			<p class="colored">
				PUBLIC
			</p>
		{:else}
			<p>PRIVATE</p>
		{/if}
			
		{#if permissions}<button on:click={togglePublic}>Toggle</button>{/if}
	</div>

	<div class="chart-wrapper">
		{#if measurements.length == 0}
			<p>No measurements yet</p>
		{:else}
			<ul>
				<li class:active={mType == 'humidity'} on:click={() => (mType = 'humidity')}>
					Humidity {Number(mLast?.humidity).toFixed(2)}
				</li>
				<li class:active={mType == 'pressure'} on:click={() => (mType = 'pressure')}>
					Pressure {Number(mLast?.pressure).toFixed(2)}
				</li>
				<li class:active={mType == 'temperature'} on:click={() => (mType = 'temperature')}>
					Temperature {Number(mLast?.temperature).toFixed(2)}
				</li>
			</ul>
			<div class="chart">
				{#key { mType, measurements }}
					<Chart
						title={mType[0].toUpperCase() + mType.slice(1)}
						dates={measurements.map((m) => m.create_time)}
						data={measurements.map((m) => m[mType])}
					/>
				{/key}
			</div>
		{/if}
	</div>
</div>

<style>
	.wrapper {
		padding: 2rem;
		flex: 1;
		max-width: 120ch;
		background-color: rgb(240, 242, 245);
	}
	.wrapper span.id {
		font-size: 0.8rem;
		margin-left: 0.25rem;
		color: #666;
	}

	.wrapper .colored {
		color: var(--c-main);
		font-weight: bold;
	}

	.title {
		display: flex;
		align-items: flex-end;
		gap: 1rem;
		margin-bottom: 1rem;
	}
	h2 {
		margin: 0;
	}

	.info {
		display: flex;
		gap: 1rem;
	}

	.chart-wrapper {
		margin-top: 2rem;
	}
	ul {
		display: flex;
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
	.chart {
		flex: 1;
	}
</style>
