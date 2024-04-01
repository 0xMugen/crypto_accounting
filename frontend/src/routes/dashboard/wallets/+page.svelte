<script>
    import { onMount } from 'svelte';

    let wallets = [];
    let myModal;
    let selectedWallet = null;



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

    async function deleteWallet(id) {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/wallets/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // Add the JWT from localStorage
            }
        });

        location.reload(); // Refresh the page
    }

    onMount(async () => {
        myModal = document.getElementById('my_modal_1');
        wallets = await getWallets();
    });

    function showModal(wallet) {
        selectedWallet = wallet;
        myModal.showModal();
    }

    function openPage(walletId) {
        location.href = `/dashboard/wallets/${walletId}`;
    }
</script>


        <div class="overflow-x-auto">
            <div class="flex flex-col items-center">

                <h2>Wallets</h2>
                <table class="table">
                <!-- head -->
                    <thead>
                        <tr>
                        <th>name</th>
                        <th>Blockchain</th>
                        <th>Address</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each wallets as wallet}
                        <tr>
                            <th>{wallet.name}</th>
                          <td>{wallet.blockchain}</td>
                          <td>{wallet.address}</td>
                          <th>
                            <button class="btn btn-ghost btn-xs" on:click={openPage(wallet.id)} >details</button>
                          </th>
                          <td>
                            <button class="btn btn-outline btn-error" on:click={() => showModal(wallet)}>delete</button>
                          </td>
                        </tr>
                      {/each}

                      <dialog bind:this={myModal} id="my_modal_1" class="modal modal-bottom sm:modal-middle">
                        <form method="dialog" class="modal-box">
                          <h3 class="font-bold text-lg">Hello!</h3>
                          <p class="py-4">Are you sure you want to delete this wallet?</p>
                          <div class="modal-action">
                            <!-- if there is a button in form, it will close the modal -->
                            <button class="btn" on:click={() => myModal.close()}>No</button>
                            <button class="btn" on:click={() => deleteWallet(selectedWallet.id)}>Yes</button>
                          </div>
                        </form>
                      </dialog>
                    </tbody>
                </table>
            </div>
        </div>


<style>
    .card {
        background-color: #37cdbe;

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