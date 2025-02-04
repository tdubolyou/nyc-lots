<script>
    import { onMount } from 'svelte';
    import maplibre from 'maplibre-gl';
    import { createEventDispatcher } from 'svelte';
  
    let map;

    // Define a function to fly to the passed coordinates and zoom level
    export const flyTo = (coordinates = [-79.3832, 43.6532], zoomLevel = 14) => {
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
        center: [-79.3832, 43.6532], // Toronto, for example
        zoom: 12
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
  