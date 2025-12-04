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
	function flyTo(coordinates = [-79.3832, 43.6532], zoomLevel = 14, layerOn = [], layerOff = [], legendData = null) {
		if (mapRef && typeof mapRef.flyTo === 'function') {
			
			// Update legend BEFORE animation (lightweight DOM operation)
			if (legendData && mapRef.updateLegend) {
				mapRef.updateLegend(legendData);
			}
			
			// Set animation flag to suppress reactive updates during flyTo (prevents Windows glitching)
			if (mapRef.setAnimating) {
				mapRef.setAnimating(true);
			}
			
			// Perform flyTo with explicit parameters to prevent Windows glitching
			mapRef.flyTo({
				center: coordinates,
				zoom: zoomLevel,
				duration: 3500, // Longer duration to prevent motion sickness
				curve: 1.42, // Smoother curve for gentler animation
				essential: true, // Prevents animation from being interrupted
				easing: (t) => t * (2 - t), // Smooth easeOut curve
			});

			// Wait for animation to complete BEFORE changing layers
			// This prevents WebGL frame drops on Windows that cause "snapping"
			mapRef.once('moveend', () => {
				// Reset animation flag
				if (mapRef.setAnimating) {
					mapRef.setAnimating(false);
				}
				
				// Handle layer visibility AFTER animation completes
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
				
				// Fade in mask and stations800m layers when section 0 is opened
				// Section 0 coordinates: [-74.1009, 40.7000]
				if (coordinates[0] === -74.1009 && coordinates[1] === 40.7000 && mapRef.fadeInFirstSectionLayers) {
					mapRef.fadeInFirstSectionLayers();
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
		width: 100%;
		height: 100vh;
		overflow: hidden;
	}

	.map-container {
		flex: 1;
		height: 100vh;
		width: 100%;
		overflow: hidden;
		transition: all 0.4s ease;
		opacity: 0;
	}

	.map-container.visible {
		opacity: 1;
	}

	/* Mobile Responsive Styles */
	@media (max-width: 768px) {
		.app {
			flex-direction: column;
		}

		.map-container {
			height: 100vh;
			width: 100%;
			position: relative;
		}
		
		.map-container.sidebar-visible {
			width: 100%;
		}
	}

	/* Small Mobile Devices */
	@media (max-width: 480px) {
		.map-container {
			width: 100%;
			height: 100vh;
		}
	}

	/* Landscape orientation */
	@media (max-width: 768px) and (orientation: landscape) {
		.map-container {
			height: 100vh;
		}
	}

	/* Skip link styles */
	.skip-link {
		position: absolute;
		top: -40px;
		left: 0;
		background: #008080;
		color: white;
		padding: 8px 16px;
		z-index: 10000;
		text-decoration: none;
		font-family: 'Barlow', sans-serif;
	}

	.skip-link:focus {
		top: 0;
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

<a href="#main-content" class="skip-link">Skip to main content</a>

<div class="app">
	<!-- Splash Page (Visible on Load) -->
	{#if showSplash}
		<SplashPage onClose={closeSplash} />
	{/if}

	<!-- Map is always rendered but initially hidden -->
	<main id="main-content" class="map-container {showSplash ? '' : 'visible'}">
		<Map on:mapReady={handleMapRef} splashClosed={!showSplash} />
	</main>

	<!-- Main Content (Visible when Splash is hidden) -->
	{#if !showSplash}
		<Sidebar {flyTo} />
		<!-- <BoroChart /> -->
	{/if}
</div>