<script>
  import { slide } from 'svelte/transition';
  import { tick } from 'svelte';
  import BoroChart from './BoroChart.svelte';
  import LotSizeChart from './LotSize.svelte';
  import LotScatterChart from './LotScatter.svelte';
  import DevLine from './DevLine.svelte'
  
  export let flyTo; // Function passed in from the parent component to handle map flyTo

  let sidebarVisible = true;

  let sidebarContentRef;
  let mainHeaderRef;
  let sectionHeaderRefs = [];
  let scrollPosition = 0;

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
      title: "How Many Transit-Oriented Surface Parking Lots are in NYC?", 
      content: [
        { type: "text", value: "There are 2,222 surface parking parcels that sit within walking distance of MTA stations.  "},
        { type: "text", value: "2,222", style: "highlight-number" },
        { type: "text", value: "Parking Lots", style: "highlight-subtitle" },
        { type: "text", value: "Brooklyn contains the largest share with 786. Staten Island has the fewest, 108, though many of its sites are significantly larger.  Manhattan contains 301 lots, about a third of which are below Central Park."}, 
        { type: "chart", component: "BoroChart" },
        
      ],
      coordinates: [-74.1009, 40.7000],
      zoomLevel: 9.9,
      isCollapsed: true,
      layerOn: ['heatmap', 'lots_par_fill', 'lots_par_outline', 'lots_par'],
      layerOff: ['lots_units', 'dev_pts_heatmap', 'dev_par_fill', 'dev_par_outline', 'boro-labels', 'boro-unit-labels', 'lots_units_faded'],
      legend: {
        title: "Parking Lot Area (hectares)",
        gradient: "parking-gradient",
        labels: ["0", "0.4", "0.8", "1.2", "1.6+"]
      }
    },
    { 
      title: "Whats the Total Footprint of These Parking Lots?", 
      content: [
         
      { type: "text", value: "Together, the city’s surface lots occupy just over 150 hectares - roughly half of Central Park, or more than thirteen Hudson Yards. " },
      { type: "chart", component: "LotScatterChart" },  
      { type: "text", value: "The pattern varies by borough.  The map shows an example of how this variation looks in Brooklyn, which has the most land overall at 50 hectares, but the smallest average size. By contrast, Staten Island, with lower total area at just over 10 hectares, holds disproportionately large sites, a mix of park-n-ride lots and large commercial parking." }
      ],
      coordinates: [-73.9932, 40.6748],
      zoomLevel: 15,
      isCollapsed: true,
      layerOn: ['heatmap', 'lots_par_fill', 'lots_par_outline', 'lots_par'],
      layerOff: ['lots_units_faded','dev_pts_heatmap', 'dev_par_fill', 'dev_par_outline', 'boro-labels', 'boro-unit-labels'],
      legend: {
        title: "Parking Lot Area (hectares)",
        gradient: "parking-gradient",
        labels: ["0", "0.4", "0.8", "1.2", "1.6+"]
      }
    },
    
    { 
      title: "Parcel Fragmentation and Redevelopment Constraints", 
      content: [
        { type: "text", value: "There some obvious reasons many of these sites have not been redeveloped already.  Many surface lots consist of multiple small, separately owned parcels, each with different configurations, reflecting historical structures and incremental change. This fragmentation makes redevelopment potential more complicated and often expensive, potentially keeping parking as the most stable, low-risk use." },
             
      ],
      coordinates: [-73.9934, 40.7271],
      zoomLevel: 18.90,
      isCollapsed: true,
      layerOn: ['heatmap', 'lots_par_fill', 'lots_par_outline', 'lots_par'],
      layerOff: ['dev_pts_heatmap', 'dev_par_fill', 'dev_par_outline', 'boro-labels', 'boro-unit-labels'],
      legend: {
        title: "Parking Lot Area (hectares)",
        gradient: "parking-gradient",
        labels: ["0", "0.4", "0.8", "1.2", "1.6+"]
      }
    },
    
    
    
    { 
      title: "What Typically Gets Built in Each Borough?", 
      content: [
        { type: "text", value: "A decade of project data illustrates how each borough typically builds. Manhattan sees the highest densities, driven by land values and zoning. The outer boroughs vary widely with Queens and Brooklyn showing an upward trajectory over time. These historic densities form the basis for estimating potential development outcomes on surface parking lots." },
        { type: "chart", component: "DevLine" }  
      ],
      coordinates: [-73.9938, 40.7512],
      zoomLevel: 13.32, 
      isCollapsed: true,
      layerOn: ['dev_pts_heatmap', 'dev_par_fill', 'dev_par_outline'],
      layerOff: ['heatmap', 'lots_par_fill', 'lots_par_outline', 'lots_par', 'boro-labels', 'boro-unit-labels'],
      legend: {
        title: "Recent Development Density (units/ha)",
        gradient: "development-gradient",
        labels: ["0", "25", "50", "75", "100+"]
      }
    },
    { 
      title: "Whats the housing potential of these lots?", 
      content: [
        { type: "text", value: "62,820", style: "highlight-number" },
        { type: "text", value: "Potential Housing Units", style: "highlight-subtitle" },
        { type: "text", value: "Suspending, for a minute, the potential financial and regulatory barriers to redevelopment, and applying recent development densities to land now used for surface parking yields an estimated 62,820 housing units." },
        { type: "text", value: "Given that New York has added 12,000–30,000 units per year in the last decade, these lots represent two to five years of new supply under today’s conditions. If we apply the higher densities of the last three years — reflecting a shift toward larger, more ambitious projects — capacity rises toward 100,000 units. " },
        { type: "text", value: "This is by no means a feasibility analysis.  Its simply to highlight that with regulatory change and finaincial incentives, there is physical space for significant housing on under-utilized, transit-oriented parking lots across NYC." }
      ],
      coordinates: [-74.1009, 40.7000],
      zoomLevel: 9.9,
      isCollapsed: true,
      layerOn: ['lots_units_faded', 'lots_par_fill', 'lots_par_outline', 'lots_par', 'boro-unit-labels'],
      layerOff: ['dev_pts_heatmap', 'dev_par_fill', 'dev_par_outline', 'heatmap', 'lots_units', 'boro-labels'],
      legend: {
        title: "Housing Potential (Units)",
        gradient: "units-faded-gradient",
        labels: ["0", "25", "50", "100", "200+"]
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

  function handleScroll(event) {
    scrollPosition = event.target.scrollTop;
  }
  
  function navigateToSection(index) {
    // Ensure index is within bounds
    if (index < 0) index = sections.length - 1;
    if (index >= sections.length) index = 0;
    
    sections = sections.map((section, i) => ({
      ...section,
      isCollapsed: i === index ? false : true
    }));

    currentSectionIndex = index;

    const targetSection = sections[index];
    flyTo(
      targetSection.coordinates,
      targetSection.zoomLevel,
      targetSection.layerOn || [],
      targetSection.layerOff || [],
      targetSection.legend
    );

    scrollToSection(index);
  }

  function nextSection() {
    // Check if all sections are collapsed
    const allCollapsed = sections.every(section => section.isCollapsed);
    if (allCollapsed) {
      navigateToSection(0); // Open the first section
    } else {
      navigateToSection(currentSectionIndex + 1);
    }
  }

  function previousSection() {
    navigateToSection(currentSectionIndex - 1);
  }

  // Update toggleCollapse to maintain currentSectionIndex
  function toggleCollapse(index) {
    const wasOpen = !sections[index].isCollapsed;
    
    // Toggle the clicked section, close all others
    sections = sections.map((section, i) => ({
      ...section,
      isCollapsed: i === index ? wasOpen : true
    }));

    // Update currentSectionIndex when a section is opened
    if (!wasOpen) {
      currentSectionIndex = index;
      
      // Only trigger flyTo and scroll when opening a section
      const targetSection = sections[index];
      flyTo(
        targetSection.coordinates,
        targetSection.zoomLevel,
        targetSection.layerOn || [],
        targetSection.layerOff || [],
        targetSection.legend
      );

      scrollToSection(index);
    }
  }

  // Simple scroll function - put the section header at the top of the viewport (below main header)
  function scrollToSection(index) {
    // Wait for the slide transition to fully complete before measuring positions
    setTimeout(() => {
      if (sidebarContentRef && sectionHeaderRefs[index]) {
        // Find the section header's absolute position in the scrollable content
        let sectionTop = 0;
        let el = sectionHeaderRefs[index];
        while (el && el !== sidebarContentRef) {
          sectionTop += el.offsetTop;
          el = el.offsetParent;
        }
        
        // The ideal scroll position is just the section's position
        // Add a buffer to ensure the header isn't cut off
        const idealScroll = sectionTop - 10;
        
        // Get the maximum possible scroll (total scrollable height minus visible height)
        const maxScroll = sidebarContentRef.scrollHeight - sidebarContentRef.clientHeight;
        
        // Use the smaller of idealScroll or maxScroll to handle small content
        const targetScroll = Math.min(Math.max(0, idealScroll), maxScroll);
        
        console.log('Section:', index, 'SectionTop:', sectionTop, 'IdealScroll:', idealScroll, 'MaxScroll:', maxScroll, 'TargetScroll:', targetScroll, 'Current scrollTop:', sidebarContentRef.scrollTop);
        
        sidebarContentRef.scrollTo({
          top: targetScroll,
          behavior: 'smooth'
        });
      }
    }, 520); // Wait for slide transition (500ms) + buffer for accurate measurements
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
    scroll-behavior: smooth;
    scroll-padding-top: 0;
  }
  
  .sidebar-hidden {
    transform: translateX(-100%);
  }
  
  .section-header {
    color: #000;
    font-weight: 500;
    margin: 0.5rem 0;
    transition: background-color 0.2s ease;
    font-size: 1.2rem;
    background: #ffffff;
  }

  .section-header-button {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    background: none;
    border: none;
    padding: 0.5rem;
    border-radius: 4px;
    font: inherit;
    color: inherit;
    cursor: pointer;
    text-align: left;
    font-weight: 500;
  }
  
  .section-header.selected .section-header-button {
    font-weight: 700;
  }

  .section-header-button:hover {
    background-color: #f8f9fa;
  }

  .section-header-button:active {
    background-color: #e9ecef;
  }

  .section-header-button:focus-visible {
    outline: 2px solid #008080;
    outline-offset: 2px;
  }

  .section-header.sticky {
    position: sticky;
    top: 0;
    z-index: 10;
    margin: 0;
    border-radius: 0;
  }

  .section-header.sticky .section-header-button {
    border-radius: 0;
  }

  .section.collapsed .section-header-button {
    font-weight: 500;
    color: #666;
    opacity: 0.9;
  }

  .section.collapsed .section-header-button:hover {
    color: #333;
    font-weight: 500;
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
    font-weight: 500;
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

  .collapse-button:focus-visible {
    outline: 2px solid #008080;
    outline-offset: 2px;
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

  .open-button:focus-visible {
    outline: 2px solid #008080;
    outline-offset: 2px;
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
      height: 45vh;
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
      bottom: 80px;
      left: 20px;
    }

    .collapse-button {
      top: 5px;
      right: 5px;
      padding: 6px;
      font-size: 1rem;
    }

    .bottom-nav-controls {
      padding: 0.5rem;
      gap: 6px;
    }

    .bottom-nav-button {
      width: 70px;
      height: 40px;
      min-width: 70px;
      min-height: 40px;
    }

    .progress-dot {
      width: 12px;
      height: 12px;
      min-width: 20px;
      min-height: 20px;
      padding: 4px;
      box-sizing: content-box;
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

    .section p {
      font-size: 14px;
      padding: 0.25rem 0.5rem;
    }

    .section p.highlight-number {
      font-size: 36px;
    }

    .section p.highlight-subtitle {
      font-size: 20px;
    }
  }
  
  /* Small Mobile Devices */
  @media (max-width: 480px) {
    .sidebar {
      height: 55vh;
    }

    header h1 {
      font-size: 1.1rem;
    }

    .section-header {
      font-size: 0.85rem;
    }

    .section p {
      font-size: 13px;
    }

    .section p.highlight-number {
      font-size: 28px;
    }

    .section p.highlight-subtitle {
      font-size: 18px;
    }
  }
  
  /* Bottom Navigation Controls */
  .bottom-nav-controls {
    position: sticky;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 0.75rem;
    background: #ffffff;
    border-top: 1px solid #e5e5e5;
    margin-top: auto;
    z-index: 10;
  }

  .bottom-nav-buttons {
    display: flex;
    flex-direction: row;
    gap: 8px;
    align-items: center;
  }

  .bottom-nav-button {
    background: #FF4500;
    border: none;
    border-radius: 8px;
    width: 150px;
    height: 40px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: background-color 0.2s ease;
    color: white;
    font-family: 'Barlow', sans-serif;
    font-size: 14px;
    font-weight: 500;
  }
  
  .bottom-nav-button span {
    color: white;
  }

  .bottom-nav-button:hover {
    background: #e54020;
  }

  .bottom-nav-button:active {
    background: #d63910;
  }

  .bottom-nav-button:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  .bottom-nav-button:focus-visible {
    outline: 2px solid #008080;
    outline-offset: 2px;
  }

  .progress-indicator {
    display: flex;
    flex-direction: row;
    gap: 8px;
    align-items: center;
    justify-content: center;
  }

  .progress-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    border: none;
    background: #d3d3d3;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .progress-dot.active {
    background: #FF4500;
  }

  .progress-dot:hover {
    background: #b0b0b0;
  }

  .progress-dot.active:hover {
    background: #e54020;
  }

  .progress-dot:focus-visible {
    outline: 2px solid #008080;
    outline-offset: 2px;
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }

  .scroll-indicator {
    position: fixed;
    bottom: 100px;
    left: 520px;
    background: rgba(0, 128, 128, 0.9);
    color: white;
    padding: 10px 15px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 14px;
    z-index: 10000;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
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
    font-size: 60px;
    font-weight: bold;
    color: #008080; /* Teal color */
    text-align: center;
    margin: 1rem 0 0rem 0;
    line-height: 1;
  }
  
  /* Style for highlight subtitles */
  .section p.highlight-subtitle {
    font-family: 'Barlow', sans-serif;
    font-size: 36px;
    font-weight: bold;
    color: #008080; /* Teal color */
    text-align: center;
    /* margin: -0.1rem 0 1rem 0; */
    /* padding: 0.5rem; */
  }
</style>

<!-- Sidebar Container -->
<div class="sidebar {sidebarVisible ? '' : 'sidebar-hidden'}" aria-hidden={!sidebarVisible}>
  <!-- Collapse Button -->
  <button class="collapse-button" on:click={closeSidebar} aria-label="Close sidebar">×</button>
  
  <div class="sidebar-content" bind:this={sidebarContentRef} on:scroll={handleScroll}>
    <!-- Header Section -->
    <header bind:this={mainHeaderRef}>
      <h1>How Much Housing Could Fit on the Parking Lots of NYC?</h1>
      <!-- <h2>A lot, actually</h2> -->
      <p>By: <a href="http://www.tomweatherburn.com/" target="_blank" rel="noopener noreferrer">Tom Weatherburn<span class="visually-hidden"> (opens in new tab)</span></a></p>
      <!-- <p class="introduction">
        This analysis explores the potential for housing development on surface parking lots near transit stations across New York City. By examining lot sizes, locations, and development patterns, we can estimate how many new housing units could be created in these underutilized spaces.
      </p> -->
    </header>



    <!-- Render each section -->
    {#each sections as section, index}
      <div class="section {section.isCollapsed ? 'collapsed' : ''}" data-section-index={index}>
        <h3
          class="section-header {index === currentSectionIndex && !section.isCollapsed ? 'selected' : ''}"
          bind:this={sectionHeaderRefs[index]}
        >
          <button
            class="section-header-button"
            on:click={() => toggleCollapse(index)}
            aria-expanded={!section.isCollapsed}
            aria-controls={`section-content-${index}`}
            type="button"
          >
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
          </button>
        </h3>
        {#if !section.isCollapsed}
          <div id={`section-content-${index}`} transition:slide={{ duration: 500 }}>
            {#each section.content as block}
              {#if block.type === 'text'}
                <p class={block.style || ''}>{@html block.value}</p>
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

  <!-- Navigation Controls -->
  <div class="bottom-nav-controls">
    <!-- Navigation Buttons -->
    <div class="bottom-nav-buttons">
      <button class="bottom-nav-button" on:click={previousSection} aria-label="Previous section">
        <svg width="12" height="12" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M10 12L6 8L10 4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Back</span>
      </button>
      <button class="bottom-nav-button" on:click={nextSection} aria-label="Next section">
        <span>Next</span>
        <svg width="12" height="12" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M6 4L10 8L6 12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
    
    <!-- Progress Indicator -->
    <div class="progress-indicator">
      {#each sections as section, index}
        <button 
          class="progress-dot {index === currentSectionIndex && !sections[index].isCollapsed ? 'active' : ''}"
          on:click={() => navigateToSection(index)}
          aria-label="Go to section {index + 1}"
        ></button>
      {/each}
    </div>
  </div>
</div>

<!-- Scroll Position Indicator -->
<!-- <div class="scroll-indicator">
  Scroll: {scrollPosition}px
</div> -->

<!-- Open Sidebar Button (Visible when Sidebar is hidden) -->
{#if !sidebarVisible}
  <button class="open-button" on:click={openSidebar} aria-label="Open sidebar">i</button>
{/if}