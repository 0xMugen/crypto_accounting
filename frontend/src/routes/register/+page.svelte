<script>
  import { goto } from '$app/navigation';
  import { writable } from 'svelte/store';

  let first_name = '';
  let last_name = '';
  let username = '';
  let email = '';
  let password = '';
  let password2 = '';
  let passwordValid = false;
  let passwordMismatch = false;
  let passwordSimple = false;
  let isLoading = writable(false); 
  let isError = writable(false);
  let errorMessage = writable(''); 


 $: {
    // const hasLowercase = /[a-z]/.test(password);
    // const hasUppercase = /[A-Z]/.test(password);
    const hasNumber = /\d/.test(password);
    // const hasSpecialChar = /[!@#\$%\^&\*]/.test(password);
    const hasValidLength = password.length >= 8;

    passwordValid =  hasNumber && hasValidLength;
    passwordSimple = !passwordValid; // Indicates that the password is too simple
  }


  const checkPasswords = () => {
    if (password !== password2) {
      passwordMismatch = true;
    } else {
      passwordMismatch = false;
    }
  }



  async function register() {
    isLoading.set(true);
    if (!passwordValid) {
      isLoading.set(false);
      isError.set(true);
      errorMessage.set('Password is too simple');
      return;
    }
    if (passwordMismatch) {
      isLoading.set(false);
      isError.set(true);
      errorMessage.set('Passwords do not match');
      return;
    }
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, first_name, last_name, email, password, password2 })
    });

    if (!res.ok) {
      const errorData = await res.json();  // Parse response body as JSON

      // Django often sends errors in a dictionary-like structure.
      // It could be a simple key-value pair like {"detail": "Error details"} 
      // or more complex dictionary like {"field": ["Error 1", "Error 2"]}.
      // Adjust the below code based on the error structure returned by your Django server

      const errorMessages = Object.values(errorData).join(', ');  // Convert error details into string

      isLoading.set(false);
      isError.set(true);
      errorMessage.set(errorMessages);  // Set error message from Django
      return;
    } else {
      isLoading.set(false);
      isError.set(false);
      goto('/login');
    }
  }


  function closeErrorModal() {
        isError.set(false);
    }

</script>

<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company">
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight">Create an account</h2>
    </div>
  
    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-6">

        <div class="flex flex-wrap -mx-3 mb-6">

            <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
              <label for="first_name" class="block text-sm font-medium leading-6">First Name</label>
                <div class="mt-2">
                    <input bind:value={first_name} id="first_name" name="first_name" type="text" autocomplete="name" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 bg-white px-1">
                </div>
            </div>
            
            <div class="w-full md:w-1/2 px-3">
                <label for="last_name" class="block text-sm font-medium leading-6">Last Name</label>
                <div class="mt-2">
                    <input bind:value={last_name} id="last_name" name="last_name" type="text" autocomplete="last_name" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 bg-white px-1">
                </div>
            </div>

        </div>


        <div>
          <label for="email" class="block text-sm font-medium leading-6">Email address</label>
          <div class="mt-2">
            <input bind:value={email} id="email" name="email" type="email" autocomplete="email" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 bg-white px-1">
          </div>
        </div>

        <div>
            <label for="username" class="block text-sm font-medium leading-6">Username</label>
            <div class="mt-2">
                <input bind:value={username} id="username" name="username" type="username" autocomplete="username" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 bg-white px-1">
            </div>
        </div>
  
        <div>
          <div class="flex items-center justify-between">
            <label for="password" class="block text-sm font-medium leading-6">Password</label>
          </div>
          <div class="mt-2 relative">
            <input on:keyup={checkPasswords} bind:value={password} id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 bg-white px-1">
            {#if passwordSimple}
              <div class="absolute top-full mt-1 text-red-600 text-sm animate-pulse">Should contain a number and be at least 8 characters.</div>
            {/if}
          </div>
        </div>


        <div>
          <div class="flex items-center justify-between">
            <label for="password2" class="block text-sm font-medium leading-6">Password confirmation</label>
          </div>
          <div class="mt-2 relative">
            <input on:keyup={checkPasswords} bind:value={password2} id="password2" name="password2" type="password" autocomplete="new-password" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 bg-white px-1">
            {#if passwordMismatch}
              <div class="absolute top-full mt-1 text-red-600 text-sm animate-pulse">Passwords do not match.</div>
            {/if}
          </div>
        </div>


        <div>
          <button type="submit" on:click={register} class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Register</button>
        </div>
      </form>
  
      <p class="mt-10 text-center text-sm text-gray-500">
        Already have an account?
        <a href="/login" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Login</a>
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
          <p>{$errorMessage}</p>
          <button class="btn" on:click={closeErrorModal}>Close</button>
      </div>
  </div>
{/if}