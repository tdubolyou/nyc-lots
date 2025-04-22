<script>
	import { i18n } from '$lib/i18n';
	import { ParaglideJS } from '@inlang/paraglide-sveltekit';
	import '../app.css';
	import 'maplibre-gl/dist/maplibre-gl.css'; // Import default MapLibre GL CSS
	let { children } = $props();

</script>

<ParaglideJS {i18n}>
	{@render children()}
</ParaglideJS>
