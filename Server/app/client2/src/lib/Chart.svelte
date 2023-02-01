<script>
	import { onMount } from 'svelte';
	import Chart from 'chart.js/auto';

	let canvas;

	export let title;
	export let dates;
	export let data;

	onMount(() => {
		new Chart(canvas, {
			type: 'line',
			data: {
				labels: dates.map((str) => {
					const date = new Date(str);
					const formattedDate = date.toLocaleString('default', {
						day: '2-digit',
						month: '2-digit',
						year: '2-digit',
						hour: '2-digit',
						minute: '2-digit',
						second: '2-digit'
					});
					return formattedDate.replace(/\//g, '.');
				}),
				datasets: [
					{
						label: title,
						data: data,
						fill: false,
						borderColor: 'rgb(75, 192, 192)',
						responsive: true,
						scaleFontColor: '#FFFFFF',
						tension: 0.3
					}
				]
			},
			options: {
				grid: {
					color: 'purple'
				},
				scales: {
					x: { ticks: { color: 'purple' } },
					y: { ticks: { color: 'purple' } }
				}
			}
		});
	});
</script>

<div class="chart">
	<canvas bind:this={canvas} />
</div>
