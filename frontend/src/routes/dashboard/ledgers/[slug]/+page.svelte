<script>
    import { onMount } from 'svelte';

    export let data;
    let ledgerId = data.title;
    let ledger = [];
    

    async function getLedger() {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/ledgerSort/?ledger_id=${ledgerId}`, {
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
        ledger = await getLedger();
    });
</script>



<div class="overflow-x-auto">
    <table class="table">
      <!-- head -->
      <thead>
        <tr>
          <th>order</th>
          <th>refid</th>
          <th>time</th>
          <th>asset</th>
          <th>transaction type</th>
          <th>fee</th>
          <th>balance</th>
          <th>amount</th>
        </tr>
      </thead>
      <tbody>
        <!-- row 1 -->
        {#each ledger as item}
        <tr>
          <th>{item.order}</th>
          <td>{item.refid}</td>
          <td>{convertDateReadable(item.time)}</td>
          <td>{item.asset}</td>
          <td>{item.transaction_type}</td>
          <td>{item.fee}</td>
        <td>{item.balance}</td>
        <td>{item.amount}</td>
        </tr>
       {/each}
      </tbody>
    </table>
  </div>