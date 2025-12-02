<script>
  import { onMount, onDestroy, createEventDispatcher } from 'svelte';
  import maplibre from 'maplibre-gl';
  import { base } from '$app/paths';
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
  export let splashClosed = false; // Prop to know when splash is closed
  
  // Initialize coordinate display variables
  let cursorLng = '-74.00';
  let cursorLat = '40.700';
  let cursorZoom = '9.8';

  // Reactive legend variables
  let legendTitle = "Parking Lot Area (hectares)";
  let legendGradientStyle = "linear-gradient(to right, rgba(220,250,250,0) 0%, rgba(229,280,270,0.5) 20%, rgb(153,216,215) 40%, rgb(102,194,184) 60%, rgb(44,162,165) 80%, rgb(0,109,130) 100%)";
  let legendLabels = ["0", "0.4", "0.8", "1.2", "1.6+"];
  
  // Track if first section has been opened to show map legend
  let showMapLegend = false;

  // Function to update legend from parent component
  function updateLegend(legendData) {
    if (legendData) {
      legendTitle = legendData.title;
      if (legendData.gradient === "development-gradient") {
        legendGradientStyle = "linear-gradient(to right, rgba(245,245,220,0) 0%, rgba(245,245,220,0) 5%, rgb(222,184,135,0.5) 20%, rgb(210,180,140) 40%, rgb(160,82,45) 60%, rgb(139,69,19) 80%, rgb(101,67,33) 95%, rgb(69,46,23) 100%)";
      } else if (legendData.gradient === "units-gradient") {
        // This matches the lots_units heatmap color ramp
        legendGradientStyle = "linear-gradient(to right, rgba(200,255,200,0) 0%, rgba(180,255,120,0.5) 20%, rgba(100,220,100,0.8) 40%, rgba(44,162,95,1) 60%, rgba(0,109,80,1) 80%, rgba(0,70,60,1) 100%)";
      } else if (legendData.gradient === "units-faded-gradient") {
        // This matches the lots_units_faded heatmap color ramp
        legendGradientStyle = "linear-gradient(to right, rgba(240,240,240,0) 0%, rgba(220,220,220,0.3) 20%, rgba(200,200,200,0.5) 40%, rgba(180,180,180,0.7) 60%, rgba(160,160,160,0.8) 80%, rgba(140,140,140,0.9) 100%)";
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
    // Removed - this functionality should be handled by the Sidebar component
  }

  // Reactive statement to trigger animation when splash is closed
  $: if (splashClosed && map && !initialAnimationComplete) {
    // Small delay to ensure smooth transition from splash to map
    setTimeout(playInitialAnimation, 500);
  }

  onMount(() => {
    // Hide the map container initially
    const mapEl = document.getElementById('map');
    if (mapEl) {
      mapEl.style.display = 'none';
    }

    map = new maplibre.Map({
      container: 'map',
      attributionControl: false,
      style: `${base}/mapTO-light.json`,
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
            'https://api.maptiler.com/maps/satellite/{z}/{x}/{y}.jpg?key=rGKSrBEhmKFMvUL5I5NH'
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
          'layout': {
            'visibility': 'none'
          },
          'paint': {
            'fill-color': '#FFFFFFFF',
            'fill-opacity': 0
          }
        });

        map.addSource('boro', { type: 'geojson', data: boro });
        map.addLayer({
          'id': 'boro',
          'type': 'fill',
          'source': 'boro',
          'layout': {
            'visibility': 'none'
          },
          'paint': {
            'fill-color': '#F0F0F0FF', // Very light grey color
            'fill-opacity': 0,
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
          'layout': {
            'visibility': 'none'
          },
          'paint': {
            'line-color': '#000000',
            'line-opacity': 0,
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
        
        // White hairline outline always visible
        map.addLayer({
          'id': 'lots_par_white_outline',
          'type': 'line',
          'source': 'lots_par',
          'minzoom': 0,
          'layout': { 'visibility': 'visible' },
          'paint': {
            'line-color': '#FFFFFF',
            'line-width': 0.5
          }
        });

        // Orange outline that appears at high zoom
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
        
        // Store reference to current popup (will be used after popup layer is added)
        let currentPopup = null;
  
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
              1.6, 1
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
              0.2, 'rgba(229,230,255, 0.5)',       // semi-transparent
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

        // Light grey version of lots_units heatmap for housing potential section
        map.addLayer({
          'id': 'lots_units_faded',
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
              0, 'rgba(240,240,240,0)',         // fully transparent light grey
              0.2, 'rgba(220,220,220,0.3)',     // semi-transparent light grey
              0.4, 'rgba(200,200,200,0.5)',     // medium light grey
              0.6, 'rgba(180,180,180,0.7)',     // darker light grey
              0.8, 'rgba(160,160,160,0.8)',     // darker grey
              1, 'rgba(140,140,140,0.9)'        // darkest grey
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
              0, 0.6,
              14, 0.6,
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

        // Add borough unit totals labels layer
        map.addLayer({
          'id': 'boro-unit-labels',
          'type': 'symbol',
          'source': 'borolabel',
          'layout': {
            'text-field': [
              'format',
              ['get', 'boroname'],
              { 'font-scale': 0.9 },
              '\n',
              {},
              ['number-format', ['round', ['get', 'est_units_total']], { 'min-fraction-digits': 0, 'max-fraction-digits': 0 }],
              { 'font-scale': 1.4 },
              '\n',
              {},
              ['concat', ['number-format', ['*', ['/', ['get', 'est_units_total'], 62528], 100], { 'min-fraction-digits': 1, 'max-fraction-digits': 1 }], '%'],
              { 'font-scale': 0.8 }
            ],
            'text-size': 20,
            'text-anchor': 'center',
            'text-font': ['Barlow Bold'],
            'symbol-placement': 'point',
            'text-allow-overlap': true,
            'text-ignore-placement': false,
            'visibility': 'none' // Hidden by default
          },
          'paint': {
            'text-color': [
              'case',
              ['==', ['get', 'boroname'], 'Brooklyn'], '#008080',
              ['==', ['get', 'boroname'], 'Manhattan'], '#008080', 
              ['==', ['get', 'boroname'], 'Bronx'], '#008080',
              ['==', ['get', 'boroname'], 'Queens'], '#008080',
              ['==', ['get', 'boroname'], 'Staten Island'], '#008080',
              '#000000'
            ],
            'text-halo-color': '#ffffff',
            'text-halo-width': 3
          }
        });
  
        // Use map idle event to display the map container and start animation
        map.on('idle', () => {
          if (!mapShown) {
            document.getElementById('map').style.display = 'block';
            mapShown = true;
            // Animation will be triggered by splashClosed prop instead
          }
        });
  

  
        // Add popup layer LAST so it's on top and can receive clicks
        // Use tiny opacity so it's queryable but invisible
        map.addSource('lots_par_popup', { type: 'geojson', data: lots_par_popup });
        map.addLayer({
          'id': 'lots_par_popup',
          'type': 'fill',
          'source': 'lots_par_popup',
          'layout': { 'visibility': 'visible' },
          'paint': {
            'fill-color': 'rgba(0,0,0,0)',
            'fill-opacity': 0.001  // Tiny opacity so layer is queryable
          }
        });
        
        // Helper function to find nearest point from lots_pts
        function findNearestPoint(clickLng, clickLat, pointX, pointY, maxDistance = 0.001) {
          // First, try to query rendered points (if visible) using a small bounding box
          const pointBox = [
            [pointX - 5, pointY - 5],
            [pointX + 5, pointY + 5]
          ];
          const pointFeatures = map.queryRenderedFeatures(pointBox, { layers: ['lots_pts'] });
          
          if (pointFeatures.length > 0) {
            return pointFeatures[0].properties;
          }
          
          // If no rendered points, search in the imported lots_pts data
          if (lots_pts && lots_pts.features) {
            let nearestPoint = null;
            let minDistance = Infinity;
            
            for (const pointFeature of lots_pts.features) {
              if (pointFeature.geometry && pointFeature.geometry.coordinates) {
                const [lng, lat] = pointFeature.geometry.coordinates;
                // Calculate distance using simple Euclidean distance (degrees)
                const dLat = lat - clickLat;
                const dLng = lng - clickLng;
                const distance = Math.sqrt(dLat * dLat + dLng * dLng);
                
                if (distance < minDistance && distance < maxDistance) {
                  minDistance = distance;
                  nearestPoint = pointFeature;
                }
              }
            }
            
            if (nearestPoint && nearestPoint.properties) {
              return nearestPoint.properties;
            }
          }
          
          return null;
        }
        
        // Add global click handler - query popup layer and find nearest point
        map.on('click', (e) => {
          // Query popup layer with bounding box
          const queryBox = [
            [e.point.x - 10, e.point.y - 10],
            [e.point.x + 10, e.point.y + 10]
          ];
          let features = map.queryRenderedFeatures(queryBox, { layers: ['lots_par_popup'] });
          
          let props = null;
          const clickLng = e.lngLat.lng;
          const clickLat = e.lngLat.lat;
          
          // If we got popup layer features, try to find nearest point first
          if (features.length > 0 && features[0].layer.id === 'lots_par_popup') {
            // Try to find nearest point from lots_pts
            const pointProps = findNearestPoint(clickLng, clickLat, e.point.x, e.point.y);
            if (pointProps) {
              props = pointProps;
            } else {
              // Fallback to parcel properties if no point found
              props = features[0].properties;
            }
          } else {
            // Fallback to fill layer and match to popup data
            features = map.queryRenderedFeatures(queryBox, { layers: ['lots_par_fill'] });
            if (features.length > 0) {
              const clickedFeature = features[0];
              
              // Try to find nearest point from lots_pts
              const pointProps = findNearestPoint(clickLng, clickLat, e.point.x, e.point.y);
              if (pointProps) {
                props = pointProps;
              } else {
                // Find matching feature in popup data by matching geometry
                if (lots_par_popup && lots_par_popup.features) {
                  const clickedGeom = JSON.stringify(clickedFeature.geometry.coordinates);
                  const popupMatch = lots_par_popup.features.find(f => {
                    if (!f.geometry || !f.geometry.coordinates) return false;
                    return JSON.stringify(f.geometry.coordinates) === clickedGeom;
                  });
                  if (popupMatch && popupMatch.properties) {
                    props = popupMatch.properties;
                  }
                }
                // If no match found, use fill layer properties as last resort
                if (!props) {
                  props = clickedFeature.properties;
                }
              }
            }
          }
          
          if (!props) return;
          
          // Close any existing popup first
          if (currentPopup) {
            currentPopup.remove();
            currentPopup = null;
          }
          
          // Handle both point data (Address) and parcel data (Address__pts)
          const address = props.Address__pts || props.Address || 'N/A';
          const owner = props.OwnerName__pts || props.OwnerName || 'N/A';
          
          const content = `
            <span style="font-size:18px"><strong>${address}</strong></span><br>
            Borough: ${props.boro_name || 'N/A'}<br>
            Owner: ${owner}<br>
            Area (HA): ${props.Area_HA ? parseFloat(props.Area_HA).toFixed(3) : 'N/A'}<br>
            Estimated Unit Potential:
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
  
        // Add updateLegend function to the map object
        map.updateLegend = updateLegend;
        
        // Add fade-in function for mask, stations800m, and boro layers
        map.fadeInFirstSectionLayers = function() {
          if (!map.getLayer('mask') || !map.getLayer('stations800m') || !map.getLayer('boro')) return;
          
          // Show the map legend
          showMapLegend = true;
          
          // Set visibility to visible
          map.setLayoutProperty('mask', 'visibility', 'visible');
          map.setLayoutProperty('stations800m', 'visibility', 'visible');
          map.setLayoutProperty('boro', 'visibility', 'visible');
          
          // Animate opacity fade-in
          const duration = 2500; // 2.5 seconds
          const startTime = performance.now();
          const startOpacityMask = 0;
          const targetOpacityMask = 0.9;
          const startOpacityStations = 0;
          const targetOpacityStations = 1;
          const startOpacityBoro = 0;
          const targetOpacityBoro = 1;
          
          function animate(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth fade
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            
            const currentOpacityMask = startOpacityMask + (targetOpacityMask - startOpacityMask) * easeProgress;
            const currentOpacityStations = startOpacityStations + (targetOpacityStations - startOpacityStations) * easeProgress;
            const currentOpacityBoro = startOpacityBoro + (targetOpacityBoro - startOpacityBoro) * easeProgress;
            
            map.setPaintProperty('mask', 'fill-opacity', currentOpacityMask);
            map.setPaintProperty('stations800m', 'line-opacity', currentOpacityStations);
            map.setPaintProperty('boro', 'fill-opacity', currentOpacityBoro);
            
            if (progress < 1) {
              requestAnimationFrame(animate);
            }
          }
          
          requestAnimationFrame(animate);
        };
        
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
    bottom: 20px;
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

  .map-legend {
    position: fixed;
    top: calc(20px + 80px + 8px); /* Position below the main legend */
    right: 20px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 4px;
    font-family: monospace;
    font-size: 12px;
    z-index: 1000;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    min-width: 150px;
  }

  .map-legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
  }

  .map-legend-item:last-child {
    margin-bottom: 0;
  }

  .map-legend-symbol {
    width: 30px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 8px;
  }

  .map-legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #000000;
  }

  .map-legend-line {
    width: 24px;
    height: 2px;
    border-top: 2px dashed #000000;
  }

  .map-legend-square {
    width: 16px;
    height: 16px;
    background-color: #F0F0F0;
    border: 1px solid #CCCCCC;
  }

  .map-legend-label {
    font-size: 11px;
    color: #333;
  }

  /* Mobile Responsive Styles */
  @media (max-width: 768px) {
    .coordinates-box {
      bottom: 50vh;
      right: 10px;
      font-size: 10px;
      padding: 8px;
    }

    .legend {
      top: 10px;
      right: 10px;
      bottom: auto;
      padding: 8px;
      font-size: 10px;
      max-width: 140px;
    }

    .legend-gradient {
      height: 15px;
      min-width: 120px;
    }

    .legend-labels {
      font-size: 8px;
    }

    .map-legend {
      top: calc(10px + 55px + 6px);
      right: 10px;
      padding: 8px;
      font-size: 10px;
      min-width: 110px;
    }

    .map-legend-label {
      font-size: 9px;
    }

    .map-legend-symbol {
      width: 24px;
      height: 16px;
      margin-right: 6px;
    }

    .map-legend-dot {
      width: 6px;
      height: 6px;
    }

    .map-legend-line {
      width: 20px;
    }

    .map-legend-square {
      width: 12px;
      height: 12px;
    }
  }

  /* Small Mobile Devices */
  @media (max-width: 480px) {
    .coordinates-box {
      display: none;
    }

    .legend {
      top: 8px;
      right: 8px;
      padding: 6px;
      max-width: 120px;
    }

    .legend-gradient {
      height: 10px;
      min-width: 100px;
    }

    .map-legend {
      display: none; /* Hide secondary legend on very small screens */
    }
  }

  /* Mobile popup styles */
  @media (max-width: 768px) {
    :global(.maplibregl-popup-content) {
      max-width: 280px !important;
      font-size: 13px !important;
      padding: 10px !important;
    }
    
    :global(.maplibregl-popup-content span[style*="font-size:44px"]) {
      font-size: 32px !important;
    }
  }

  @media (max-width: 480px) {
    :global(.maplibregl-popup-content) {
      max-width: 240px !important;
      font-size: 12px !important;
      padding: 8px !important;
    }
    
    :global(.maplibregl-popup-content span[style*="font-size:44px"]) {
      font-size: 28px !important;
    }
  }
</style>
  
<div id="map" role="application" aria-label="Interactive map of New York City showing surface parking lots within 800 meters of MTA transit stations. Use sidebar navigation to explore different sections and click on parking lots for details."></div>
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
{#if showMapLegend}
<div class="map-legend">
  <div class="map-legend-item">
    <div class="map-legend-symbol">
      <div class="map-legend-dot"></div>
    </div>
    <div class="map-legend-label">MTA Stations</div>
  </div>
  <div class="map-legend-item">
    <div class="map-legend-symbol">
      <div class="map-legend-line"></div>
    </div>
    <div class="map-legend-label">800m Buffer</div>
  </div>
  <div class="map-legend-item">
    <div class="map-legend-symbol">
      <div class="map-legend-square"></div>
    </div>
    <div class="map-legend-label">NYC</div>
  </div>
</div>
{/if}