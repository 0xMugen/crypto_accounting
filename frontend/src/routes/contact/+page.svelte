<script>
  let nameInput = '';
  let email = '';
  let message = '';
  let success = '';
  let errors = ['', '', '',''];
  let text = "";
  let limit = 1000;

  function validateForm() {
    clearMessages();
    let errorFlag = false;

    if (nameInput.length < 1) {
      errors[0] = 'Name cannot be blank';
      errorFlag = true;
    }

    if (!emailIsValid(email)) {
      errors[1] = 'Invalid email address';
      errorFlag = true;
    }

    if (message.length < 1) {
      errors[2] = 'Please enter a message';
      errorFlag = true;
    }

    if (message.length > limit) {
      errors[2] = 'Your message is to long';
      errorFlag = true;
    }

    if (!errorFlag) {
      success = 'Success!';
    }
  }

  function clearMessages() {
    errors = ['', '', ''];
    success = '';
  }

  function emailIsValid(email) {
    let pattern = /\S+@\S+\.\S+/;
    return pattern.test(email);
  }
</script>

<div id="overlay" class="w-full mb-10 -translate-y-20">
  <form on:submit|preventDefault={validateForm}>
    <h1 class="tracking-[5px]"><b>Contact Us</b></h1>

    <label for="name">Name :</label>
    <input type="text" bind:value={nameInput} placeholder="Your name">
    <small class="error">{errors[0]}</small>

    <label for="email">Email :</label>
    <input type="text" bind:value={email} placeholder="Your email">
    <small class="error">{errors[1]}</small>

    <label for="message">Message</label>
    <textarea bind:value={message} class:invalid={text.length > limit} placeholder="Your message" rows="6"></textarea>
    <small class="error">{errors[2]}</small>
    <p id="result" style="color: {message.length > limit ? '#ff2851' : '#737373'}">{message.length}/{limit}</p>

    <div class="center">
      <input type="submit" value="Send Message">
      <p id="success">{success}</p>
    </div>
  </form>
</div>

  <style>
  form {
    max-width: 550px;
    width: 90%;
    background: #fff;
    margin: 17vh auto 0 auto;
    padding: 40px;
    border-radius: 3px;
    box-sizing: border-box;
  }

  h1 {
    margin: 0;
    text-align: center;
    color: #000;
    font-size: 2em;
  }

  label {
    display: block;
    margin: 20px 0;
    color: #000000a4;
    font-size: 1em;
  }

  input, textarea {
    width: 100%;
    padding: 10px;
    box-sizing: border-box;
    outline: none;
    resize: none;
    border: none;
    border-bottom: 1px solid #d3d3d3;
    background-color: #ededed;
    color: #000;
    letter-spacing: 0.8px;
  }

  input[type="text"]:focus, textarea:focus {
    border-bottom: 1px solid #0073ffb6;
  }

  textarea::-webkit-scrollbar {
    width: 4px;
  }

  textarea::-webkit-scrollbar-thumb {
    background-color: #0073ffb6;
  }

  .center {
    text-align: center;
  }

  input[type="submit"] {
    margin-top: 30px;
    width: 90%;
    max-width: 200px;
    background: linear-gradient(to right, rgb(106, 240, 255), rgb(207, 254, 255));
    color: #000000d6;
    font-size: 17px;
    font-weight: 600;
    cursor: pointer;
    border-radius: 3px;
    box-shadow: 0 0 3px rgba(12, 12, 12, 0.356);
  }

  .error {
    color: red;
  }

  .error-border {
    border-bottom: 1px solid red;
  }

  #success {
    color: #28a745;
  }

  </style>
  
 
  