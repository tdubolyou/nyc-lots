<script>
  import { slide } from 'svelte/transition';
  import BoroChart from './BoroChart.svelte';
  import LotSizeChart from './LotSize.svelte';
  import LotScatterChart from './LotScatter.svelte';
  import DevLine from './DevLine.svelte'
  
  export let flyTo; // Function passed in from the parent component to handle map flyTo

  let sidebarVisible = true;

  // Map block component names to Svelte components.
  const componentMap = {
    BoroChart: BoroChart,
    LotSizeChart: LotSizeChart,
    LotScatterChart: LotScatterChart,
    DevLine: DevLine
    // Add additional chart/component mappings here if needed.
  };

  // Each section now has a content array of blocks.
  let sections = [
    { 
      title: "How many surface lots are there in NYC?", 
      content: [
        { type: "text", value: "There are a lot. I narrowed it down to lots within 800m of MTA stations that were in both the PLUTO database and the City' parking lot data. Across all 5 boroughs I identified 2,222 parking lots. The breakdown by borough is as shown below."},
        { type: "chart", component: "BoroChart" },
      ],
      coordinates: [-74.1009, 40.7000],
      zoomLevel: 9.9,
      isCollapsed: true,
      layerOn: ['heatmap', 'lots_par_fill', 'lots_par_outline', 'lots_par'],
      layerOff: ['dev_pts_heatmap', 'dev_par_fill'],
      legend: {
        title: "Parking Lot Area (m²)",
        gradient: "parking-gradient",
        labels: ["0", "250", "500", "750", "1000+"]
      }
    },
    { 
      title: "How big are they?", 
      content: [
        { type: "text", value: "There is a big spread.  There are 7 sites over 10 HA, there are tons of smaller lots.  The chart below shows the average size of the lots and the total area of the lots by borough.  We can see that Brooklyn has the largest area as well as a relatively small average size, pointing to many smaller lots while Quees has a much alarger share of large lots." },
        { type: "chart", component: "LotScatterChart" }      
      ],
      coordinates: [-73.9427, 40.6544],
      zoomLevel: 11.3,
      isCollapsed: true,
      layerOn: ['heatmap', 'lots_par_fill', 'lots_par_outline', 'lots_par'],
      layerOff: ['dev_pts_heatmap', 'dev_par_fill'],
      legend: {
        title: "Parking Lot Area (m²)",
        gradient: "parking-gradient",
        labels: ["0", "250", "500", "750", "1000+"]
      }
    },
    { 
      title: "What typically gets built in each borough?", 
      content: [
        { type: "text", value: "I looked at development within the same catchment that was built within the last 10 years, according to PLUTO. Clearly the highest density borough is Manhattan. Despite lower densities in 2017-19,the average desity has been increasong slightly and sits in the mid 70s (units/ha). Staten Island has the lowest average density and it has been arouns 4.5 units/ha over the 10 year period. While recent development in the bronx has been lower density, there is an overall increasing trend. The average over 10 years is 31 units/ha.  In Brooklyn densities have increased significantly in recent years, up to 60 units/ha in 2023. the average over the 10 year period is 41." },
        { type: "chart", component: "DevLine" }  
      ],
      coordinates: [-73.9938, 40.7512],
      zoomLevel: 13.32, 
      isCollapsed: true,
      layerOn: ['dev_pts_heatmap', 'dev_par_fill'],
      layerOff: ['heatmap', 'lots_par_fill', 'lots_par_outline', 'lots_par'],
      legend: {
        title: "Recent Development Density (units/ha)",
        gradient: "development-gradient",
        labels: ["0", "25", "50", "75", "100+"]
      }
    },
    { 
      title: "Whats the housing potential of these lots?", 
      content: [
        { type: "text", value: "Applying historic density tot he area of the parking lots, gives a sense of the housing potential of these surface lots. Doign so yielded a total of:" },
        { type: "text", value: "62,528", style: "highlight-number" },
        { type: "text", value: "Given new untis have ranged from 12K to 30k in recent years, this represents between 2 and 5 years of new supply. If one were to apply the average densityof the last 3 years, we would see significantly increased yields, up to ~100k units." }
      ],
      coordinates: [-74.1009, 40.7000],
      zoomLevel: 9.9,
      isCollapsed: true,
      layerOn: ['heatmap', 'lots_par_fill', 'lots_par_outline', 'lots_par'],
      layerOff: ['dev_pts_heatmap', 'dev_par_fill'],
      legend: {
        title: "Parking Lot Area (m²)",
        gradient: "parking-gradient",
        labels: ["0", "250", "500", "750", "1000+"]
      }
    }
  ];
    
  let currentSectionIndex = 0;

  function closeSidebar() {
    sidebarVisible = false;
  }
  
  function openSidebar() {
    sidebarVisible = true;
  }
  
  function navigateToSection(index) {
    // Ensure index is within bounds
    if (index < 0) index = sections.length - 1;
    if (index >= sections.length) index = 0;
    
    // Close all sections first
    sections = sections.map(section => ({ ...section, isCollapsed: true }));
    
    // Open the target section
    sections[index].isCollapsed = false;
    
    // Update current index
    currentSectionIndex = index;
    
    // Trigger the flyTo for the section
    flyTo(
      sections[index].coordinates,
      sections[index].zoomLevel,
      sections[index].layerOn || [],
      sections[index].layerOff || [],
      sections[index].legend
    );
  }

  function nextSection() {
    navigateToSection(currentSectionIndex + 1);
  }

  function previousSection() {
    navigateToSection(currentSectionIndex - 1);
  }

  // Update toggleCollapse to maintain currentSectionIndex
  function toggleCollapse(index) {
    sections = sections.map((section, i) => {
      if (i === index) {
        section.isCollapsed = !section.isCollapsed;
        if (!section.isCollapsed) {
          currentSectionIndex = index;
          flyTo(
            section.coordinates,
            section.zoomLevel,
            section.layerOn || [],
            section.layerOff || [],
            section.legend
          );
        }
      } else {
        section.isCollapsed = true;
      }
      return section;
    });
  }
