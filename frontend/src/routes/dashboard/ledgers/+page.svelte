<script>
    import { onMount } from "svelte";

    let ledgers= [];
    let myModal;
    let selectedLedger;


    async function getLedger() {
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

    async function deleteLedger(id) {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/ledgers/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // Add the JWT from localStorage
            }
        });

        location.reload(); // Refresh the page
    }


    function showModal(ledger) {
        selectedLedger = ledger;
        myModal.showModal();
    }

    function openPage(ledgerId) {
        location.href = `/dashboard/ledgers/${ledgerId}`;
    }



    onMount(async () => {
        ledgers = await getLedger();
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

</script>
<div class="overflow-x-auto">
    <table class="table">
      <!-- head -->
      <thead>
        <tr>
          <th>
            <label>
              <input type="checkbox" class="checkbox" />
            </label>
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
              <input type="checkbox" class="checkbox" />
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
          <th>
            <button class="btn btn-ghost btn-xs" on:click={openPage(ledger.id)} >details</button>
          </th>
          <th>
            <button class="btn btn-outline btn-error" on:click={() => showModal(ledger)}>delete</button>
          </th>
        </tr>
        {/each}
      </tbody>
      <tfoot>
        <tr>
        </tr>
      </tfoot>
      
    </table>
  </div>

<dialog bind:this={myModal} id="my_modal_1" class="modal modal-bottom sm:modal-middle">
    <form method="dialog" class="modal-box">
        <h3 class="font-bold text-lg">Hello!</h3>
        <p class="py-4">Are you sure you want to delete this ledger?</p>
        <div class="modal-action">
        <!-- if there is a button in form, it will close the modal -->
        <button class="btn" on:click={() => myModal.close()}>No</button>
        <button class="btn" on:click={() => deleteLedger(selectedLedger.id)}>Yes</button>
        </div>
    </form>
</dialog>



<style>
    .card {
        background-color: #37cdbe;

    }
    h1 {
        color: #000;
    }
    button {
        margin: 1rem;
    }
</style>