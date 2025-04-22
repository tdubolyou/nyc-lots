<script>
  export let onClose; // Function to close or hide the splash
</script>

<style>
  .splash {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: left;
    justify-content: left;
    background: url('/splash_bg.png') center/cover no-repeat;
    z-index: 1000;
    color: white;
    text-align: center;
    padding: 2rem;
  }

  .overlay {
    background: rgba(0, 0, 0, 0.6);
    padding: 2rem;
    border-radius: 8px;
    max-width: 600px;
  }

  .title {
    font-family: 'Barlow', sans-serif;
    font-size: 2.5rem;
    font-weight: 900;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }

  .subtitle {
    font-size: 1.4rem;
    font-weight: 500;
    margin-bottom: 1rem;
    color: lightgrey;
  }

  .byline {
    font-size: 1rem;
    margin-bottom: 2rem;
  }

  .enter-button {
    background: #FF5A30;
    color: white;
    font-size: 1.25rem;
    font-weight: 700;
    padding: 0.75rem 2rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.2s ease-in-out;
  }

  .enter-button:hover {
    background: #e85428;
  }
</style>

<div class="splash">
  <div class="overlay">
    <div class="title">The Parking Lots of NYC</div>
    <div class="subtitle">How Many Lots Could Be Built On Surface Lots Near Transit?</div>
    <div class="byline">By: Tom Weatherburn</div>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque fermentum commodo neque, at bibendum massa blandit a.
      Vivamus sed aliquam velit. Sed eget justo et diam fermentum scelerisque quis a nibh.
    </p>
    <p>
      Fusce at augue ac nisl viverra tempus. Suspendisse in sagittis libero. Integer in leo justo. Vestibulum in tristique neque.
      Praesent tincidunt consectetur feugiat.
    </p>
    <p>
      Curabitur fermentum nunc a diam pharetra, at sodales turpis aliquet. Integer iaculis odio ac leo pellentesque, sed accumsan
      ipsum efficitur. Donec sit amet odio nec nulla semper vehicula.
    </p>
    <button class="enter-button" on:click={() => onClose()}>Enter Map</button>
  </div>
</div>
