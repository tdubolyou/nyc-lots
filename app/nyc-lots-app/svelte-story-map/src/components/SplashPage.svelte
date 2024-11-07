<script>
    export let onClose; // Function to close the splash page
  </script>
  
  <style>
    .splash {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      /* background: url("/bg.jpg") center center no-repeat; */
      background: transparent;
      background-size: cover;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      color: #232323;
      font-family: 'Source Sans Pro', sans-serif;
    }
  
    .content {
      background: url("/bg.jpg") center center no-repeat;
      /* background: #ececec; */
      padding: 20px;
      border-radius: 40px;
    }
  
    .title {
      font-size: 3rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
    }
  
    .byline {
      font-size: 1.2rem;
      margin-bottom: 1rem;
    }
  
    .text-block {
      font-size: 1rem;
      margin-bottom: 1.5rem;
      max-width: 600px;
    }
  
    .close-button {
      background: #FF5A30; /* mapTO orange */
      border: none;
      color: white;
      padding: 10px 20px;
      font-size: 1rem;
      cursor: pointer;
      border-radius: 5px;
    }
  
    .logo {
      margin-top: 20px;
      
    }
  
    .logo img {
      width: 150px;
      cursor: pointer;
    }
  </style>
  
  <div class="splash">
    <div class="content">
      <div class="title">Welcome to the Story Map</div>
      <div class="byline">By: Your Name</div>
      <div class="text-block">
        This interactive story map explores various aspects of Toronto's urban landscape, providing insights and data to help you understand the city's unique characteristics.
      </div>
      <button class="close-button" on:click={onClose}>Enter</button>
  
      <!-- Logo Link to mapTO -->
      <div class="logo">
        <a href="https://www.mapto.ca" target="_blank">
          <img src="/Logo_orange_2024_bolder.png" alt="mapTO logo" />
        </a>
      </div>
    </div>
  </div> 
  