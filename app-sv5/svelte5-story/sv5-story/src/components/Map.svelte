<script>
  import { onMount, onDestroy, createEventDispatcher } from 'svelte';
  import maplibre from 'maplibre-gl';
  // import 'maplibre-gl/dist/maplibre-gl.css'; // Import default MapLibre GL CSS if needed

  import stations from '../data/stations.json';
  import stations800m from '../data/stations_800m.json';
  import NYCsubways from '../data/NYCsubways.json';
  import lots_pts from '../data/lots_pts.json';
  import lots_par from '../data/lots_par.json';
  import lots_par_popup from '../data/lots_par_popup.json';
  import dev_pts from '../data/dev_pts.json';
  import dev_par from '../data/dev_par.json';
  import mask from '../data/mask.json';
  import boro from '../data/boro.json';
  import borolabel from '../data/boro_pt.json';
  //import { openSection } from './Sidebar.svelte';

  let map;
  const dispatch = createEventDispatcher();
  let mapShown = false; // flag to show map only once
  let initialAnimationComplete = false; // Track if initial animation has played
  
  // Initialize coordinate display variables
  let cursorLng = '-74.00';
  let cursorLat = '40.700';
  let cursorZoom = '9.8';

  // Reactive legend variables
  let legendTitle = "Parking Lot Area (m²)";
  let legendGradientStyle = "linear-gradient(to right, rgba(220,250,250,0) 0%, rgba(229,280,270,0.5) 20%, rgb(153,216,215) 40%, rgb(102,194,184) 60%, rgb(44,162,165) 80%, rgb(0,109,130) 100%)";
  let legendLabels = ["0", "250", "500", "750", "1000+"];

  // Function to update legend from parent component
  function updateLegend(legendData) {
    if (legendData) {
      legendTitle = legendData.title;
      if (legendData.gradient === "development-gradient") {
        legendGradientStyle = "linear-gradient(to right, rgba(245,245,220,0) 0%, rgba(245,245,220,0) 5%, rgb(222,184,135,0.5) 20%, rgb(210,180,140) 40%, rgb(160,82,45) 60%, rgb(139,69,19) 80%, rgb(101,67,33) 95%, rgb(69,46,23) 100%)";
      } else if (legendData.gradient === "units-gradient") {
        // This matches the lots_units heatmap color ramp
        legendGradientStyle = "linear-gradient(to right, rgba(200,255,200,0) 0%, rgba(180,255,120,0.5) 20%, rgba(100,220,100,0.8) 40%, rgba(44,162,95,1) 60%, rgba(0,109,80,1) 80%, rgba(0,70,60,1) 100%)";
      } else {
        legendGradientStyle = "linear-gradient(to right, rgba(220,250,250,0) 0%, rgba(229,280,270,0.5) 20%, rgb(153,216,215) 40%, rgb(102,194,184) 60%, rgb(44,162,165) 80%, rgb(0,109,130) 100%)";
      }
      legendLabels = legendData.labels;
    }
  }

  // Function to handle the initial zoom animation
  function playInitialAnimation() {
    if (!map || initialAnimationComplete) return;
    
    map.flyTo({
      center: [-74.1009, 40.7000],
      zoom: 9.9,
      bearing: 0,
      pitch: 0,
      duration: 5000, // Animation duration in milliseconds (12 seconds)
      essential: true
    });
    
    initialAnimationComplete = true;

    // Open the first sidebar section after the animation
    setTimeout(() => {
      openSection.set(0);
    }, 5000); // Match the duration of the flyTo
  }

  // Updated flyTo function to handle legend data, now with "gradient-units" for lots_units color scheme
  const flyTo = (coordinates = [-79.3832, 43.6532], zoomLevel = 14, layerOn = [], layerOff = [], legendData = null) => {
    if (map) {
      // Update legend if provided
      if (legendData) {
        legendTitle = legendData.title;
        if (legendData.gradient === "development-gradient") {
          legendGradientStyle = "linear-gradient(to right, rgba(245,245,220,0) 0%, rgba(245,245,220,0) 5%, rgb(222,184,135,0.5) 20%, rgb(210,180,140) 40%, rgb(160,82,45) 60%, rgb(139,69,19) 80%, rgb(101,67,33) 95%, rgb(69,46,23) 100%)";
        } else if (legendData.gradient === "units-gradient") {
          // This matches the lots_units heatmap color ramp
          legendGradientStyle = "linear-gradient(to right, rgba(200,255,200,0) 0%, rgba(180,255,120,0.5) 20%, rgba(100,220,100,0.8) 40%, rgba(44,162,95,1) 60%, rgba(0,109,80,1) 80%, rgba(0,70,60,1) 100%)";
        } else {
          legendGradientStyle = "linear-gradient(to right, rgba(220,250,250,0) 0%, rgba(229,280,270,0.5) 20%, rgb(153,216,215) 40%, rgb(102,194,184) 60%, rgb(44,162,165) 80%, rgb(0,109,130) 100%)";
        }
        legendLabels = legendData.labels;
      }
      
      map.flyTo({
        center: coordinates,
        zoom: zoomLevel,
        speed: 0.8,
        curve: 1
      });
    }
  };

  onMount(() => {
    // Hide the map container initially
    const mapEl = document.getElementById('map');
    if (mapEl) {
      mapEl.style.display = 'none';
    }

    map = new maplibre.Map({
      container: 'map',
      attributionControl: false,
      style: '/mapTO-light.json',
      center: [-73.9748, 40.6935], // Starting position for the animation
      zoom: 8.7, // Starting zoom level
      // maxBounds: [
      //   [-74.9, 40.4],
      //   [-73.5, 41.0]
      // ]
    });

    // Add mousemove event handler
    map.on('mousemove', (e) => {
      cursorLng = e.lngLat.lng.toFixed(4);
      cursorLat = e.lngLat.lat.toFixed(4);
      cursorZoom = map.getZoom().toFixed(2);
    });

    // Add zoom event handler
    map.on('zoom', () => {
      cursorZoom = map.getZoom().toFixed(2);
    });

    map.on('load', () => {
      try {
        // -----------------------------------------------------
        // 1. Satellite Imagery Layer (covers entire basemap)
        // -----------------------------------------------------
        map.addSource('satellite', {
          type: 'raster',
          tiles: [
            'https://api.maptiler.com/maps/satellite/{z}/{x}/{y}.jpg?key=get_your_own_OpIi9ZULNHzrESv6T2vL'
          ],
          tileSize: 256
        });
        map.addLayer({
          'id': 'satellite',
          'type': 'raster',
          'source': 'satellite',
          'paint': {
            // Satellite imagery fades in only at very high zoom levels.
            // At zoom 17, the satellite layer is fully transparent (opacity 0).
            // At zoom 18, the satellite layer is fully opaque (opacity 1).
            // This ensures satellite imagery is only visible when zoomed in very close.
            'raster-opacity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              17, 0,   // No satellite at or below zoom 17
              18, 1    // Fully visible at zoom 18 and above
            ]
          }
        });
        // -----------------------------------------------------
        // 2. Custom Overlay Layers (above the satellite imagery)
        // -----------------------------------------------------
        map.addSource('mask', { type: 'geojson', data: mask });
        map.addLayer({
          'id': 'mask',
          'type': 'fill',
          'source': 'mask',
          'paint': {
            'fill-color': '#FFFFFFFF',
            'fill-opacity': 0.9
          }
        });

        map.addSource('boro', { type: 'geojson', data: boro });
        map.addLayer({
          'id': 'boro',
          'type': 'fill',
          'source': 'boro',
          'paint': {
            'fill-color': '#F0F0F0FF', // Very light grey color
            'fill-opacity': 1, // Ensure the fill is visible
            'fill-outline-color': '#FFFFFF' // Add white outline
          }
        });
        
        
        
        map.addSource('stations', { type: 'geojson', data: stations });
        map.addLayer({
          'id': 'stations',
          'type': 'circle',
          'source': 'stations',
          'paint': {
            'circle-radius': [
              'interpolate',
              ['exponential', 1.75],
              ['zoom'],
              8, 1,
              12, 3,
              14, 6,
              16, 12
            ],
            'circle-color': '#000',
            'circle-stroke-color': '#fff',
            'circle-stroke-width': 1,
            'circle-opacity': 0.8
          }
        });

        // Add station labels
        map.addLayer({
          'id': 'station-labels',
          'type': 'symbol',
          'source': 'stations',
          'minzoom': 13,
          'layout': {
            'text-field': ['get', 'StationName'],
            'text-size': 12,
            'text-anchor': 'top',
            'text-offset': [0, 1],
            'text-allow-overlap': false
          },
          'paint': {
            'text-color': '#333333',
            'text-halo-color': '#ffffff',
            'text-halo-width': 1.5
          }
        });

        map.addSource('stations800m', { type: 'geojson', data: stations800m });
        map.addLayer({
          'id': 'stations800m',
          'type': 'line',
          'source': 'stations800m',
          'paint': {
            'line-color': '#000000',
            'line-width': [
              'interpolate',
              ['exponential', 1.75],
              ['zoom'],
              8, 1,
              12, 2,
              14, 3,
              16, 4
            ],
            'line-dasharray': [2, 2]
          }
        });

        map.addSource('NYCsubways', { type: 'geojson', data: NYCsubways });
        map.addLayer({
          'id': 'NYCsubways',
          'type': 'line',
          'source': 'NYCsubways',
          'paint': {
            'line-width': 1,
            'line-color': '#333333'
          }
        });

        // lots_par layers (Parking Lots)
        map.addSource('lots_par', { type: 'geojson', data: lots_par });
        map.addLayer({
          'id': 'lots_par_fill',
          'type': 'fill',
          'source': 'lots_par',
          'minzoom': 0,
          'maxzoom': 17,
          'layout': { 'visibility': 'visible' },
          'paint': {
            'fill-color': '#175A5AFF',
            'fill-opacity': 1
          }
        });
        
        map.addLayer({
          'id': 'lots_par_outline',
          'type': 'line',
          'source': 'lots_par',
          'minzoom': 17,
          'layout': { 'visibility': 'visible' },
          'paint': {
            'line-color': '#FF4500',
            'line-width': 2
          }
        });

        // Invisible popup layer for lots_par - covers entire parcel area
        map.addSource('lots_par_popup', { type: 'geojson', data: lots_par_popup });
        map.addLayer({
          'id': 'lots_par_popup',
          'type': 'fill',
          'source': 'lots_par_popup',
          'layout': { 'visibility': 'visible' },
          'paint': {
            'fill-color': 'rgba(0,0,0,0)',
            'fill-opacity': 0
          }
        });

        // lots_pts layer (Points feeding the heatmap)
        map.addSource('lots_pts', { type: 'geojson', data: lots_pts });
        // map.addLayer({
        //   'id': 'lots',
        //   'type': 'circle',
        //   'source': 'lots_pts',
        //   'layout': { 'visibility': 'none' },
        //   'paint': {
        //     'circle-radius': [
        //       'interpolate',
        //       ['linear'],
        //       ['zoom'],
        //       10, 2,
        //       16, 4
        //     ],
        //     'circle-color': '#B42222',
        //     'circle-opacity': 0.8
        //   }
        // });
  
        map.on('mouseenter', 'lots_par_popup', () => {
          map.getCanvas().style.cursor = 'pointer';
        });
        map.on('mouseleave', 'lots_par_popup', () => {
          map.getCanvas().style.cursor = '';
        });
        
        // Add mouse events for the polygon layer
        map.on('mouseenter', 'lots_par_fill', () => {
          map.getCanvas().style.cursor = 'pointer';
        });
        map.on('mouseleave', 'lots_par_fill', () => {
          map.getCanvas().style.cursor = '';
        });
        
        // Add a click handler with a larger pixel buffer for easier clicking
        let currentPopup = null; // Store reference to current popup
        
        map.on('click', (e) => {
          // Close any existing popup first
          if (currentPopup) {
            currentPopup.remove();
            currentPopup = null;
          }
          
          // Use a larger pixel radius (30px) to query features around the click point
          const features = map.queryRenderedFeatures([
            // e.point,
          [e.point.x - 20, e.point.y - 20],
          [e.point.x + 20, e.point.y + 20]
          ], { layers: ['lots_par_popup'] });
          
          if (!features.length) return;
          const feature = features[0];
          const props = feature.properties;
          const content = `
            <span style="font-size:18px"><strong>${props.Address__pts || 'N/A'}</strong></span><br>
            Borough: <strong>${props.boro_name || 'N/A'}</strong><br>
            Owner: <strong>${props.OwnerName__pts  || 'N/A'}</strong><br>
            Area (HA): <strong>${props.Area_HA || 'N/A'}</strong><br>
            <strong>Estimated Unit Potential:</strong>
            <span style="font-family: 'Barlow'; font-weight: 900; color: #FF5A30; font-size:44px; display: block; margin: 15px 0; text-align: center;">${props.EstUnitsBoro ? Math.round(props.EstUnitsBoro) : 'N/A'}</span>
          `;
          currentPopup = new maplibre.Popup({
            closeButton: true,
            closeOnClick: true,
            className: 'custom-popup'
          })
            .setLngLat(e.lngLat)
            .setHTML(content)
            .addTo(map);
        });
        
        // Close popup on zoom/scroll
        map.on('zoom', () => {
          if (currentPopup) {
            currentPopup.remove();
            currentPopup = null;
          }
        });
        
        // Close popup on drag/pan
        map.on('dragstart', () => {
          if (currentPopup) {
            currentPopup.remove();
            currentPopup = null;
          }
        });
  
        // Append custom CSS for the popup close button
        const style = document.createElement('style');
        style.innerHTML = `
          .maplibregl-popup .maplibregl-popup-close-button {
            padding: 5px;
          }
          .dev-popup .maplibregl-popup-content {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 4px;
            padding: 8px 12px;
            font-family: 'Barlow', sans-serif;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
          }
        `;
        document.head.appendChild(style);
  
        map.addLayer({
          'id': 'heatmap',
          'type': 'heatmap',
          'source': 'lots_pts',
          'paint': {
            'heatmap-weight': [
              'interpolate',
              ['linear'],
              ['get', 'Area_HA'],
              0, 0,
              30, 1
            ],
            'heatmap-intensity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, 2,
              9, 8
            ],
            'heatmap-color': [
              'interpolate',
              ['linear'],
              ['heatmap-density'],
              0, 'rgba(220,250,250,0)',           // fully transparent
              0.2, 'rgba(229,230,255, 0.5)',       // semi-transparent (should be rgba for opacity)
              0.4, 'rgb(153,216,215)',            // opaque
              0.6, 'rgb(102,194,184)',            // opaque
              0.8, 'rgb(44,162,165)',             // opaque
              1, 'rgb(0,109,130)'                 // opaque
            ],
            'heatmap-radius': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, 4,
              9, 10,
              14, 35,
              30, 200
            ],
            'heatmap-opacity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, 0.8,
              14, 0.8,
              14.01, 0
            ]
          }
        });

        // New lots_units heatmap layer with green color ramp
        map.addLayer({
          'id': 'lots_units',
          'type': 'heatmap',
          'source': 'lots_pts',
          'layout': {
            'visibility': 'none'
          },
          'paint': {
            'heatmap-weight': [
              'interpolate',
              ['linear'],
              ['get', 'EstUnitsBoro'],
              0, 0,
              1000, 1
            ],
            'heatmap-intensity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, 2,
              9, 5
            ],
            'heatmap-color': [
              'interpolate',
              ['linear'],
              ['heatmap-density'],
              0, 'rgba(200,255,200,0)',         // fully transparent
              0.2, 'rgba(180,255,120,0.5)',     // semi-transparent lime green
              0.4, 'rgba(100,220,100,0.8)',     // medium green
              0.6, 'rgba(44,162,95,1)',         // darker green
              0.8, 'rgba(0,109,80,1)',          // dark blue-green
              1, 'rgba(0,70,60,1)'              // darkest
            ],
            'heatmap-radius': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, 4,
              9, 10,
              14, 35,
              20, 200
            ],
            'heatmap-opacity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, 0.8,
              14, 0.8,
              14.01, 0
            ]
          }
        });

        map.addSource('dev_par', { type: 'geojson', data: dev_par });
        map.addLayer({
          'id': 'dev_par_fill',
          'type': 'fill',
          'source': 'dev_par',
          'layout': {
            'visibility': 'none'
          },
          'paint': {
            'fill-color': '#974312FF',
            'fill-opacity': 0.7,
            'fill-outline-color': '#974312FF'
          }
        });

        // Add a thin white outline layer for dev_par polygons
        map.addLayer({
          'id': 'dev_par_outline',
          'type': 'line',
          'source': 'dev_par',
          'layout': {
            'visibility': 'none'
          },
          'paint': {
            'line-color': '#ffffff',
            'line-width': 1.2
          }
        });

        // Add hover popup for development polygons
        let devPopup = null;
        
        map.on('mouseenter', 'dev_par_fill', (e) => {
          map.getCanvas().style.cursor = 'pointer';
          
          if (e.features.length > 0) {
            const feature = e.features[0];
            const props = feature.properties;
            
            const content = `
              <div style="font-size: 14px; line-height: 1.4;">
                <strong>${props.Address || 'N/A'}</strong><br>
                Units/HA: <strong>${props.UnitsHA ? Math.round(props.UnitsHA * 10) / 10 : 'N/A'}</strong>
              </div>
            `;
            
            devPopup = new maplibre.Popup({
              closeButton: false,
              closeOnClick: false,
              className: 'dev-popup'
            })
              .setLngLat(e.lngLat)
              .setHTML(content)
              .addTo(map);
          }
        });
        
        map.on('mouseleave', 'dev_par_fill', () => {
          map.getCanvas().style.cursor = '';
          if (devPopup) {
            devPopup.remove();
            devPopup = null;
          }
        });
        
        // Remove popup on zoom change
        map.on('zoom', () => {
          if (devPopup) {
            devPopup.remove();
            devPopup = null;
          }
        });

        // Add dev_pts heatmap layer
        map.addSource('dev_pts', { type: 'geojson', data: dev_pts });
        map.addLayer({
          'id': 'dev_pts_heatmap',
          'type': 'heatmap',
          'source': 'dev_pts',
          'layout': {
            'visibility': 'none'
          },
          'paint': {
            'heatmap-weight': [
              'interpolate',
              ['linear'],
              ['get', 'UnitsHA'],
              0, 0,
              122, 1
            ],
            'heatmap-intensity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, 1,
              9, 3
            ],
            'heatmap-color': [
              'interpolate',
              ['linear'],
              ['heatmap-density'],
              0, 'rgba(245,245,220,0)',
              0.05, 'rgba(245,245,220,0)',
              0.2, 'rgb(222,184,135, 0.5)',
              0.4, 'rgb(210,180,140)',
              0.6, 'rgb(160,82,45)',
              0.8, 'rgb(139,69,19)',
              0.95, 'rgb(101,67,33)',
              1, 'rgb(69,46,23)'
            ],
            'heatmap-radius': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, 3,
              9, 8,
              14, 15,
              20, 40
            ],
            'heatmap-opacity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, 0.8,
              14, 0.8,
              14.01, 0
            ]
          }
        });

        // Ensure borough labels use calculated centroids for correct placement
        // Ensure borough labels use calculated centroids for correct placement
        map.addSource('borolabel', { type: 'geojson', data: borolabel });
        map.addLayer({
          'id': 'boro-labels',
          'type': 'symbol',
          'source': 'borolabel',
          'layout': {
            'text-field': ['get', 'boroname'],
            'text-size': 12, // Increased for better visibility
            'text-anchor': 'center',
            'text-transform': 'uppercase',
            'text-letter-spacing': 0.15, // Slightly increased for clarity
            'symbol-placement': 'point',
            'text-allow-overlap': false,
            'text-ignore-placement': false
          },
          'paint': {
            'text-color': '#0E0E0EFF', // Darker shade for better contrast
            'text-halo-color': '#ffffff',
            'text-halo-width': 2.5 // Slightly increased for better readability
          }
        });
  
        // Use map idle event to display the map container and start animation
        map.on('idle', () => {
          if (!mapShown) {
            document.getElementById('map').style.display = 'block';
            mapShown = true;
            // Start the animation after a short delay to ensure smooth transition
            setTimeout(playInitialAnimation, 1000);
          }
        });
  

  
        // Add updateLegend function to the map object
        map.updateLegend = updateLegend;
        dispatch('mapReady', map);
      } catch (error) {
        console.error('Error adding GeoJSON source to the map:', error);
      }
    });
  
    onDestroy(() => {
      if (map) map.remove();
    });
  });
