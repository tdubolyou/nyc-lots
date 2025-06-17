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
        { type: "text", value: "There are a lot. Across all 5 boroughs I identified 2,222 parking lots. The breakdown by borough is as shown below. Spatially, they are generally distributed around the outsides of the subway network. Let's have a look."},
        { type: "chart", component: "BoroChart" },
        { type: "text", value:  "I narrowed it down to lots within 800m of subway stations that were in both the PLUTO database and the City of NYC mapping. Having said that it's not as many as I might have guessed." }
      ],
      coordinates: [-74.1009, 40.7000],
      zoomLevel: 9.9,
      isCollapsed: false,
      layerOn: [],
      layerOff: []
    },
    { 
      title: "How big are they?", 
      content: [
        { type: "text", value: "Sint voluptate id sunt est sint. Sint elit pariatur deserunt nisi duis culpa amet tempor magna quis. In dolore laboris voluptate ad excepteur velit ex velit minim occaecat in cillum. Ut et anim nisi tempor nostrud adipisicing.  Dolor deserunt consectetur dolore eu sunt duis ex sit eiusmod commodo reprehenderit adipisicing minim. Ex proident fugiat culpa quis proident eu magna cillum aliquip deserunt amet pariatur consectetur. Do ullamco aliquip sunt occaecat velit sunt culpa velit enim eu adipisicing.  Dolore exercitation sunt sunt excepteur proident irure. Incididunt velit nostrud Lorem exercitation dolor non amet. Sit nisi tempor ea exercitation velit minim quis deserunt id velit. Incididunt enim tempor laboris mollit sunt sit nisi eu id. Duis veniam dolor nisi dolor exercitation sint cupidatat laborum et nostrud. Dolor consectetur eiusmod excepteur cillum consequat. Enim consectetur fugiat amet Lorem labore." },
        { type: "chart", component: "LotScatterChart" }      
      ],
      coordinates: [-73.856077, 40.848447],
      zoomLevel: 16,
      isCollapsed: true,
      layerOn: [],
      layerOff: []
    },
    { 
      title: "What typically gets built in each borough?", 
      content: [
        { type: "text", value: "Analysis of the map data." },
        { type: "chart", component: "DevLine" }  
      ],
      coordinates: [-73.856077, 40.848447],
      zoomLevel: 15, 
      isCollapsed: true,
      layerOn: ['dev_par_fill'],
      layerOff: ['heatmap', 'lots_par_fill', 'lots_par_outline', 'lots_par']
    },
    { 
      title: "Whats the housing potential of these lots?", 
      content: [
        { type: "text", value: "Final thoughts and conclusions." }
      ],
      coordinates: [-73.856077, 40.848447],
      zoomLevel: 13,
      isCollapsed: true,
      layerOn: ['heatmap', 'lots_par_fill'],
      layerOff: []
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
      sections[index].layerOff || []
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
            section.layerOff || []
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
    width: 400px;
    position: fixed;
    left: 0;
    top: 0;
    transition: transform 0.4s ease;
    font-family: 'Barlow', sans-serif;
    color: #333;
    z-index: 999;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }
  
  .sidebar-content {
    padding: 1rem;
    overflow-y: auto;
    flex-grow: 1;
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
    padding: 1rem 0;
    margin-bottom: 1rem;
    border-bottom: 1px solid #e5e5e5;
    
  }

  .nav-button {
    background: #FF5A30;
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
    </header>

    <!-- Navigation Buttons -->
    <div class="navigation-buttons">
      <button class="nav-button" on:click={previousSection} aria-label="Previous section">
        ← Previous
      </button>
      <button class="nav-button" on:click={nextSection} aria-label="Next section">
        Next →
      </button>
    </div>
    
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
                <p>{block.value}</p>
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
</div>

<!-- Open Sidebar Button (Visible when Sidebar is hidden) -->
{#if !sidebarVisible}
  <button class="open-button" on:click={openSidebar} aria-label="Open sidebar">i</button>
{/if}