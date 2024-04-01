<script>
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { get } from 'svelte/store';

    let wallets = [];
    let ledgers = [];

    let selectedLedgers = [];
    let blockchain = ['ETH'];
    let selectableTokens = [];
    let selectedContracts = [];
    let uniqueTokens = [];
    let reportName = "";
    let currency = "";
    let useDateRange = false;
    let ids = [];
  

    let checkedValues = [];

    let isLoading = writable(false); 
    let isError = writable(false);
    let isValid = writable(false);
    let errorMessage = writable(''); 

    let selectedWallets = [];

    $: {
      ids = selectedWallets.map(function(element) {
        return element.id;
      });
      selectableTokens = [];
      for (let i = 0; i < wallets.length; i++) {
        //check if wallets[i].id is in selectedWallets
        if (ids.includes(wallets[i].id)) {
          for (let j = 0; j < wallets[i].wallettoken_set.length; j++) {
            //check for duplicates
            let found = false;
            for (let k = 0; k < selectableTokens.length; k++) {
              if (selectableTokens[k].token === wallets[i].wallettoken_set[j].token) {
                found = true;
                selectableTokens[k].count += 1;
              }
            }
            if (!found) {
              selectableTokens.push({token: wallets[i].wallettoken_set[j].token, count: wallets[i].wallettoken_set[j].count, is_asset_price: wallets[i].wallettoken_set[j].is_asset_price, contract_address: wallets[i].wallettoken_set[j].contract_address});
            }
          }
        }
      }
    selectableTokens.sort((a, b) => b.count - a.count);
    console.log(selectableTokens);
    }
    async function getWallets() {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/wallets/`, {
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

    async function getLedgers() {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/ledgers/`, {
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

    function closeErrorModal() {
        isError.set(false);
    }

    function closeValidModal() {
        isValid.set(false);
    }


    onMount(async () => {
       wallets = await getWallets();
       ledgers = await getLedgers();
    });

    function convertDate(inputString) {
        let date = new Date(inputString);
        let day = date.getDate(); // Get the day
        let monthIndex = date.getMonth(); // Get the month index (0-11)
        let year = date.getFullYear(); // Get the year

        // Array of month names
        let monthNames = ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"];

        let monthName = monthNames[monthIndex]; // Get the month name

        // if day is less than 10, prepend a '0' to maintain the format
        if (day < 10) day = '0' + day;

        return `${day} ${monthName} ${year}`; // Return in the desired format
    }

    async function createReport() {
      isLoading.set(true);
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/reports/`, {
            method: 'POST',
            body: JSON.stringify(
              { wallets: ids, 
                ledgers: selectedLedgers, 
                name: reportName, 
                blockchains: blockchain, 
                currency : currency, 
                contracts: selectedContracts
              }),
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // Add the JWT from localStorage
            }
        });
        isLoading.set(false);
        if (!res.ok) {
            errorMessage.set('Failed to authenticate request. Status code: ' + res.status);
            isError.set(true);
            return;
        } else {
            isValid.set(true);
        }

        const result = await res.json();

    }

    function handleCheckboxChange(e) {
        if (e.target.checked) {
            checkedValues.push(e.target.value);
        } else {
            let index = checkedValues.indexOf(e.target.value);
            if (index !== -1) {
                checkedValues.splice(index, 1);
            }
        }
    }

    onMount(async () => {
    });

    


</script>

<div class="relative">
<div class="flex flex-row">

  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4 text-center text-white">Tokens</h1>
    <div class="overflow-x-auto overflow-y-auto h-[70vh] w-40">
      <table class="table table-width">
        <thead>
          <tr>
            <th>Token Name</th>
          </tr>
        </thead>
        <tbody>
          {#each selectableTokens as token}
              <tr>
                  <td>
                    <label class="{token.is_asset_price === false ? 'non-asset-label' : ''}">
                      <input type="checkbox" class="checkbox" bind:group={selectedContracts} value={[token.contract_address, token.token]}/>
                      {token.token}
                  </label>
                  </td>
              </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Card -->
  <div class="p-4 rounded card items-center justify-center max-w-md w-full sm:max-w-lg mx-auto">
    <h1 class="text-2xl font-bold mb-4 text-center text-black">Input Data</h1>
    
    
    <form on:submit|preventDefault={createReport}>
        <div class="mb-4">
            
          <p class="block text-gray-700 text-sm font-bold mb-2">
          Select fiat currency
          </p>
  
          <select bind:value={currency} class="select select-bordered w-full max-w-xs">
              <option value="EUR">Euro</option>
              <option value="USD">US Dollar</option>
              <option value="GBP">British Pound</option>
          </select>
      </div>
        <div class="mb-4">
            <p class="block text-gray-700 text-sm font-bold mb-2">
            Report name
            </p>
    
            <input bind:value={reportName} type="text" placeholder="Type here" class="input input-bordered input-accent w-full max-w-xs" />
        </div>
    
        
        <button class="btn" type='submit'>Upload</button>
    </form>

</div>

  <!-- Tables -->
  <div class="flex flex-col">
    <h1 class="p-5">Wallets</h1>
    <div class="overflow-x-auto overflow-y-auto h-[40vh]">
      <table class="table table-width">
        <!-- head -->
        <thead>
          <tr>
            <th>
            </th>
            <th>Name</th>
            <th>Blockchain</th>
            <th>address</th>
            <th>Creation date</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {#each wallets as wallet}
  
              
          <tr>
            <th>
              <label>
                <input type="checkbox" class="checkbox" bind:group={selectedWallets} value={wallet}/>
              </label>
            </th>
            <td>
              <div class="flex items-center space-x-3">
                <div>
                  <div class="font-bold">{wallet.name}</div>
                  <div class="text-sm opacity-50">exchange</div>
                </div>
              </div>
            </td>
            <td>
              {wallet.blockchain}
              <br/>
              <span class="badge badge-ghost badge-sm">name</span>
            </td>
            <td><span class="address">{wallet.address.slice(0, 4)}...{wallet.address.slice(-4)}</span></td>
            <td>{convertDate(wallet.created)}</td>
          </tr>
          {/each}
        </tbody>
        <tfoot>
          <tr>
          </tr>
        </tfoot>
        
      </table>
    </div>
    <h1 class="p-5">Ledgers</h1>
    <div class="overflow-x-auto overflow-y-auto h-[40vh]">
      <table class="table table-width">
        <!-- head -->
        <thead>
        <tr>
            <th>
            </th>
            <th>Name</th>
            <th>Exchange</th>
            <th>Creation date</th>
            <th></th>
        </tr>
        </thead>
        <tbody>
        {#each ledgers as ledger}

            
        <tr>
            <th>
            <label>
                <input type="checkbox" class="checkbox" bind:group={selectedLedgers} value={ledger.id} />
            </label>
            </th>
            <td>
            <div class="flex items-center space-x-3">
                <div>
                <div class="font-bold">{ledger.name}</div>
                <div class="text-sm opacity-50">exchange</div>
                </div>
            </div>
            </td>
            <td>
            {ledger.exchange}
            <br/>
            <span class="badge badge-ghost badge-sm">name</span>
            </td>
            <td>{convertDate(ledger.created)}</td>
        </tr>
        {/each}
        </tbody>
        <tfoot>
        <tr>
        </tr>
        </tfoot>
        
    </table>
    </div>
  </div>
</div>

{#if $isLoading}
<div class="absolute inset-0 flex items-center justify-center z-10">
    <span class="loading loading-spinner loading-lg"></span>
</div>
{/if}

{#if $isValid}
<div class="fixed inset-0 flex items-center justify-center">
    <div class="p-4 bg-slate-500 rounded shadow-md">
        <h2 class="text-xl font-bold">Confirmation</h2>
        <p>You've successfully uploaded the data</p>
        <button class="btn" on:click={closeValidModal}>Close</button>
    </div>
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


</div>

<style>

.table-width {
    min-width: 400px;
  }
  .address {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .card {
    width: 100%;
    margin: 5rem;
    background-color: beige;
  }
  h2 {
    color: white;
  }
  button {
    margin: 1rem;
  }

  .non-asset-label {
        color: red;
    }
</style>