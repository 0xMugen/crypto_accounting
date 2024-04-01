<script>
    import { onMount } from 'svelte';
    import { get } from 'svelte/store';

    let wallets = [];
    let ledgers = [];
    let reports = [];

    let myModal;
    let selectedReport;

    async function getReports() {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/reports/`, {
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

    async function deleteReport(id) {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/reports/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // Add the JWT from localStorage
            }
        });

        if (res.ok) {
          reports = reports.filter(report => report.id !== id);
        } else {
            console.error('Failed to delete report', id);
        }
    }

    function openPage(reportId) {
        location.href = `/dashboard/reports/${reportId}`;
    }

    onMount(async () => {
        reports = await getReports();
    });

    function showModal(report) {
        selectedReport = report;
        myModal.showModal();
    }

    function expandCard(reportId) {
      let reportCard = document.getElementById(reportId);
      let cardContent = reportCard.querySelector('.card-content');
      let expandButton = reportCard.querySelector('.expand-button');

      // toggle max-height
      if (cardContent.style.maxHeight) {
        cardContent.style.maxHeight = null;
        reportCard.classList.remove('expanded');
      } else {
        cardContent.style.maxHeight = cardContent.scrollHeight + 'px';
        reportCard.classList.add('expanded');
      }
    }

</script>

<h1>Reports</h1>

<style>
    .card-custom {
      width: 80%; /* Adjust to your desired width */
      background-color: #3d4451; /* Change the background color */
      margin: 30px auto; /* Add more space around cards and center them */
      padding: 20px; /* Add padding inside cards */
    }

    .content-section {
        display: flex;
        justify-content: space-between;
    }

    .data-section {
        width: 45%;
    }

    /* limit the height of the card content */
    .report-card .card-content {
      max-height: 200px; /* adjust this value as needed */
      overflow: hidden;
    }

    /* style the expand button */
    .report-card .expand-button {
      text-align: center;
      cursor: pointer;
    }
    

    .report-card .expand-button .arrow {
      display: inline-block;
      width: 0;
      height: 0;
      border-left: 10px solid transparent;
      border-right: 10px solid transparent;
      border-top: 10px solid #FFF;
    }

    .report-card.expanded .expand-button .arrow {
      border-top: none;
      border-bottom: 10px solid #FFF;
    }

    .card-footer {
      position: relative; 
      display: flex;
      justify-content: flex-end; 
    }

    .expand-button {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      bottom: -10px;
    }

  </style>
  
  {#each reports as report}
  <div class="card card-custom shadow-xl">
    <div class="card-body report-card pt-0" id="{report.id}">  
      <div class="flex justify-between ">
        <div class="p-6 card-title">
          {report.name}
        </div>
        <div class="p-6">
          <div class="flex items-center">
            {#if report.start_date && report.end_date }
              <div class="flex-grow"></div>
              <h2 class="date">{report.start_date}</h2>
              <span class="mx-2">➔</span>
              <h2 class="date">{report.end_date}</h2>

            {:else if report.start_date && !report.end_date}
              <h2 class="date">Start date: {report.start_date}</h2>
            {:else if !report.start_date && report.end_date}
              <h2 class="date">End date: {report.end_date}</h2>
            {:else}
              <h2 class="date">No selected date</h2>
            {/if}
          </div>          
        </div>
      </div>
      <div class="card-content">
      <div class="content-section">
        <div class="data-section">
          <h3 >Wallets:</h3>
          <table class="table">
            <!-- head -->
            <thead>
              <tr>
                <th>Name</th>
                <th>Blockchain</th>
                <th>adress</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {#each report.wallets as wallet}
                  
              <tr>
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
                <td>{wallet.address.slice(0, 4)}...{wallet.address.slice(-4)}</td>
              </tr>
              {/each}
            </tbody>
            <tfoot>
              <tr>
              </tr>
            </tfoot>
            
          </table>
        </div>
        <div class="data-section">
          <h3>Ledgers:</h3>
          <table class="table">
            <!-- head -->
            <thead>
              <tr>
                <th>Name</th>
                <th>Exchange</th>
                <th>Source</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {#each report.ledgers as ledger}
                  
              <tr>
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
                {#if ledger.api_key}
                    <td>{ledger.api_key}</td>
                {:else}
                    <td>CSV file</td>
                {/if}
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
    
    <div class="card-footer">
      <div class="card-actions justify-end">
        <button class="btn btn-secondary" on:click={openPage(report.id)}>View</button>
        <button class="btn btn-outline btn-error" on:click={() => showModal(report)}>delete</button>
      </div>
      {#if report.wallets.length > 2 || report.ledgers.length > 2}
        <div class="expand-button" on:click={() => expandCard(report.id)}>
          <span class="arrow"></span>
        </div>
      {/if}
    </div>
    
    
  </div>
  
  </div>
{/each}


<dialog bind:this={myModal} id="my_modal_1" class="modal modal-bottom sm:modal-middle">
    <form method="dialog" class="modal-box">
        <h3 class="font-bold text-lg">Hello!</h3>
        <p class="py-4">Are you sure you want to delete this report?</p>
        <div class="modal-action">
        <!-- if there is a button in form, it will close the modal -->
        <button class="btn" on:click={() => myModal.close()}>No</button>
        <button class="btn" on:click={() => deleteReport(selectedReport.id)}>Yes</button>
        </div>
    </form>
</dialog>

