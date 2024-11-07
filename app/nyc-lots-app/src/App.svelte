<script>
	import Sidebar from './components/Sidebar.svelte';
	import Map from './components/Map.svelte';
	import SplashPage from './components/SplashPage.svelte';

	let mapRef;
	let sidebarVisible = true;
	let showSplash = true;

	function handleMapRef(event) {
		mapRef = event.detail;
	}

	function toggleSidebar() {
   		sidebarVisible = !sidebarVisible;
  	}
	
	// Function to handle flyTo using the Map's method
	function flyTo(coordinates, zoomLevel) {
		if (mapRef) {
		mapRef.flyTo(coordinates, zoomLevel);
		}
	}

	// Function to close the splash page
	function closeSplash() {
		showSplash = false;
	}

  </script>
  
  <style>
	.app {
	  display: flex;
	  position: relative;
	}
  
	.map-container {
	  flex: 1;
	  height: 100vh;
	  overflow: hidden;
	  
	}
  </style>
  
  <div class="app">
	<!-- Splash Page (Visible on Load) -->
	{#if showSplash}
	  <SplashPage onClose={closeSplash} />
	{/if}
  
	<!-- Main Content (Visible when Splash is hidden) -->
	{#if !showSplash}
	  <Sidebar {flyTo} />
	  <div class="map-container">
		<Map bind:this={mapRef} />
	  </div>
	{/if}
  </div>
  