<script>
  import { onMount, onDestroy, createEventDispatcher } from 'svelte';
  import maplibre from 'maplibre-gl';
  // import 'maplibre-gl/dist/maplibre-gl.css'; // Import default MapLibre GL CSS if needed

  import stations from '../data/stations.json';
  import stations800m from '../data/stations_800m.json';
  import NYCsubways from '../data/NYCsubways.json';
  import lots_pts from '../data/lots_pts.json';
  import lots_par from '../data/lots_par.json';
  import dev_pts from '../data/dev_pts.json';
  import dev_par from '../data/dev_par.json';
  import mask from '../data/mask.json';
  import boro from '../data/boro.json';
  import borolabel from '../data/boro_pt.json';

  let map;
  const dispatch = createEventDispatcher();
  let mapShown = false; // flag to show map only once
  
  // Initialize coordinate display variables
  let cursorLng = '-74.000';
  let cursorLat = '40.700';
  let cursorZoom = '9.8';

  // // Fly-to function remains unchanged.
  // const flyTo = (coordinates = [-79.3832, 43.6532], zoomLevel = 14) => {
  //   if (map) {
  //     map.flyTo({
  //       center: coordinates,
  //       zoom: zoomLevel,
  //       speed: 0.8,
  //       curve: 1
  //     });
  //   }
  // };

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
      center: [-74.000, 40.700],
      zoom: 9.8,
      maxBounds: [
        [-74.9, 40.4],
        [-73.5, 41.0]
      ]
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
            'raster-opacity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              17, 0,
              18, 1
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

        // lots_pts layer (Points feeding the heatmap)
        map.addSource('lots_pts', { type: 'geojson', data: lots_pts });
        map.addLayer({
          'id': 'lots',
          'type': 'circle',
          'source': 'lots_pts',
          'layout': { 'visibility': 'none' },
          'paint': {
            'circle-radius': [
              'interpolate',
              ['linear'],
              ['zoom'],
              10, 2,
              16, 4
            ],
            'circle-color': '#B42222',
            'circle-opacity': 0.8
          }
        });

        // Interactive Popup Layer for lots_pts - with much larger clickable area
        map.addLayer({
          'id': 'lots_pts_popup',
          'type': 'circle',
          'source': 'lots_pts',
          'layout': { 'visibility': 'visible' },
          'paint': {
            'circle-radius': [
              'interpolate',
              ['linear'],
              ['zoom'],
              10, 20, // Significantly increased from 15
              16, 40  // Significantly increased from 30
            ],
            'circle-color': 'rgba(0,0,0,0)',
            'circle-opacity': 0
          }
        });
  
        map.on('mouseenter', 'lots_pts_popup', () => {
          map.getCanvas().style.cursor = 'pointer';
        });
        map.on('mouseleave', 'lots_pts_popup', () => {
          map.getCanvas().style.cursor = '';
        });
        
        // Add a click handler with a larger pixel buffer for easier clicking
        map.on('click', (e) => {
          // Use a larger pixel radius (30px) to query features around the click point
          const features = map.queryRenderedFeatures([
            [e.point.x - 20, e.point.y - 20],
            [e.point.x + 20, e.point.y + 20]
          ], { layers: ['lots_pts_popup'] });
          
          if (!features.length) return;
          const feature = features[0];
          const props = feature.properties;
          const content = `
            <span style="font-size:18px"><strong>${props.Address || 'N/A'}</strong></span><br>
            Borough: <strong>${props.boro_name || 'N/A'}</strong><br>
            Owner: <strong>${props.OwnerName || 'N/A'}</strong><br>
            Land Use: <strong>${props.LandUse || 'N/A'}</strong><br>
            Area (HA): <strong>${props.Area_HA || 'N/A'}</strong><br>
            <strong>Estimated Unit Potential:</strong>
            <span style="font-family: 'Barlow'; font-weight: 900; color: #FF5A30; font-size:44px; display: block; margin: 15px 0; text-align: center;">${props.EstUnitsBoro ? Math.round(props.EstUnitsBoro) : 'N/A'}</span>
          `;
          new maplibre.Popup({
            closeButton: true,
            closeOnClick: true,
            className: 'custom-popup'
          })
            .setLngLat(feature.geometry.coordinates)
            .setHTML(content)
            .addTo(map);
        });
  
        // Append custom CSS for the popup close button
        const style = document.createElement('style');
        style.innerHTML = `
          .maplibregl-popup .maplibregl-popup-close-button {
            padding: 5px;
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
              ['get', 'estimated_units'],
              0, 0,
              1000, 1
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
              0, 'rgba(220,250,250,0)',
              0.2, 'rgb(229,280,270, 0.5)',
              0.4, 'rgb(153,216,215)',
              0.6, 'rgb(102,194,184)',
              0.8, 'rgb(44,162,165)',
              1, 'rgb(0,109,130)'
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
  
        // Use map idle event to display the map container after all layers have loaded.
        map.on('idle', () => {
          if (!mapShown) {
            document.getElementById('map').style.display = 'block';
            mapShown = true;
          }
        });
  
        // Also log zoom events for debugging
        map.on('zoom', () => {
          console.log('Zoom level:', map.getZoom());
        });
  
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
    display: none; /* Hide the map initially */
  }
  
  .coordinates-box {
    position: absolute;
    top: 20px;
    right: 20px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 4px;
    font-family: monospace;
    font-size: 12px;
    z-index: 1000;  /* Increased z-index */
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    pointer-events: none;  /* Allow clicking through the box */
    user-select: none;  /* Prevent text selection */
  }
</style>
  
<div id="map"></div>
<div class="coordinates-box">
  Lng: {cursorLng} | Lat: {cursorLat} | Zoom: {cursorZoom}
</div>