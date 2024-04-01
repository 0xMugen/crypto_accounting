<script>
    import { goto } from '$app/navigation'
    import { onMount } from 'svelte';
    let username;
    let loggedIn = false;
    if (typeof window !== "undefined") {
        //check for username in local storage
        username = localStorage.getItem("username");
        loggedIn = username ? true : false;
    }

    function login () {
        goto('/login')
    }

    onMount(() => {
        if (loggedIn) {
            goto('/dashboard')
        }
    })
</script>


{#if !loggedIn}
<div class="hero min-h-screen bg-base-200">
    <div class="hero-content text-center">
      <div class="max-w-md">
        <h1 class="text-5xl font-bold">Hello there</h1>
        <p class="py-6">Welcome to the Crypto accounting ledger, the cutting-edge platform designed to simplify your crypto accounting needs.</p>
        <button class="btn btn-primary" on:click={login}>Get Started</button>
      </div>
    </div>
  </div>
{/if}
