<script>
  export let onClose; // Function to close or hide the splash
  import { onMount } from 'svelte';
  let scrolled = false;
  let overlayEl;

  function handleScroll() {
    if (overlayEl && overlayEl.scrollTop > 10) {
      scrolled = true;
    } else {
      scrolled = false;
    }
  }

  onMount(() => {
    if (overlayEl) {
      overlayEl.addEventListener('scroll', handleScroll);
    }
    return () => {
      if (overlayEl) {
        overlayEl.removeEventListener('scroll', handleScroll);
      }
    };
  });
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
    max-width: 650px;
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
  .down-arrow {
    position: absolute;
    left: 50%;
    bottom: 4rem;
    transform: translateX(-50%);
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 0.85;
    animation: bounce 1.5s infinite;
    z-index: 10;
    pointer-events: none;
    background: rgba(255,255,255,0.7);
    border-radius: 1.5rem;
    padding: 0.25rem 0.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    transition: opacity 0.4s;
  }
  .down-arrow.fadeout {
    opacity: 0;
    transition: opacity 0.4s;
  }
  @keyframes bounce {
    0%, 100% { transform: translateY(0);}
    50% { transform: translateY(10px);}
  }
</style>

{#if onClose}
  <div class="splash">
    <div class="background"></div>
    <div class="overlay" bind:this={overlayEl}>
      <div class="title">The Parking Lots of NYC</div>
      <div class="subtitle">How Much Housing Could Be Built On Surface Lots Near Transit?</div>
      <div class="byline">By: <a href="https://tomweatherburn.com" target="_blank">Tom Weatherburn</a></div>
      

      
      <p>
        New York City is in the grip of a deepening housing crisis. With rents at record highs—climbing over 30% in some neighborhoods since 2020 (NY Times, 2024)—and a near-record low vacancy rate of just 1.4% (NY Times, 2024), the city is struggling to keep up with demand. Despite adding between 12,000 and 30,000 units annually over the past decade (NYC Comptroller, 2023), this growth lags behind population needs, especially in transit-accessible areas. Meanwhile, vast swaths of land, often just steps from subway stations, remain locked up in surface parking lots—remnants of outdated zoning laws and a car-first mindset that no longer fits the reality of 21st-century urban life. What if we reimagined these spaces? What if, instead of housing cars, they housed people?
      </p>

      <p>
        In this analysis, we map and quantify the city’s surface parking lots, focusing on those within an 800-meter radius of MTA stations—the areas best suited for new housing. By overlaying land use data from PLUTO and the city’s open data portal with transit accessibility, we estimate the number of potential housing units that could replace these underutilized lots. The total housing stock in NYC was approximately 3,705,000 units in 2023 (NYC Comptroller, 2023), yet demand continues to outpace supply. The results of our analysis are striking: converting even a fraction of these sites could add tens of thousands of homes, potentially filling a significant portion of the city’s housing gap. Would this be a silver bullet for affordability? No—but every additional unit helps ease pressure on the market, and placing new housing near transit aligns with the broader goals of sustainability and livability.
      </p>
      <p>  
        The question is no longer whether we should rethink these spaces, but how quickly we can act. Surface parking may have once been a necessary urban fixture, but in a city where land is as precious as gold, the logic no longer holds. Housing near transit lowers carbon emissions, reduces commuting costs, and fosters more walkable, vibrant neighborhoods. Other global cities have already taken bold steps in this direction—NYC risks falling behind. If we are serious about tackling the housing crisis, it’s time to challenge the assumption that parking deserves a premium spot in our urban fabric.
      </p>
      <div class="image-container">
        <img src="/splash_img.jpg" alt="Splash Image" />
        <button class="enter-button" on:click={onClose}>ENTER MAP</button>
      </div>
    </div>
    <div class="down-arrow" class:fadeout={scrolled}>
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#FF5A30" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-down">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </div>
  </div>
{/if}
