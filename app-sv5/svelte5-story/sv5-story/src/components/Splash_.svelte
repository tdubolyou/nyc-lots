<script>
  export let onClose; // Function to close or hide the splash
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import { base } from '$app/paths';
  let scrolled = false;
  let overlayEl;
  
  // Detect mobile devices immediately if in browser
  let isMobile = browser ? window.innerWidth <= 768 : false;

  function handleScroll() {
    if (overlayEl && overlayEl.scrollTop > 10) {
      scrolled = true;
    } else {
      scrolled = false;
    }
  }

  // Function to scroll overlay to the bottom
  function scrollToBottom() {
    if (overlayEl) {
      overlayEl.scrollTo({
        top: overlayEl.scrollHeight,
        behavior: 'smooth'
      });
    }
  }

  onMount(() => {
    // Re-check on mount in case window was resized (though unlikely for splash)
    if (browser) {
      isMobile = window.innerWidth <= 768;
    }
    
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
    /* height: 100vh; */
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

  h1.title {
    font-family: 'Barlow', sans-serif;
    font-size: 4rem;
    font-weight: 900;
    text-transform: uppercase;
    margin: 0 0 0.5rem 0;
    font-style: italic;
    line-height: 3.5rem;
  }

  h2.subtitle {
    font-size: 1.2rem;
    font-weight: 200;
    margin: 0 0 1rem 0;
    color: rgb(69, 69, 69);
  }

  p.byline {
    font-size: 0.8rem;
    margin-bottom: 1rem;
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

  .enter-button:focus-visible {
    outline: 2px solid #008080;
    outline-offset: 2px;
  }

  /* Screen reader only class */
  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
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
    pointer-events: auto; /* Enable pointer events for click */
    background: rgba(255,255,255,0.7);
    border-radius: 1.5rem;
    padding: 0.25rem 0.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    transition: opacity 0.4s;
    cursor: pointer; /* Show pointer cursor on hover */
  }
  .down-arrow.fadeout {
    opacity: 0;
    transition: opacity 0.4s;
  }
  @keyframes bounce {
    0%, 100% { transform: translateY(0);}
    50% { transform: translateY(10px);}
  }

  .mobile-notice {
    background: #f0f7f7;
    border-left: 4px solid #008080;
    padding: 1rem;
    margin-top: 0;
    border-radius: 4px;
  }

  .mobile-notice p {
    margin: 0;
    font-style: italic;
    color: #555;
  }

  /* Tablet */
  @media (max-width: 768px) {
    .splash {
      padding: 1.5rem;
    }

    .overlay {
      padding: 1.5rem;
      max-width: 90vw;
      max-height: 85vh;
    }

    h1.title {
      font-size: 2.5rem;
      line-height: 2.2rem;
    }

    h2.subtitle {
      font-size: 1rem;
    }

    p {
      font-size: 14px;
    }
  }

  /* Small Mobile */
  @media (max-width: 480px) {
    .splash {
      padding: 1rem;
    }

    .overlay {
      padding: 1rem;
      max-height: 90vh;
    }

    h1.title {
      font-size: 1.8rem;
      line-height: 1.7rem;
    }

    h2.subtitle {
      font-size: 0.9rem;
    }

    p {
      font-size: 13px;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
</style>

{#if onClose}
  <div class="splash">
    <div class="background"></div>
    <div class="overlay" bind:this={overlayEl} role="dialog" aria-labelledby="splash-title">
      <h1 id="splash-title" class="title">The Parking Lots of NYC</h1>
      <h2 class="subtitle">How Much Housing Could Fit On Transit-Oriented Surface Parking Lots?</h2>
      <p class="byline">By: <a href="https://tomweatherburn.com" target="_blank" rel="noopener noreferrer">Tom Weatherburn<span class="visually-hidden"> (opens in new tab)</span></a></p>
      

      <div class="image-container">
        <img src="{base}/splash_img.jpg" alt="Aerial view of a surface parking lot in New York City near transit" />
        {#if !isMobile}
          <button class="enter-button" on:click={onClose}>ENTER MAP</button>
        {/if}
      </div>
      
      {#if isMobile}
        <div class="mobile-notice">
          <p>This interactive map experience is best viewed on a desktop or laptop computer. Please visit us on a larger screen to explore the full map and data visualizations.</p>
        </div>
      {/if}
      
      <p>
        New York City is in the grip of a deepening housing crisis. With rents at record highs and a near-record low vacancy rate, the city is struggling to keep up with housing demand. Meanwhile, vast swaths of land, often just steps from subway stations, remain locked up in surface parking lots.
      </p>
      
      <p>
        We mapped the city's surface parking lots, within 800-meters of MTA stations, areas potentially well suited for new housing and estimate the number of potential housing units that could replace these lots. Although not an exahustive site-level evaluation, we find converting even some of these sites could add tens of thousands of homes, potentially filling a portion of the city's housing gap.
      </p>
      
      
      
    </div>
    <!-- <div class="down-arrow" class:fadeout={scrolled} on:click={scrollToBottom}>
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#FF5A30" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-down">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </div> -->
  </div>
{/if}
