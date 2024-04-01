<script>
    let email = '';
  
    async function handleRecovery() {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/password-reset/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });

        if (!res.ok) {
          console.log(res);
        }
    }
  </script>
  
  <div class="min-h-scree flex justify-center items-center ">
    <div class="bg-white p-8 rounded-xl shadow-md w-96">
      <h1 class="text-2xl font-bold mb-4">Password Recovery</h1>
      <p class="text-gray-600 mb-4">Enter your email address to receive password reset instructions.</p>
      <form on:submit|preventDefault={handleRecovery}>
        <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-600">Email</label>
          <input type="email" id="email" bind:value={email} required class="w-full p-2 border rounded mt-1" />
        </div>
        <div>
          <button type="submit" class="btn btn-primary w-full">Send Recovery Email</button>
        </div>
      </form>
    </div>
  </div>
  
  <style>
    /* You can add additional styles here */
  </style>
  