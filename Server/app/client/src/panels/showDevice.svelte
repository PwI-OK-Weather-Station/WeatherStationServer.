<script>
    import { dataset_dev } from 'svelte/internal';
    import {fetchGET} from '../utils'
    import Loader from './loader.svelte'
    import { dataset } from './data.js';
    import Graph from './graph.svelte'
    import { Line } from 'svelte-chartjs'
    export let id;
    let dataGet = {}
    async function getMeasurements() {
        let results = await fetchGET(`/api/device/${id}/10`, {});
        console.log(results);
        results = results['measurements']
        dataGet = results;
        console.log(results);
        return results;
    }
    let awaitMeasurements = getMeasurements();
    export let selectedDevice;
    
</script>
{#await awaitMeasurements}
<p><Loader /> Pobieram dane</p>
{:then measurement}
<div class="md:w-full  max-h-max text-sm font-medium overflow-auto text-gray-900 bg-white border border-gray-200 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
    {#if measurement.length == 0 }
    <a class="align-middle" >
        <h1 class="text-center align-middle">Brak danych</h1>
    </a>
    {:else}
        
        <Graph dataGet={measurement}/>

        {#each measurement as {create_time, temperature, pressure, humidity}}
        <a class="block w-full px-4 py-2 border-b border-gray-200 cursor-default">
        {create_time} <br/> {temperature}°C<br/>{humidity}% <br/> {pressure}hPa
        </a>
        {/each}
    {/if}
    </div>
{:catch error}
    Coś poszło nie tak <br/>
    {error}
{/await}