</script>
  
<style>
  #map {
    height: 100vh;
    width: 100%;
    display: none;
  }
  
  .coordinates-box {
    position: fixed;
    top: calc(20px + 80px + 8px); /* 20px (legend top) + 80px (legend height estimate) + 8px (margin) */
    right: 20px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 4px;
    font-family: monospace;
    font-size: 12px;
    z-index: 1000;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    pointer-events: none;
    user-select: none;
  }

  .legend {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 4px;
    font-family: monospace;
    font-size: 12px;
    z-index: 1000;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    margin-bottom: 8px; /* Add margin to separate from coordinates box */
  }

  .legend-gradient {
    height: 20px;
    min-width: 200px;
    margin-bottom: 5px;
    background-size: 100% 100%;
    background-repeat: no-repeat;
    border-radius: 2px;
    overflow: hidden;
  }
  
  .legend-labels {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
  }

  /* Mobile Responsive Styles */
  @media (max-width: 768px) {
    .coordinates-box {
      top: 10px;
      right: 10px;
      font-size: 10px;
      padding: 8px;
    }

    .legend {
      top: 20px;
      right: 20px;
      bottom: auto;
      padding: 8px;
      font-size: 10px;
    }

    .legend-gradient {
      height: 15px;
      min-width: 150px;
    }

    .legend-labels {
      font-size: 8px;
    }
  }

  /* Small Mobile Devices */
  @media (max-width: 480px) {
    .coordinates-box {
      display: none;
    }

    .legend {
      top: 15px;
      right: 15px;
      padding: 6px;
    }

    .legend-gradient {
      height: 12px;
      min-width: 120px;
    }
  }
</style>
  
<div id="map"></div>
<div class="coordinates-box">
  Lng: {cursorLng} | Lat: {cursorLat} | Zoom: {cursorZoom}
</div>
<div class="legend">
  <div>{legendTitle}</div>
  <div class="legend-gradient" style="background: {legendGradientStyle}"></div>
  <div class="legend-labels">
    {#each legendLabels as label}
      <span>{label}</span>
    {/each}
  </div>
</div>