</script>

<style>
  .sidebar {
    background: #ffffff;
    border-right: 1px solid #e5e5e5;
    height: 100vh;
    width: 500px;
    position: fixed;
    left: 0;
    top: 0;
    transition: transform 0.4s ease;
    font-family: 'Barlow', sans-serif;
    color: #333;
    z-index: 999;
    display: flex;
    flex-direction: column;
  }
  
  .sidebar-content {
    padding: 1rem;
    overflow-y: auto;
    flex-grow: 1;
    padding-bottom: 0;
  }
  
  .sidebar-hidden {
    transform: translateX(-100%);
  }
  
  .section-header {
    color: #000;
    cursor: pointer;
    font-weight: 900;
    margin: 0.5rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem;
    border-radius: 4px;
    transition: background-color 0.2s ease;
  }
  
  .section-header:hover {
    background-color: rgba(0, 0, 0, 0.05);
  }
  
  header h1, header h2, header p {
    color: #000;
    margin: 0;
  }
  
  header h1 {
    font-size: 2rem;
    font-weight: 900;
    font-style: italic;
  }
  
  header h2 {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }
  
  header p {
    font-size: 0.85rem;
    color: #555;
    margin-bottom: 1rem;
  }
  
  a {
    color: #FF5A30;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  .collapse-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: 1.2rem;
    color: #555;
    padding: 8px;
    border-radius: 50%;
    transition: background-color 0.2s ease;
  }
  
  .collapse-button:hover {
    background-color: rgba(0, 0, 0, 0.05);
  }
  
  .open-button {
    position: fixed;
    z-index: 1000;
    top: 20px;
    left: 20px;
    background: #FF5A30;
    border: none;
    cursor: pointer;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    color: #fff;
    font-size: 1.2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease;
  }
  
  .open-button:hover {
    transform: scale(1.05);
  }
  
  .chevron-icon {
    display: inline-block;
    margin-left: 0.5rem;
    vertical-align: middle;
    transition: transform 0.4s ease;
  }
  
  /* Mobile Responsive Styles */
  @media (max-width: 768px) {
    .sidebar {
      position: fixed;
      top: auto;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 40vh;
      border-right: none;
      border-top: 1px solid #e5e5e5;
      transform: translateY(100%);
    }

    .sidebar:not(.sidebar-hidden) {
      transform: translateY(0);
    }

    .sidebar-hidden {
      transform: translateY(100%);
    }

    .open-button {
      top: auto;
      bottom: 20px;
      left: 20px;
    }

    header h1 {
      font-size: 1.25rem;
    }

    header h2 {
      font-size: 0.9rem;
    }

    .section-header {
      font-size: 0.9rem;
      padding: 0.75rem;
    }
  }
  
  /* Small Mobile Devices */
  @media (max-width: 480px) {
    .sidebar {
      height: 50vh;
    }

    header h1 {
      font-size: 1.1rem;
    }

    .section-header {
      font-size: 0.85rem;
    }
  }
  
  .navigation-buttons {
    display: flex;
    justify-content: space-between;
    padding: 1rem;
    border-bottom: 1px solid #e5e5e5;
    border-top: 1px solid #e5e5e5;
    background: #ffffff;
    position: sticky;
    bottom: 0;
    margin-top: auto;
    
  }

  .nav-button {
    background: #888382FF;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
    transition: background-color 0.2s ease;
    flex: 1;
    margin: 0 0.5rem;
  }

  .nav-button:first-child {
    margin-left: 0;
  }

  .nav-button:last-child {
    margin-right: 0;
  }

  .nav-button:hover {
    background: #e54a20;
  }

  .nav-button:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
  
  .introduction {
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-size: 16px;
    padding: 0.5rem;
    margin-bottom: 1rem;
    line-height: 1.6;
  }
  
  .section p {
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-size: 16px;
    padding: 0.5rem;
    line-height: 1.6;
  }
  
  /* Style for highlighted numbers */
  .section p.highlight-number {
    font-family: 'Barlow', sans-serif;
    font-size: 88px;
    font-weight: bold;
    color: #008080; /* Teal color */
    text-align: center;
    margin: 1rem 0;
    padding: 0.5rem;
  }
