<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  export let data;
  let subreports = [];
  let transactions = [];
  let selectedSubreport = null;
  let selectedTransaction;
  let myModal;
  let transaction_length;

  let selectedTransactionId = null;
  let editedTransactions = {};

  let totalgazfee = 0;

  export let placeholder = "Decsription :";
  let isTextAreaFocused = false;
  let textContent = "";

  function handleRowClick(transactionId) {
    selectedTransactionId = transactionId;
  }

  async function updateAssetPrice(transaction) {
    const updatedTransactionData = {
      asset_price: transaction.asset_price,
    };

    const res = await fetch(
      `${import.meta.env.VITE_API_URL}/api/transactions/${transaction.id}/`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(updatedTransactionData),
      }
    );

    if (res.ok) {
      transactions = await getTransactions(selectedSubreport);
    } else {
      // Handle error response here
    }
  }

  async function revertAssetPrice(transactionId) {
    const transaction = transactions.find(
      (transaction) => transaction.id === transactionId
    );
    transaction.asset_price = transaction.original_asset_price;

    await updateAssetPrice(transaction);
  }

  async function getReports() {
    const res = await fetch(
      `${import.meta.env.VITE_API_URL}/api/subreports/?report_id=${data.title}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`, // Add the JWT from localStorage
        },
      }
    );

    if (!res.ok) {
      location.href = "/login";
    }

    const result = await res.json();
    return result;
  }

  async function getTransactions(report_id) {
    const res = await fetch(
      `${
        import.meta.env.VITE_API_URL
      }/api/transactions/?report_id=${report_id}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`, // Add the JWT from localStorage
        },
      }
    );

    const result = await res.json();
    transaction_length = result.length;
    return result;
  }

  onMount(async () => {
    subreports = await getReports();
    selectedSubreport = subreports[0].id;
    transactions = await getTransactions(subreports[0].id);
    await updateTotalGasFee();
  });

  function getDoubleRefids() {
    const refidCountMap = new Map();
    transactions.forEach((transaction) => {
      if (transaction.source === "ledger") {
        const refid = transaction.refid;
        if (refidCountMap.has(refid)) {
          refidCountMap.set(refid, refidCountMap.get(refid) + 1);
        } else {
          refidCountMap.set(refid, 1);
        }
      }
    });

    const doubleRefids = [];
    refidCountMap.forEach((count, refid) => {
      if (count > 1) {
        doubleRefids.push(refid);
      }
    });

    return doubleRefids;
  }

  // Function to generate alternating colors (yellow and orange) for double refids
  let borderToggle = false;
  function getColorForRowKRK(transaction) {
    const doubleRefids = getDoubleRefids();
    if (doubleRefids.includes(transaction.refid)) {
      const index = doubleRefids.indexOf(transaction.refid);
      const color = index % 2 === 0 ? "#15203a" : "#192644";
      borderToggle = !borderToggle; // Switch the color
      return ` background-color: ${color}`;
    }
    return "transparent"; // default color when refid does not appear more than once
  }

  function getColorForTxType(txType) {
    switch (txType) {
      case "inner":
        return "#02ff00";
      case "outer":
        return "#ff0000";
      case "internal":
        return "#006bff";
      default:
        return "transparent";
    }
  }

  async function handleButtonClick(subreport) {
    selectedSubreport = subreport.id;
    transactions = await getTransactions(subreport.id);
  }

  function truncateFloat(value) {
    return parseFloat(value).toString();
  }

  function showModal(transaction) {
    selectedTransaction = transaction;
    myModal.showModal();
  }

  function shortFormatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: "2-digit", month: "2-digit", day: "2-digit" };
    return date.toLocaleDateString("en-GB", options);
  }

  function longFormatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: "numeric", month: "long", day: "numeric" };
    return date.toLocaleDateString("en-GB", options);
  }

  function formatTime(dateString) {
    const date = new Date(dateString);
    const options = {
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
      hour12: true,
    };
    return date.toLocaleTimeString("en-GB", options);
  }

  function truncateNumberWithEllipsis(number, maxDecimalDigits) {
    const truncatedNumber = parseFloat(number).toFixed(maxDecimalDigits);
    return truncatedNumber.length > maxDecimalDigits
      ? `${truncatedNumber.slice(0, maxDecimalDigits)}...`
      : truncatedNumber;
  }

  function calculateTotalGasFee() {
    let total = 0;
    transactions.forEach((transaction) => {
      if (transaction.source === "ledger") {
        total += parseFloat(transaction.gasToCurrency);
      }
    });
    return total;
  }

  function handleFocus() {
    isTextAreaFocused = true;
  }

  function handleBlur() {
    isTextAreaFocused = false;
  }
