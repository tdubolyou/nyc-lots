<script>
    import { onMount } from 'svelte';
    import maplibre from 'maplibre-gl';
    import { createEventDispatcher } from 'svelte';
    import stations from '../data/stations.json'; // MTA Stations
    import lots from '../data/nyc_lots_units.geojson'; // MTA Stations
    let map;

    // Define a function to fly to the passed coordinates and zoom level
    export const flyTo = (coordinates = [-74.0060, 40.7128], zoomLevel = 14) => {
        if (map) {
        map.flyTo({
            center: coordinates,
            zoom: zoomLevel,
            speed: 0.8,
            curve: 1
        });
        }
    };
  
    onMount(() => {
        map = new maplibre.Map({
            container: 'map',
            style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
            center: [-74.0060, 40.7128],
            zoom: 12
        });

        // Add the GeoJSON source
        map.on('load', () => {
            map.addSource('stations', {
                type: 'geojson',
                data: stations
            });

            // Add a layer to display the points
            map.addLayer({
                'id': 'stations-layer',
                'type': 'circle',
                'source': 'stations',
                'paint': {
                    'circle-radius': {
                        'base': 2,
                        'stops': [
                            [12, 4], // Radius at zoom level 12
                            [22, 20] // Radius at zoom level 22
                        ]
                    },
                    'circle-color': 'darkred'
                }
            });

            map.addSource('lots', {
                type: 'geojson',
                data: lots
            });

            // Add a layer to display the points
            map.addLayer({
                'id': 'stations-layer',
                'type': 'circle',
                'source': 'lots',
                'paint': {
                    'circle-radius': {
                        'base': 2,
                        'stops': [
                            [12, 4], // Radius at zoom level 12
                            [22, 20] // Radius at zoom level 22
                        ]
                    },
                    'circle-color': 'darkred'
                }
            });
        });
    });
  </script>
  
  <style>
    #map {
      height: 100vh;
      width: 100%;
    }
  </style>
  
  <div id="map"></div>
  