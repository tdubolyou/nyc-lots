<script>
	// Font import
	import '@fontsource/barlow';
	import '@fontsource/barlow-condensed';

	import Sidebar from '../components/Sidebar.svelte';
	import Map from '../components/Map.svelte';
	import SplashPage from '../components/Splash_.svelte';
	// import BoroChart from '../components/BoroChart.svelte';
	// import LotSizeChart from '../components/LotSize.svelte'

	let mapRef;
	let sidebarVisible = true;
	let showSplash = true;
	let mapLoaded = false;

	// Define a function to fly to the passed coordinates and zoom level
	function flyTo(coordinates = [-79.3832, 43.6532], zoomLevel = 14, layerOn = [], layerOff = []) {
		if (mapRef && typeof mapRef.flyTo === 'function') {
			mapRef.flyTo({
				center: coordinates,
				zoom: zoomLevel,
				speed: 0.8,
				curve: 1,
			});

			// Handle layer visibility
			layerOn.forEach(layerId => {
				if (mapRef.getLayer(layerId)) {
					mapRef.setLayoutProperty(layerId, 'visibility', 'visible');
				}
			});

			layerOff.forEach(layerId => {
				if (mapRef.getLayer(layerId)) {
					mapRef.setLayoutProperty(layerId, 'visibility', 'none');
				}
			});
		} else {
			console.error('Map reference is not set properly or does not have the flyTo method');
		}
	}

	function handleMapRef(event) {
		mapRef = event.detail; // Assign the map instance received from Map.svelte
		mapLoaded = true; // Set flag when the map is fully initialized
	}

	function toggleSidebar() {
		sidebarVisible = !sidebarVisible;
	}

	// Function to close the splash page
	function closeSplash() {
		showSplash = false;
	}
</script>

<style>
	@font-face {
		font-family: 'Barlow';
		src: url('/fonts/barlow/Barlow-ExtraBold.ttf') format('woff2');
		font-weight: 900;
		font-style: normal;
		font-display: swap;
	}

	.app {
		display: flex;
		position: relative;
	}

	.map-container {
		flex: 1;
		height: 100vh;
		overflow: hidden;
		transition: opacity 0.5s ease-in-out;
		opacity: 0; /* Hide the map initially */
	}

	.map-container.visible {
		opacity: 1; /* Fade in the map once the splash is dismissed */
	}
</style>

<div class="app">
	<!-- Splash Page (Visible on Load) -->
	{#if showSplash}
		<SplashPage onClose={closeSplash} />
	{/if}

	<!-- Map is always rendered but initially hidden -->
	<div class="map-container {showSplash ? '' : 'visible'}">
		<Map on:mapReady={handleMapRef} />
	</div>

	<!-- Main Content (Visible when Splash is hidden) -->
	{#if !showSplash}
		<Sidebar {flyTo} />
		<!-- <BoroChart /> -->
	{/if}
</div>