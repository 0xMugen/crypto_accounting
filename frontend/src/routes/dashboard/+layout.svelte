<script>
    import { onMount } from "svelte";

    let username;
    let loggedIn = false;
    if (typeof window !== "undefined") {
        //check for username in local storage
        username = localStorage.getItem("username");
        loggedIn = username ? true : false;
    }

    onMount(() => {
        if (!loggedIn) {
            window.location.href = "/login";
        }
    });
</script>

<div class="drawer lg:drawer-open">
  <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col items-center">
    <!-- Page content here -->
    <label for="my-drawer-2" class="btn btn-primary drawer-button lg:hidden">Open drawer</label>
    <slot />

  </div> 
  <div class="drawer-side w-65">
    <label for="my-drawer-2" class="drawer-overlay"></label>
    <ul class="menu pl-5 w-60 h-full bg-base-200">
      <!-- Sidebar content here -->
      <li  class="text-xl font-semibold p-0"><a href="/dashboard/importdata">Import data</a></li>
      <li class="pl-4 text-lg text-gray-450"><a href="/dashboard/wallets">Wallets</a></li>
      <li class="pl-4 text-lg text-gray-450"><a href="/dashboard/ledgers">Ledgers</a></li>
      <li class="text-xl font-semibold"><a href="/dashboard/createReport">Create report</a></li>
      <li class="pl-4 text-lg text-gray-200"><a href="/dashboard/reports">Reports</a></li>
    </ul>
  </div>
</div>

<style>
.drawer-side {
  width: 200px; 
}

.menu li {
  margin-bottom: 8px;
}
</style>