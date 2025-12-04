# FlyTo Glitching on Windows — Diagnostic Guide  
**MapLibre GL JS**

This document summarizes all known causes of `map.flyTo()` appearing to **jump, snap, or glitch** specifically on **Windows machines**.  
Your older non-Svelte MapLibre build works smoothly on the same hardware, so the issue lies in the **new application code paths**, not your OS or GPU.

---

## 1. Duplicate `flyTo()` Calls (Double-Firing)

If `flyTo()` fires more than once per interaction, MapLibre cancels the first animation and jumps to the final state.

### Symptoms  
- Animation starts, then instantly snaps.  
- Behavior worse on Windows due to event timing differences.

### Test  
Add:

```js
console.trace("flyTo called");
```

If you see more than one trace → this is the cause.

---

## 2. MapLibre Events Interrupting the Animation

Events like:

- `move`  
- `moveend`  
- `idle`  
- `zoom`  
- `load`  

…may fire during a flyTo and break the animation loop.

### Test

```js
map.off('move');
map.off('moveend');
map.off('idle');
map.off('zoom');
```

If flyTo becomes smooth → confirmed.

---

## 3. Layer or Source Updates During FlyTo

Heavy operations:

- updating GeoJSON  
- changing filters  
- toggling visibility  
- adding/removing layers  
- applying new styles  

…can block WebGL rendering for 1–3 frames.

Mac hides this.  
Windows exposes it.

### Test  
Temporarily remove all non-basemap layers:

```js
map.getStyle().layers.forEach(l => {
  if (l.id !== 'background') map.removeLayer(l.id);
});
```

If flyTo is smooth → this was the cause.

---

## 4. UI / DOM Updates Interrupting WebGL Frames

DOM updates triggered by your click (or during animation) can block MapLibre’s animation frames:

- showing/hiding sidebars  
- updating labels  
- reactive UI state changes  
- layout reflows  
- CSS transitions  

These pauses cause the map to “jump forward” instead of animating smoothly.

---

## 5. Missing or Implicit FlyTo Parameters

When duration, curve, or easing are omitted, MapLibre sometimes computes a **0 ms duration** on lower-precision Windows timers.

### Safer explicit parameters:

```js
map.flyTo({
  center: [lon, lat],
  zoom: targetZoom,
  speed: 0.5,
  curve: 1.5,
  easing: (t) => t,
  duration: 2000,
  essential: true,
  animate: true
});
```

If this fixes it → duration collapse was the cause.

---

## 6. MapLibre Version Differences

Your older working build likely uses **Mapbox GL JS 1.10–1.11**, which had extremely stable camera transitions.

Your new build likely uses **MapLibre 2.x or 3.x**, which introduced:

- different interpolation  
- different timing logic  
- known regressions in smooth fly animations  
- frame skipping when layers are heavy  

### Test Version  
In console:

```js
maplibregl.version
```

Try matching versions between projects.

---

## 7. WebGL Frame Scheduling Differences on Windows

Even with hardware acceleration disabled, Windows still has:

- lower timer resolution  
- more aggressive frame coalescing  
- different requestAnimationFrame scheduling  
- more stall points under heavy GPU load  

This makes MapLibre more sensitive to interruptions during animation.

---

## 8. UI Framework or Reactive Logic Causing Mid-Animation Interruption

If any UI state updates during flyTo — even if subtle — MapLibre’s canvas may be “touched” in a way that resets or disrupts the animation loop.

These include:

- updating component state  
- hover interactions  
- recalculating layout  
- conditional DOM rendering  

These interrupts show up first on Windows.

---

## 9. Calling `setCenter`, `setZoom`, or `fitBounds` Around `flyTo`

If you do:

```js
map.setCenter(coords);
map.flyTo(...);
```

or:

```js
map.flyTo(...);
map.fitBounds(...);
```

The first transition is silently cancelled.

### Result  
It appears as a glitch, snap, or jump.

---

## 10. Browser Throttling of `requestAnimationFrame`

On some Windows GPUs, Chrome/Edge throttle rAF more aggressively:

- inactive window  
- overlapping windows  
- power saving mode  
- multi-monitor setups  

If rAF timing drops → animation collapses.

### Test  
Open devtools and re-run the flyTo.  
If it suddenly becomes smoother → rAF throttling is confirmed.

---

## MOST LIKELY CAUSES FOR YOUR CURRENT APP

Ranked from highest probability:

1. **Duplicate or rapid-fire flyTo calls**  
2. **Layer or filter updates occurring during animation**  
3. **A map event (idle/move) interrupting animation**  
4. **Missing explicit duration → collapses to 0 ms on Windows**  
5. **DOM/UI updates during animation**  
6. **MapLibre version regressions**

---

## Next Step

If you want Claude (or me) to fix it directly:

Provide:

- the exact `flyTo` block  
- the event/click handler that triggers it  
- the MapLibre version  
- list of layers being added/updated at the moment of interaction  

Once we see those, the exact cause can be pinpointed and patched.