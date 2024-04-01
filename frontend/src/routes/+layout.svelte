<script>
  import "../app.css";

  let username;
  let loggedIn = false;
  if (typeof window !== "undefined") {
      //check for username in local storage
      username = localStorage.getItem("username");
      loggedIn = username ? true : false;
  }

  async function logout() {
      if (typeof window !== "undefined") {
          localStorage.removeItem("username");
          localStorage.removeItem("token");
          location.href = "/login";
      }
  }
</script>

<div class="navbar bg-base-100 bg-black">
  <div class="navbar-start">
    <div class="dropdown">
      <label tabindex="0" class="btn btn-ghost lg:hidden">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" /></svg>
      </label>
      
      <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
        {#if loggedIn}
          <li><a href="/dashboard">Dashboard</a></li>
        {/if}
        <li>
          <a>Parent</a>
          <ul class="p-2">
            <li><a>Submenu 1</a></li>
            <li><a>Submenu 2</a></li>
          </ul>
        </li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </div>
    <a class="btn btn-ghost px-10 normal-case text-4xl" href="/">Crypto ledger</a>

    <ul class="menu menu-horizontal px-1">
      {#if loggedIn}
        <li><a class="px-4 mt-4 text-lg" href="/dashboard">Dashboard</a></li>
      {/if}
      <li tabindex="0">
        <details>
          <summary class="px-4 mt-4 text-lg">Parent</summary>
          <ul class="p-4">
            <li><a class="text-lg">Submenu 1</a></li>
            <li><a class="text-lg">Submenu 2</a></li>
          </ul>
        </details>
      </li>
      <li><a class="px-4 mt-4 text-lg" href="/contact">Contact</a></li>
    </ul>
  </div>
  
  <div class="navbar-end">
    {#if loggedIn}
      <button class="btn text-lg" onclick="my_modal_5.showModal()">logout</button>
      <dialog id="my_modal_5" class="modal modal-bottom sm:modal-middle">
        <form method="dialog" class="modal-box">
          <h3 class="font-bold text-lg">Hello</h3>
          <p class="py-4">Are you sure you want to logout?</p>
          <div class="modal-action">
            <!-- if there is a button in form, it will close the modal -->
            <button class="btn">Revert</button>
            <button class="btn" on:click={logout}>Logout</button>
          </div>
        </form>
      </dialog>
    {:else}
      <a class="btn text-xl" href="/login">Login</a>
    {/if}
  </div>
</div>
  
  <slot />