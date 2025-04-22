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
    /* align-items: center; */
    justify-content: center;
    background: none;
    z-index: 1000;
    text-align: center;
    padding: 3rem;
    font-family: 'Barlow';
    /* overflow-y: auto; */
  }

  .background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('/splash_bg.png') center/cover no-repeat;
    opacity: 0.3; /* Faded background effect */
    z-index: -1;
  }

  .overlay {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    max-width: 600px;
    z-index: 1;
    max-height: 90vh; /* Restrict height to enable scrolling */
    overflow-y: auto; /* Enable scrolling when content overflows */
    text-align: left; /* Justify content inside the div to the left */
  }

  .title {
    font-family: 'Barlow', sans-serif;
    font-size: 4rem;
    font-weight: 900;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    font-style:italic;
    line-height: 3.5rem;
  }

  .subtitle {
    font-size: 1.2rem;
    font-weight: 200;
    margin-bottom: 1rem;
    color: rgb(69, 69, 69);
  }

  .byline {
    font-size: 0.8rem;
    margin-bottom: 2rem;
    font-weight: 100;
  }

  .byline a {
    color: #FF5A30;
    text-decoration: none;
    font-weight: 100;
  }

  .byline a:hover {
    text-decoration: underline;
  }

  .image-container {
    position: relative;
    width: 100%;
    max-width: 600px;
    margin: 0 auto 1.5rem auto;
    border-radius: 4px;
    overflow: hidden;
  }

  .image-container img {
    display: block;
    width: 100%;
    height: auto;
  }

  .enter-button {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #FF5A30;
    color: white;
    font-size: 1.25rem;
    font-weight: 700;
    padding: 0.75rem 2rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.2s ease-in-out;
    z-index: 10;
  }

  .enter-button:hover {
    background: #e85428;
  }
  p {
    font-family: Georgia, 'Times New Roman', Times, serif;
    padding: 0.5rem;
  }
</style>

{#if onClose}
  <div class="splash">
    <div class="background"></div>
    <div class="overlay">
      <div class="title">The Parking Lots of NYC</div>
      <div class="subtitle">How Much Housing Could Be Built On Surface Lots Near Transit?</div>
      <div class="byline">By: <a href="https://tomweatherburn.com" target="_blank">Tom Weatherburn</a></div>
      
      <div class="image-container">
        <img src="/splash_img.jpg" alt="Splash Image" />
        <button class="enter-button" on:click={onClose}>ENTER MAP</button>
      </div>
      
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

        Laboris minim reprehenderit magna eu voluptate non id elit ipsum. Eu fugiat laboris irure ad aute nostrud velit amet anim anim. Ullamco exercitation aliqua dolore ullamco ea. Tempor quis minim ea aliquip. Dolor veniam sit do commodo fugiat consectetur magna officia. Amet reprehenderit velit aliqua non minim dolore sint duis in.

        Est nulla exercitation enim elit dolor. Labore laborum elit commodo eiusmod pariatur non dolor fugiat consectetur in velit do minim. Veniam adipisicing in ea laboris est.

        Eu elit nulla ex fugiat deserunt excepteur labore nostrud ad. Consectetur nulla Lorem reprehenderit adipisicing dolore id dolore sit veniam ex aliqua irure qui. Consequat aliquip laboris sint laboris reprehenderit reprehenderit id magna consectetur laborum ad velit Lorem duis. Laborum sint est quis exercitation non magna sint Lorem labore occaecat esse sint dolor.

        Incididunt adipisicing eiusmod do quis qui sit. Nulla nostrud esse aliquip aute est nostrud commodo eu qui eiusmod ad. Ipsum non fugiat aute dolore. Anim veniam sunt eu ea enim aliquip qui elit adipisicing. Id consequat amet sint reprehenderit quis. Anim ea Lorem consectetur est cupidatat aute laborum do cupidatat.
        </p>
    </div>
  </div>
{/if}
