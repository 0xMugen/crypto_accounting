<script context="module">
    export async function load({ params }) {
      return {
        props: {
          uid: params.uid,
          token: params.token,
        },
      };
    }
  </script>
  
  <script>
    export let uid, token;
    let password = '';
    let message = '';
  
    async function resetPassword() {
      const response = await fetch(`/reset/${uid}/${token}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });
      message = await response.json().then(data => data.message);
    }
  </script>
  
  <input bind:value={password} type="password" placeholder="Enter new password" />
  <button on:click={resetPassword}>Reset Password</button>
  <p>{message}</p>
  