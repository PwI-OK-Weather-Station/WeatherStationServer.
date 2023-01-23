<script>
    import { onMount } from "svelte";

    export let menu = 0
    onMount(() => (menu))
</script>

<header class="text-gray-400 bg-gray-900 body-font navbar">
    <div class="container mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center">
        <!-- svelte-ignore a11y-missing-attribute -->
      <a class="flex title-font font-medium items-center text-white mb-4 md:mb-0" on:click|preventDefault={() => (menu = 0)}>
        <span class="ml-3 text-xl">Weather Server</span>
      </a>
      <nav class="md:ml-auto flex flex-wrap items-center text-base justify-center" >
        <!-- svelte-ignore a11y-missing-attribute -->
        <a class="mr-5 hover:text-gray-200 active:text-white" on:click|preventDefault={() => (menu = 1)}>Sensory</a>
        <!-- svelte-ignore a11y-missing-attribute -->
        <a class="mr-5 hover:text-gray-200 active:text-white" on:click|preventDefault={() => (menu = 2)}>Login</a>
        <!-- svelte-ignore a11y-missing-attribute -->
        <a class="mr-5 hover:text-gray-200 active:text-white" on:click|preventDefault={() => (menu = 3)}>Third Link</a>
        <!-- svelte-ignore a11y-missing-attribute -->
        <a class="mr-5 hover:text-gray-200 active:text-white" on:click|preventDefault={() => (menu = 4)}>Fourth Link</a>
      </nav>
    </div>
    <hr/>
  </header>