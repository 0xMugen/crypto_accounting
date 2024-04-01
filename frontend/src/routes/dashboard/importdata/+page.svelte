<script>
     import { onMount } from 'svelte';
     import { writable } from 'svelte/store';

    let selectedBlockchain;
    let wallet;
    let walletName;

    let selectedExchange;
    let ledgerName;
    let ledgerFile;

    let isLoading = writable(false); 
    let isError = writable(false);
    let isValid = writable(false);
    let errorMessage = writable(''); 

    async function addWallet() {
        if (!selectedBlockchain || !wallet || !walletName) {
            return;
        }
        isLoading.set(true);
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/wallets/`, {
            method: 'POST',
            body: JSON.stringify({ blockchain: selectedBlockchain, address: wallet, name: walletName }),
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

    async function addLedger(e) {
        if (!selectedExchange || !ledgerName || !ledgerFile) {
            return;
        }
        isLoading.set(true);

        // Create a new FormData instance
        let formData = new FormData();

        // Append the relevant data to it
        formData.append("exchange", selectedExchange);
        formData.append("name", ledgerName);
        formData.append("file", ledgerFile);

        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/ledgers/`, {
            method: 'POST',
            body: formData, // Use formData as the body instead of JSON
            headers: {
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

    function handleFileChange(event) {
        ledgerFile = event.target.files[0];
    }

    function closeErrorModal() {
        isError.set(false);
    }

    function closeValidModal() {
        isValid.set(false);
    }

</script>


<div class="flex justify-around items-center h-screen px-4 relative">
    <div class="flex flex-col items-center w-1/2">
        <div class="w-full max-w-xs p-4 rounded shadow-md card m-20 h-100">
            <!-- Your form goes here... -->
                <h1 class="text-2xl font-bold mb-4 text-center ">Input ledger CSV file</h1>
                
                
                <form on:submit|preventDefault={addLedger}>
                    <div class="mb-4">
                        <p class="block text-gray-700 text-sm font-bold mb-2">
                        Select Exchange
                        </p>
                
                        <select bind:value={selectedExchange} class="select select-bordered w-full max-w-xs">
                            <option value="KRAKEN">Kraken</option>
                            <option value="BINANCE">Binance</option>
                            <option value="COINBASE">Coinbase</option>
                        </select>
                    </div>
                
                    <div class="mb-4">
                        <p class="block text-gray-700 text-sm font-bold mb-2">
                        Name
                        </p>
                
                        <input bind:value={ledgerName} type="text" placeholder="Type here" class="input input-bordered input-accent w-full max-w-xs" />
                    </div>
                    
                    <div class="form-control w-full max-w-xs">
                        <label class="label">
                        </label>
                        <input type="file" class="file-input file-input-bordered w-full max-w-xs" on:change={handleFileChange} />  <!-- Added event handler -->
                        <label class="label">
                        </label>
                    </div>
                    <button class="btn" type='submit'>Upload</button>
                </form>    
        </div>
    </div>
    <div class="flex flex-col items-center w-1/2">
        <div class="w-full max-w-xs p-4 rounded shadow-md card m-20 h-100">
            <!-- Your form goes here... -->
                <h1 class="text-2xl font-bold mb-4 text-center ">Input Wallet data</h1>
                
                
                <form on:submit|preventDefault={addWallet}>
                    <div class="mb-4">
                        <p class="block text-gray-700 text-sm font-bold mb-2">
                        Select Blockchain
                        </p>
                
                        <select bind:value={selectedBlockchain} class="select select-bordered w-full max-w-xs">
                            <option value="BTC">Bitcoin</option>
                            <option value="ETH">Ethereum</option>
                            <option value="MATIC">Polygon</option>
                        </select>
                    </div>

                    <div class="mb-4">
                        <p class="block text-gray-700 text-sm font-bold mb-2">
                        Name
                        </p>
                
                        <input bind:value={walletName} type="text" placeholder="Type here" class="input input-bordered input-accent w-full max-w-xs" />
                    </div>
                
                    <div class="mb-4">
                        <p class="block text-gray-700 text-sm font-bold mb-2">
                        Input wallet
                        </p>
                
                    <input bind:value={wallet} type="text" placeholder="Type here" class="input input-bordered input-accent w-full max-w-xs" />
        
        
                    </div>
                    <button class="btn" type='submit'>Upload</button>
                </form>
        
    
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

    {#if $isValid}
        <div class="fixed inset-0 flex items-center justify-center">
            <div class="p-4 bg-slate-500 rounded shadow-md">
                <h2 class="text-xl font-bold">Confirmation</h2>
                <p>You've successfully uploaded the data</p>
                <button class="btn" on:click={closeValidModal}>Close</button>
            </div>
        </div>
    {/if}
</div>



        


<style>
    .card {
        background-color: beige;

    }
    h1 {
        color: #000;
    }
    h2 {
        color: white;
    }
    button {
        margin: 1rem;
    }
</style>