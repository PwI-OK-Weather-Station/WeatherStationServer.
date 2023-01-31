<script>
    import ShowDevice from './showDevice.svelte'
    import {fetchGET} from '../utils'
    import Loader from './loader.svelte'
    async function getDevices() {
    let devices = await fetchGET('/api/devices', {});
    console.log(devices);
    devices = devices['devices']
    console.log(devices);
    return devices;
  }
  let awaitDevices = getDevices();
  let selectedDevice =-1;
  let toggle = false;
  function select(x){
    toggle = false;
    selectedDevice = x;
    toggle = true;

  }
</script>
<div class = "h-4/5 md:flex">
{#await awaitDevices}
<p><Loader /> Pobieram dane</p>
    {:then devices}

        <div class="md:w-1/6 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
            {#each devices as {device_id, device_name}}
            <a class="block w-full px-4 py-2 border-b border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-700
            focus:text-blue-700 dark:border-gray-600 dark:hover:bg-gray-600 dark:hover:text-white dark:focus:ring-gray-500 dark:focus:text-white"
            on:click={()=>select(device_id)}>
            {device_id}: {device_name}
        </a>
        {/each}
    </div>
    {:catch error}
    Coś poszło nie tak <br/>
    {error}
    {/await}
    {#key selectedDevice}
      {#if selectedDevice>=0}
        <ShowDevice id = {selectedDevice} />
      {/if}
    {/key}
</div>