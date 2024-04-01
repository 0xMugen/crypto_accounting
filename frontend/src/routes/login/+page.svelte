<script>
  import { goto } from '$app/navigation';
  import { writable } from 'svelte/store';

  let username = '';
  let password = '';
  let isLoading = writable(false); 
  let isError = writable(false);
  let errorMessage = writable(''); 

  async function login(event) {
    event.preventDefault();
    isLoading.set(true);
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!res.ok) {
          isLoading.set(false);
          isError.set(true);
          return;
        }

        const data = await res.json();

        if (data) {
          isLoading.set(false);
          console.log(data.access);
          localStorage.setItem('username', data.username);
          localStorage.setItem('token', data.access);

          location.href = "/";
        } else {
          isError.set(true);
        }
  }

    function closeErrorModal() {
        isError.set(false);
    }

</script>

<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company">
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight">Sign in to your account</h2>
    </div>
  
    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-6" action="#" method="POST">
        <div>
          <label for="email" class="block text-sm font-medium leading-6">Email address or Username</label>
          <div class="mt-2">
            <input bind:value={username} id="email" name="email" type="email" autocomplete="email" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 bg-white px-1">
          </div>
        </div>
  
        <div>
          <div class="flex items-center justify-between">
            <label for="password" class="block text-sm font-medium leading-6">Password</label>
            <div class="text-sm">
              <a href="/reset-password" class="font-semibold text-indigo-600 hover:text-indigo-500">Forgot password?</a>
            </div>
          </div>
          <div class="mt-2">
            <input  bind:value={password} id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 bg-white px-1">
          </div>
        </div>
  
        <div>
          <button on:click={login} type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign in</button>
        </div>
      </form>
  
      <p class="mt-10 text-center text-sm text-gray-500">
        Not a member?
        <a href="/register" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Register</a>
      </p>
    </div>
  </div>

  {#if $isLoading}
        <div class="absolute inset-0 flex items-center justify-center z-10">
            <span class="loading loading-spinner loading-lg"></span>
        </div>
    {/if}

    <!-- Error modal -->
    {#if $isError}
        <div class="absolute inset-0 flex items-center justify-center z-10">
            <div class="p-4 bg-slate-500 rounded shadow-md">
                <h2 class="text-xl font-bold">Error</h2>
                <p>Username or password is incorrect</p>
                <button class="btn" on:click={closeErrorModal}>Close</button>
            </div>
        </div>
    {/if}