</style>

<!-- Sidebar Container -->
<div class="sidebar {sidebarVisible ? '' : 'sidebar-hidden'}" aria-hidden={!sidebarVisible}>
  <!-- Collapse Button -->
  <button class="collapse-button" on:click={closeSidebar} aria-label="Close sidebar">×</button>
  
  <div class="sidebar-content">
    <!-- Header Section -->
    <header>
      <h1>How much housing could be built on the parking lots of NYC?</h1>
      <h2>A lot, actually</h2>
      <p>By: <a href="https://www.tomweatherburn.com/" target="_blank">Tom Weatherburn</a></p>
      <p class="introduction">
        This analysis explores the potential for housing development on surface parking lots near transit stations across New York City. By examining lot sizes, locations, and development patterns, we can estimate how many new housing units could be created in these underutilized spaces.
      </p>
    </header>

    <!-- Render each section -->
    {#each sections as section, index}
      <div class="section">
        <h3 class="section-header" on:click={() => toggleCollapse(index)} aria-expanded={!section.isCollapsed}>
          <span>{section.title}</span>
          <span class="chevron-icon">
            {#if section.isCollapsed}
              <!-- Down chevron -->
              <svg width="12" height="12" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 3L5 7L9 3" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            {:else}
              <!-- Up chevron -->
              <svg width="12" height="12" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 7L5 3L9 7" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            {/if}
          </span>
        </h3>
        {#if !section.isCollapsed}
          <div transition:slide={{ duration: 500 }}>
            {#each section.content as block}
              {#if block.type === 'text'}
                <p class={block.style || ''}>{block.value}</p>
              {:else if block.type === 'chart'}
                <div class="chart-container">
                  <svelte:component this={componentMap[block.component]} />
                </div>
              {/if}
            {/each}
          </div>
        {/if}
      </div>
    {/each}
  </div>
  
  <!-- Navigation Buttons -->
  <div class="navigation-buttons">
    <button class="nav-button" on:click={previousSection} aria-label="Previous section">
      ← Previous
    </button>
    <button class="nav-button" on:click={nextSection} aria-label="Next section">
      Next →
    </button>
  </div>
</div>

<!-- Open Sidebar Button (Visible when Sidebar is hidden) -->
{#if !sidebarVisible}
  <button class="open-button" on:click={openSidebar} aria-label="Open sidebar">i</button>
{/if}