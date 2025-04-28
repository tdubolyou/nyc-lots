<script>
  import { slide } from 'svelte/transition';
  import BoroChart from './BoroChart.svelte';
  import LotSizeChart from './LotSize.svelte';
  import LotScatterChart from './LotScatter.svelte';
  
  export let flyTo; // Function passed in from the parent component to handle map flyTo

  let sidebarVisible = true;

  // Map block component names to Svelte components.
  const componentMap = {
    BoroChart: BoroChart,
    LotSizeChart: LotSizeChart,
    LotScatterChart: LotScatterChart
    // Add additional chart/component mappings here if needed.
  };

  // Each section now has a content array of blocks.
  let sections = [
    { 
      title: "How many surface lots are there in NYC?", 
      content: [
        { type: "text", value: "There are a lot. I narrowed it down to lots within 800m of subway stations that were in both the PLUTO database and the City of NYC mapping. Having said that it's not as many as I might have thought. Let's have a look." },
        { type: "chart", component: "BoroChart" },
        { type: "text", value: "Across all 5 boroughs there are XXX parking lots. The breakdown by borough is as shown below. XX has the most, and XX has the least. Spatially, they are generally distributed around the outsides of the subway network." }
      ],
      coordinates: [-73.856077, 40.848447],
      zoomLevel: 14,
      isCollapsed: true,
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
        { type: "text", value: "Analysis of the map data." }
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
    
  function closeSidebar() {
    sidebarVisible = false;
  }
  
  function openSidebar() {
    sidebarVisible = true;
  }
  
  // Toggle the selected section and collapse others.
  function toggleCollapse(index) {
    sections = sections.map((section, i) => {
      if (i === index) {
        section.isCollapsed = !section.isCollapsed;
        if (!section.isCollapsed) {
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
    padding: 1rem;
    height: 100vh;
    width: 400px;
    position: absolute;
    left: 0;
    transition: transform 0.4s ease;
    font-family: 'Barlow', sans-serif;
    color: #333;
    z-index: 999;
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
  }
  
  .section-header:hover {
    text-decoration: underline;
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
  }
  
  .open-button {
    position: absolute;
    z-index: 1000;
    top: 10px;
    left: 10px;
    background: #FF5A30;
    border: none;
    cursor: pointer;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    color: #fff;
    font-size: 1.2rem;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .chevron-icon {
    display: inline-block;
    margin-left: 0.5rem;
    vertical-align: middle;
    transition: transform 0.4s ease;
  }
</style>

<!-- Sidebar Container -->
<div class="sidebar {sidebarVisible ? '' : 'sidebar-hidden'}" aria-hidden={!sidebarVisible}>
  <!-- Collapse Button -->
  <button class="collapse-button" on:click={closeSidebar} aria-label="Close sidebar">×</button>
  
  <!-- Header Section -->
  <header>
    <h1>How much housing could be built on the parking lots of NYC?</h1>
    <h2>A lot, actually</h2>
    <p>By: <a href="https://www.tomweatherburn.com/" target="_blank">Tom Weatherburn</a></p>
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

<!-- Open Sidebar Button (Visible when Sidebar is hidden) -->
{#if !sidebarVisible}
  <button class="open-button" on:click={openSidebar} aria-label="Open sidebar">i</button>
{/if}