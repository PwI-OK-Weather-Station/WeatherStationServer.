<script>
    import { onMount } from "svelte";

    export let menu = 0
    onMount(() => (menu))
</script>

<header class="text-gray-400 bg-gray-900 body-font navbar">
    <div class="container mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center">
        <!-- svelte-ignore a11y-missing-attribute -->
      <a class="flex title-font font-medium items-center text-white mb-4 md:mb-0" class:text-white={menu==0} on:click|preventDefault={() => (menu = 0)}>
        <span class="ml-3 text-xl">Weather Server</span>
      </a>
      <nav class="md:ml-auto flex flex-wrap items-center text-base justify-center" >
        <!-- svelte-ignore a11y-missing-attribute -->
        <a class="mr-5 hover:text-gray-200 active:text-white" class:text-white={menu==1} on:click|preventDefault={() => (menu = 1)}>Sensory</a>
        <!-- svelte-ignore a11y-missing-attribute -->
        <a class="mr-5 hover:text-gray-200 active:text-white" class:text-white={menu==4} on:click|preventDefault={() => (menu = 4)}>Login</a>
        
      </nav>
    </div>
    <hr/>
  </header>
  <style>
    .active{
      background-color: white;
    }
    </style>