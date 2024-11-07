<script>
    export let flyTo; // Function passed in from the parent component to handle map flyTo

    let sidebarVisible = true;

    let sections = [
        { title: "Introduction", content: "Introduction section content.", coordinates: [-79.3832, 43.6532], zoomLevel: 14, isCollapsed: true },
        { title: "Data Sources", content: "Details about data sources.", coordinates: [-79.3871, 43.6426], zoomLevel: 16, isCollapsed: true },
        { title: "Analysis", content: "Analysis of the map data.", coordinates: [-79.3716, 43.6615], zoomLevel: 15, isCollapsed: true },
        { title: "Conclusion", content: "Final thoughts and conclusions.", coordinates: [-79.4000, 43.6481], zoomLevel: 13, isCollapsed: true }

    ];
    
    function closeSidebar() {
      sidebarVisible = false;
    }
  
    function openSidebar() {
      sidebarVisible = true;
    }
  
    
    // function toggleCollapse(index) {
    //   sections[index].isCollapsed = !sections[index].isCollapsed;

    //   // Call flyTo only when the section is expanded
    //   if (!sections[index].isCollapsed) {
    //     flyTo(sections[index].coordinates, sections[index].zoomLevel);
    //     }
    // }
  
    // Function to toggle the selected section and collapse others
    function toggleCollapse(index) {
        sections = sections.map((section, i) => {
        // Expand the selected section and collapse all others
        if (i === index) {
            section.isCollapsed = !section.isCollapsed;
            // Call flyTo only when the section is expanded
            if (!section.isCollapsed) {
            flyTo(section.coordinates, section.zoomLevel);
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
      width: 300px;
      position: absolute;
      left: 0;
      transition: transform 0.4s ease;
      font-family: 'Source Sans Pro', sans-serif;
    }
  
    .sidebar-hidden {
      transform: translateX(-100%);
    }
  
    .section-header {
      color: #000; /* Black headers */
      cursor: pointer;
      font-weight: bold;
      margin: 0.5rem 0;
    }
  
    .section-header:hover {
      text-decoration: underline;
    }
  
    header h1, header h2, header p {
      color: #000;
      margin: 0;
    }
  
    header h1 {
      font-size: 1.5rem;
      font-weight: 800;
    }
  
    header h2 {
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
    }
  
    header p {
      font-size: 0.85rem;
      color: #555; /* Slightly grey body text */
      margin-bottom: 1rem;
    }
  
    a {
      color: #FF5A30; /* Orange links */
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
      top: 10px;
      left: 10px;
      background: #FF5A30; /* mapTO orange */
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
  </style>
  
  <!-- Sidebar Container -->
  <div class="sidebar {sidebarVisible ? '' : 'sidebar-hidden'}">
    <!-- Collapse Button -->
    <button class="collapse-button" on:click={closeSidebar}>×</button>
    
    <!-- Header Section -->
    <header>
      <h1>Story Map Title</h1>
      <h2>Subtitle Goes Here</h2>
      <p>By: Your Name</p>
    </header>
  
    <!-- Accordions for Each Section -->
    {#each sections as section, index}
      <div class="section">
        <h3 class="section-header" on:click={() => { toggleCollapse(index)}}>
            {section.title}
          </h3>
        {#if !section.isCollapsed}
          <p>{section.content}</p>
        {/if}
      </div>
    {/each}
  </div>
  
  <!-- Open Sidebar Button (Visible when Sidebar is hidden) -->
  {#if !sidebarVisible}
    <button class="open-button" on:click={openSidebar}>i</button>
  {/if}
  