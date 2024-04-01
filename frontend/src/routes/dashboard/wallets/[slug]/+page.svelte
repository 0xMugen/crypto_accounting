<script>
    import { onMount } from 'svelte';

    export let data;
    let walletId = data.title;
    let wallet = [];
    let walletTokens = [];
    let selectedToken = null;
    let container;

    function scrollLeft() {
    container.scrollBy({
        top: 0,
        left: -100,
        behavior: 'smooth'
    });
    }

    function scrollRight() {
    container.scrollBy({
        top: 0,
        left: 100,
        behavior: 'smooth'
    });
    }

    async function getWallet() {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/walletSort/?wallet_id=${walletId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // Add the JWT from localStorage
            }
        });

        if (!res.ok) {
            location.href = "/login";
        }

        const result = await res.json();
        return result;
    } 

    async function getTokens() {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/walletTokens/?wallet_id=${walletId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // Add the JWT from localStorage
            }
        });

        if (!res.ok) {
            location.href = "/login";
        }

        const result = await res.json();
        return result;
    }

    function convertDateReadable(dateString) {
        let date = new Date(dateString);
        let options = { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true };
        return date.toLocaleString('en-US', options);
    }

    onMount(async () => {
        wallet = await getWallet();
        walletTokens = await getTokens();
        walletTokens = walletTokens.sort((a, b) => b.count - a.count);
    });

    function truncateFloat(value) {
      return parseFloat(value).toString();
    }

</script>

<div><h1></h1></div>
<div class="half-viewport overflow-x-auto p-5">
    <div class="flex flex-row whitespace-nowrap">
        <div on:click={scrollLeft} class="arrow-icon p-5">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
        </div>
        <div bind:this={container} class="flex flex-row whitespace-nowrap overflow-x-scroll scrollbar-hide">
            {#each walletTokens as item}
            <input 
                class="join-item btn mx-2 {item.is_asset_price === false ? 'non-asset' : ''}" 
                type="radio" 
                name="options" 
                aria-label={item.token} 
                checked={selectedToken === item.token}
                on:click={() => selectedToken = selectedToken === item.token ? null : item.token}
            />
            {/each}
        </div>
        <div on:click={scrollRight} class="arrow-icon p-5">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
        </div>
    </div>
</div>
<div class="overflow-x-auto">
    <table class="table">
      <!-- head -->
      <thead>
        <tr>
            <th>Time</th>
            <th>block_number</th>
            <th>hash</th>
            <th>amount</th>
            <th>gasfee</th>
            <th>sender</th>
            <th>receiver</th>
            <th>token_name</th>
        </tr>
      </thead>
      <tbody>
        <!-- row 1 -->
        {#each wallet as item (item.id)} <!-- Make sure to add a key (item.id) for performance and correct behavior -->
        {#if selectedToken === null || selectedToken === item.token_name}
        <tr>
            <td>{convertDateReadable(item.time)}</td>
            <th>{item.block_number}</th>
            <td>{item.hash.slice(0, 4)}...{item.hash.slice(-4)}</td>
            <td>{truncateFloat(item.amount)}</td>
            <td>{truncateFloat(item.gasfee)}</td>
            <td>{item.sender.slice(0, 4)}...{item.sender.slice(0, 4)}</td>
            <td>{item.receiver.slice(0, 4)}...{item.sender.slice(0, 4)}</td>
            <td>{item.token_name}</td>
        </tr>
        {/if}
    {/each}    
    </tbody>
    </table>
  </div>

<style>
    .half-viewport {
    max-width: 50vw;
}


  .scrollbar-hide {
    -ms-overflow-style: none;  
    scrollbar-width: none;  
  }

  .arrow-icon {
    display: flex;
    align-items: center;
    cursor: pointer;
  }

  .non-asset {
    color: red;
  }

</style>