</script>

<main>
  <div class="flex justify-between">
    <div class="flex justify-start items-center pl-4">
      <div class="sticky top-0 flex flex-col justify-center items-center pt-6">
        <div class="btn-group pb-2">
          {#each subreports as subreport}
            <button
              class="btn join-item {selectedSubreport === subreport.id
                ? 'btn-selected'
                : ''}"
              on:click={() => handleButtonClick(subreport)}
            >
              {subreport.token}
            </button>
          {/each}
        </div>

        <p class="pb-12 pt-4">Number of transactions: {transaction_length}</p>
      </div>
    </div>

    <div class="flex h-auto justify-center items-start p-0">
      <div class="totaux flex justify-between space-x-7 bg-black pt-2">
        <div></div>
        <div></div>
        <p>Total Gas Fee:</p>
        <p>Total Gas Fiat: {totalgazfee}</p>
        <p>Total Appreciaion:</p>
        <div></div>
        <div></div>
      </div>
    </div>

    <div class="flex justify-end">
      <p>Legend :</p>
      <div>

      </div>
    </div>

  </div>

  <div class="w-full pr-2 pl-2">
    <table class="table">
      <!-- Table titles-->
      <thead>
        <tr>
          <th class="flex flex-col items-center">
            <div>Date</div>
            <div class="text-xs"><i>(DD/MM/YY)</i></div>
          </th>
          <th>Source</th>
          <th>Asset</th>
          <th>Tx Type</th>
          <th>Data</th>
          <th>Balance</th>
          <th>Total balance</th>
          <th />
          <th>Asset price</th>
          <th>Average <br />buy price</th>
          <th>Appreciation</th>
          <th>Title</th>
        </tr>
      </thead>

      {#each transactions as transaction}
        {#if transaction.source == "ledger"}
          <div class="mt-[2px]" />
          <tbody class="ledger" style={getColorForRowKRK(transaction)}>
            <!--change transaction on click-->
            <tr
              on:click={() =>
                (selectedTransactionId =
                  selectedTransactionId === transaction.id
                    ? null
                    : transaction.id)}
              style="background-color: {selectedTransactionId === transaction.id
                ? '#caf8ffe2'
                : 'transparent'}"
            >
              {#if selectedTransactionId === transaction.id}
                <td colspan="2">
                  <div
                    class="flex flex-col items-center justify-center space-x-3 w-full h-full"
                  >
                    <p class="text-center text-lg font-bold text-[#3e3e3e]">
                      <b>{longFormatDate(transaction.time)}</b>
                    </p>
                    <div
                      class="text-sm opacity-50 uppercase font-bold text-[#575f5e]"
                    >
                      {formatTime(transaction.time)}
                    </div>
                  </div>
                </td>

                <td>
                  <div class="pb-2">
                    <p class="text-[#798584] italic">Source :</p>
                    <p class="font-bold text-[#000]">{transaction.exchange}</p>
                  </div>
                  <div class="pt-2">
                    <p class="text-[#798584] italic">Asset</p>
                    <p class="font-bold text-[#000]">{transaction.asset}</p>
                  </div>
                </td>

                <td>
                  <div class="pb-2">
                    <p class="text-[#798584] italic">Tx type :</p>
                    <p class="font-bold text-[#000]">
                      {transaction.transaction_type}
                    </p>
                  </div>
                  <div class="pt-2">
                    <p class="text-[#798584] italic">Amount :</p>
                    <p class="font-bold text-[#000]">
                      {truncateFloat(transaction.amount)}
                    </p>
                  </div>
                </td>

                <td colspan="1">
                  <div class="pb-2">
                    <p class="text-[#798584] italic">Balance :</p>
                    <p class="text-[#000] font-bold">
                      {truncateFloat(transaction.balance)}
                    </p>
                  </div>
                  <div class="pt-2">
                    <p class="text-[#798584] italic">Total balance :</p>
                    <p class="text-[#000] font-bold">
                      {transaction.total_balance}
                    </p>
                  </div>
                </td>

                <td colspan="2">
                  <div class=" flex justify-between pb-1 w-full pb-2">
                    <div>
                      <p class="text-[#798584] italic">Fees :</p>
                      <p class="text-[#000] font-bold">
                        {truncateFloat(transaction.fee)}
                      </p>
                    </div>
                    <div>
                      <p class="text-[#798584] italic">Appreciation :</p>
                      <p class="text-[#000] font-bold">
                        {truncateFloat(transaction.appreciation)}
                      </p>
                    </div>
                  </div>
                  <div class="pt-3">
                    <p class="text-[#798584] italic">Average buy price :</p>
                    <p class="text-[#000] font-bold">
                      {truncateFloat(transaction.average_buy_price)}
                    </p>
                  </div>
                </td>

                <td colspan="5">
                  <div>
                    <textarea
                      on:click|stopPropagation
                      class="textarea w-full mb-2 font-bold"
                      rows="1"
                      placeholder="Title"
                      style="resize: none;"
                    />
                  </div>
                  <div>
                    <textarea
                      on:click|stopPropagation
                      class="textarea w-full mt-2"
                      rows="3"
                      placeholder="Description"
                    />
                  </div>
                </td>
              {:else}
                <td>
                  <div class="flex items-center space-x-3 w-full h-full">
                    <div>
                      <div><b>{shortFormatDate(transaction.time)}</b></div>
                      <div
                        class="text-sm opacity-50 uppercase"
                        style="font-size: 0.8em;"
                      >
                        {formatTime(transaction.time)}
                      </div>
                    </div>
                  </div>
                </td>

                <th>
                  <p>{transaction.exchange}</p>
                </th>

                <td>
                  <div class="flex items-center space-x-3">
                    <div>
                      <div class="font-bold">{transaction.asset}</div>
                    </div>
                  </div>
                </td>

                <td>
                  {transaction.transaction_type}
                  <br />
                  <span class="badge badge-ghost badge-sm">type</span>
                </td>

                <td>
                  {truncateFloat(transaction.amount)}
                  <br />
                  <span class="badge badge-ghost badge-sm">amount</span>
                </td>

                <td>
                  {truncateFloat(transaction.balance)}
                  <br />
                  <span class="badge badge-ghost badge-sm">balance</span>
                </td>

                <th>
                  {truncateNumberWithEllipsis(transaction.total_balance, 10)}
                </th>

                <td>
                  {truncateFloat(transaction.fee)}
                  <br />
                  <span class="badge badge-ghost badge-sm">fees</span>
                </td>

                <td />

                <td>
                  {truncateFloat(transaction.average_buy_price)}
                </td>

                <td>
                  {truncateFloat(transaction.appreciation)}
                </td>
                  <!--Title to fetch from the title textarea if it exists-->
                <td />
              {/if}
            </tr>
          </tbody>
        {:else}
          <div class="mt-[2px]" />
          <tbody
            class="blockExplorer mt-[2px]"
            style="background-color: #111a2e; border-left: 3px solid {getColorForTxType(
              transaction.tx_type
            )};"
          >
            <tr
              on:click={() =>
                (selectedTransactionId =
                  selectedTransactionId === transaction.id
                    ? null
                    : transaction.id)}
              style="background-color: {selectedTransactionId === transaction.id
                ? '#caf8ffe2'
                : 'transparent'}"
            >
              {#if selectedTransactionId === transaction.id}
                <td colspan="2">
                  <div
                    class="flex flex-col items-center justify-center space-x-3 w-full h-full"
                  >
                    <p class="text-center text-lg font-bold text-[#3e3e3e]">
                      <b>{longFormatDate(transaction.time)}</b>
                    </p>
                    <div
                      class="text-sm opacity-50 uppercase font-bold text-[#575f5e]"
                    >
                      {formatTime(transaction.time)}
                    </div>
                  </div>
                </td>

                <td>
                  <div class="pb-2">
                    <p class="text-[#798584] italic">Source :</p>
                    <p class="font-bold text-[#000]">
                      {#if transaction.isError == 1}
                        <span title="Transaction Reverted">
                          <div class="p-2">
                            <svg
                              viewBox="0 0 20 20"
                              xmlns="http://www.w3.org/2000/svg"
                              fill="none"
                              stroke="#ff0000"
                              style="width: 20px; height: 20px;"
                            >
                              <g id="SVGRepo_bgCarrier" stroke-width="0" />
                              <g
                                id="SVGRepo_tracerCarrier"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                              />
                              <g id="SVGRepo_iconCarrier">
                                <path
                                  fill="#ff0000"
                                  fill-rule="evenodd"
                                  d="M10 3a7 7 0 100 14 7 7 0 000-14zm-9 7a9 9 0 1118 0 9 9 0 01-18 0zm10.01 4a1 1 0 01-1 1H10a1 1 0 110-2h.01a1 1 0 011 1zM11 6a1 1 0 10-2 0v5a1 1 0 102 0V6z"
                                />
                              </g>
                            </svg>
                          </div>
                        </span>
                      {/if}
                      {transaction.exchange}
                    </p>
                  </div>
                  <div class="pt-2">
                    <p class="text-[#798584] italic">Asset</p>
                    <p class="font-bold text-[#000]">{transaction.asset}</p>
                  </div>
                </td>

                <td>
                  <div class="pb-2">
                    <p class="text-[#798584] italic">Tx type :</p>
                    <p class="font-bold text-[#000]">
                      {transaction.tx_type}
                    </p>
                  </div>
                  <div class="pt-2">
                    <p class="text-[#798584] italic">Amount :</p>
                    <p class="font-bold text-[#000]">
                      {truncateFloat(transaction.amount)}
                    </p>
                  </div>
                </td>

                <td>
                  <div class="pb-2">
                    <p class="text-[#798584] italic">Amount :</p>
                    <p class="font-bold text-[#000]">
                      {truncateFloat(transaction.amount)}
                    </p>
                  </div>

                  <div class="pb-2 pt-2">
                    <p class="text-[#798584] italic">GasFee :</p>
                    <p class="font-bold text-[#000]">
                      {truncateFloat(transaction.gasfee)}
                    </p>
                  </div>

                  <div class="pt-2">
                    <p class="text-[#798584] italic">GasFiat :</p>
                    <p class="font-bold text-[#000]">
                      {truncateFloat(transaction.gasToCurrency)}
                    </p>
                  </div>
                </td>

                <td>
                  <div class="pb-2">
                    <p class="text-[#798584] italic">Balance :</p>
                    <p class="text-[#000] font-bold">
                      {truncateFloat(transaction.balance)}
                    </p>
                  </div>
                  <div class="pt-2">
                    <p class="text-[#798584] italic">Total balance :</p>
                    <p class="text-[#000] font-bold">
                      {transaction.total_balance}
                    </p>
                  </div>
                </td>

                <td colspan="2">
                  <div>
                    <p class="text-[#798584] italic">Asset price :</p>
                    <input
                    type="number"
                    bind:value={transaction.asset_price}
                    class="input-field {transaction.asset_price ==
                    transaction.original_asset_price
                      ? ''
                      : 'text-orange-700'}"
                    style="width: calc(1ch * {transaction.asset_price.toString()
                      .length} + 2ex)"
                    />
                    <button
                    on:click|preventDefault={() =>
                      updateAssetPrice(transaction)}>Confirm</button
                    >
                    {#if transaction.asset_price != transaction.original_asset_price}
                    <button on:click={() => showModal(transaction)}
                      >Revert</button
                    >
                    {/if}
                  </div>

                  <div class="pt-3">
                    <p class="text-[#798584] italic">Average buy price :</p>
                    <p class="text-[#000] font-bold">
                      {truncateFloat(transaction.average_buy_price)}
                    </p>
                  </div>

                  <div class="pt-3">
                    <p class="text-[#798584] italic">Appreciation :</p>
                    <p class="text-[#000] font-bold">
                      {truncateFloat(transaction.appreciation)}
                    </p>
                  </div>
                </td>

                <td colspan="3">
                  <div>
                    <textarea
                      on:click|stopPropagation
                      class="textarea w-full mb-2 font-bold"
                      rows="1"
                      placeholder="Title"
                      style="resize: none;"
                    />
                  </div>
                  <div>
                    <textarea
                      on:click|stopPropagation
                      class="textarea w-full mt-2"
                      rows="3"
                      placeholder="Description"
                    />
                  </div>
                </td>
              {:else}
                <td>
                  <div class="flex items-center space-x-3 w-full h-full">
                    <div>
                      <div class="bold">
                        <b>{shortFormatDate(transaction.time)}</b>
                      </div>
                      <div
                        class="text-sm opacity-50 uppercase"
                        style="font-size: 0.8em;"
                      >
                        {formatTime(transaction.time)}
                      </div>
                    </div>
                  </div>
                </td>

                <th>
                  <div style="display: flex; align-items: center;">
                    {#if transaction.isError == 1}
                      <span title="Transaction Reverted">
                        <div class="p-2">
                          <svg
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            stroke="#ff0000"
                            style="width: 20px; height: 20px;"
                          >
                            <g id="SVGRepo_bgCarrier" stroke-width="0" />
                            <g
                              id="SVGRepo_tracerCarrier"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                            />
                            <g id="SVGRepo_iconCarrier">
                              <path
                                fill="#ff0000"
                                fill-rule="evenodd"
                                d="M10 3a7 7 0 100 14 7 7 0 000-14zm-9 7a9 9 0 1118 0 9 9 0 01-18 0zm10.01 4a1 1 0 01-1 1H10a1 1 0 110-2h.01a1 1 0 011 1zM11 6a1 1 0 10-2 0v5a1 1 0 102 0V6z"
                              />
                            </g>
                          </svg>
                        </div>
                      </span>
                    {/if}
                    {transaction.exchange}
                  </div>
                </th>

                <td>
                  <div class="flex items-center space-x-3">
                    <div>
                      <div class="font-bold">{transaction.asset}</div>
                    </div>
                  </div>
                </td>
                <td>
                  {transaction.tx_type}
                  <br />
                  <span class="badge badge-ghost badge-sm">type</span>
                </td>
                <td>
                  Amount: <span class="opacity-50"
                    >{truncateFloat(transaction.amount)}</span
                  >
                  <br />
                  GasFee:
                  <span class="opacity-50"
                    >{truncateNumberWithEllipsis(transaction.gasfee, 10)}</span
                  >
                  <br />
                  GasFiat:
                  <span class="opacity-50"
                    >{truncateFloat(transaction.gasToCurrency)}</span
                  >
                </td>

                <td>
                  {truncateNumberWithEllipsis(transaction.balance, 10)}
                  <br />
                  <span class="badge badge-ghost badge-sm">balance</span>
                </td>

                <th>
                  {truncateNumberWithEllipsis(transaction.total_balance, 10)}
                </th>

                <td>
                  {transaction.hash.slice(0, 4)}...{transaction.hash.slice(-4)}
                  <br />
                  <span class="badge badge-ghost badge-sm">hash</span>
                </td>

                <td>
                  <div
                    class={transaction.asset_price ==
                    transaction.original_asset_price
                      ? ""
                      : "text-orange-700"}
                  >
                    {truncateFloat(transaction.asset_price)}
                    {#if transaction.asset_price != transaction.original_asset_price}
                      <button on:click={() => showModal(transaction)}
                        >Revert</button
                      >
                    {/if}
                  </div>
                </td>

                <td>
                  {truncateFloat(transaction.average_buy_price)}
                </td>

                <td>
                  {truncateFloat(transaction.appreciation)}
                </td>

                <td />
              {/if}
            </tr>
          </tbody>
          {#if selectedTransactionId === transaction.id}
            <tr style="background-color: {selectedTransactionId === transaction.id
              ? '#caf8ffe2'
              : 'transparent'}">
              <td></td>
              <td></td>
              <td colspan="9">
                <div class="flex space-x-1">
                  <p class="text-[#798584] italic">Hash :</p>
                  <p class="text-[#000] font-bold">
                    {transaction.hash}
                  </p>
                </div>
              </td>
            </tr>
          {/if}
        {/if}
      {/each}

      <!-- foot -->
    </table>
  </div>

  <dialog
    bind:this={myModal}
    id="my_modal_1"
    class="modal modal-bottom sm:modal-middle"
  >
    <form method="dialog" class="modal-box">
      <h3 class="font-bold text-lg">Hello!</h3>
      <p class="py-4">
        Are you sure you want to remove your edited price and go back to the one
        we've got?
      </p>
      <div class="modal-action">
        <!-- if there is a button in form, it will close the modal -->
        <button class="btn" on:click={() => myModal.close()}>No</button>
        <button
          class="btn"
          on:click={() => revertAssetPrice(selectedTransactionId)}>Yes</button
        >
      </div>
    </form>
  </dialog>
</main>

<style>
  /* .ledger {
    background-color: red;
  } */

  main {
    box-shadow: inset 0 0 0 2px
      linear-gradient(to right, #000 0%, rgba(255, 255, 255, 0) 3%);
  }

  .btn-selected {
    background-color: #f5854ae2;
  }

  .textarea {
    background-color: #000000ab;
    box-shadow: inset 0 0 4px rgba(26, 26, 26, 0.5);
    color: #494949;
    border-radius: 3px;
    border: 2px solid transparent;
    outline: none;
    transition: all 0.2s;
  }

  .textarea:hover {
    cursor: pointer;
    background-color: #363636ab;
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
  }

  .textarea:focus {
    cursor: text;
    color: #ffffff;
    background-color: #000000c2;
    border-color: #000;
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
  }

  table {
    border-collapse: collapse;
    width: 100%;
  }

  th,
  td,
  tr {
    border: none;
  }

  .totaux {
    display: -ms-inline-grid;
    padding-bottom: 20px;
    clip-path: 
      polygon(
        0 0,
        100% 0,
        90% 3em,
        10% 3em,
        0 0
      );
  }
</style>
