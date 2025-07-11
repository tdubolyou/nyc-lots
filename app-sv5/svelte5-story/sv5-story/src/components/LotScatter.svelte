<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import lotsData from '../data/lots_pts.json';
  
    let svg;
    let tooltipVisible = false;
    let tooltipText = '';
    let tooltipX = 0;
    let tooltipY = 0;
  
    onMount(() => {
      if (!lotsData || !lotsData.features) {
        console.error('Invalid data format');
        return;
      }

      // Extract properties from features
      const properties = lotsData.features.map(f => f.properties);
      
      // Step 1: Aggregate the data by borough
      const boroughs = d3.rollups(
        properties,
        v => ({
          number_of_lots: v.length,
          average_lot_size: d3.mean(v, d => d.Area_HA * 10000), // convert hectares to square meters
          total_area: d3.sum(v, d => d.Area_HA * 10000)
        }),
        d => d.boro_name
      ).map(([key, values]) => ({ boro: key, ...values }));

      // Get the container's width and calculate dimensions based on a fixed aspect ratio
      const containerWidth = svg.parentNode.clientWidth;
      const margin = { top: 40, right: 30, bottom: 60, left: 80 };
      const totalWidth = containerWidth;
      const totalHeight = containerWidth * 0.6667; // Same aspect ratio as BoroChart
      const width = totalWidth - margin.left - margin.right;
      const height = totalHeight - margin.top - margin.bottom;
  
      // Clear any existing content
      d3.select(svg).selectAll("*").remove();
  
      // Create the SVG container with responsive sizing
      const svgElement = d3.select(svg)
        .attr('width', totalWidth)
        .attr('height', totalHeight)
        .attr('viewBox', `0 0 ${totalWidth} ${totalHeight}`)
        .attr('preserveAspectRatio', 'xMidYMid meet')
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
  
      // Define scales
      const x = d3.scaleLinear()
        .domain([0, d3.max(boroughs, d => d.number_of_lots)]).nice()
        .range([0, width]);
  
      const y = d3.scaleLinear()
        .domain([0, d3.max(boroughs, d => d.average_lot_size)]).nice()
        .range([height, 0]);
  
      const r = d3.scaleSqrt()
        .domain([0, d3.max(boroughs, d => d.total_area)])
        .range([5, 30]);
  
      // Add subtle grid lines
      const makeXGridlines = () => d3.axisBottom(x).ticks(5);
      const makeYGridlines = () => d3.axisLeft(y).ticks(5);
  
      svgElement.append('g')
        .attr('class', 'grid')
        .attr('transform', `translate(0,${height})`)
        .call(makeXGridlines()
          .tickSize(-height)
          .tickFormat('')
        );
  
      svgElement.append('g')
        .attr('class', 'grid')
        .call(makeYGridlines()
          .tickSize(-width)
          .tickFormat('')
        );
  
      // Draw axes with styled ticks
      svgElement.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll('text')
        .style('font-family', 'Barlow, sans-serif')
        .style('font-size', '12px');
  
      svgElement.append('g')
        .attr('class', 'y-axis')
        .call(d3.axisLeft(y))
        .selectAll('text')
        .style('font-family', 'Barlow, sans-serif')
        .style('font-size', '12px');
  
      // Add axis labels
      svgElement.append('text')
        .attr('x', width / 2)
        .attr('y', height + margin.bottom - 10)
        .attr('text-anchor', 'middle')
        .style('font-family', 'Barlow, sans-serif')
        .style('font-size', '14px')
        .style('font-weight', '700')
        .text('Number of Lots');
  
      svgElement.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', -margin.left + 20)
        .attr('x', -height / 2)
        .attr('text-anchor', 'middle')
        .style('font-family', 'Barlow, sans-serif')
        .style('font-size', '14px')
        .style('font-weight', '700')
        .text('Average Lot Size (sq m)');
  
      // Add bubbles
      svgElement.selectAll('circle')
        .data(boroughs)
        .join('circle')
        .attr('cx', d => x(d.number_of_lots))
        .attr('cy', d => y(d.average_lot_size))
        .attr('r', d => r(d.total_area))
        .attr('fill', '#FF3300')
        .attr('opacity', 0.6)
        .attr('stroke', '#FF3300')
        .attr('stroke-width', 1)
        .style('cursor', 'pointer');
  
      // Add borough labels
      svgElement.selectAll('text.boro-label')
        .data(boroughs)
        .join('text')
        .attr('class', 'boro-label')
        .attr('x', d => x(d.number_of_lots))
        .attr('y', d => y(d.average_lot_size))
        .attr('dy', '-1em')
        .attr('text-anchor', 'middle')
        .style('font-family', 'Barlow, sans-serif')
        .style('font-size', '12px')
        .style('font-weight', '700')
        .style('fill', '#333')
        .text(d => d.boro);
  
      // Add title
      svgElement.append('text')
        .attr('x', width / 2)
        .attr('y', -margin.top/2)
        .attr('text-anchor', 'middle')
        .style('font-family', 'Barlow, sans-serif')
        .style('font-size', '16px')
        .style('font-weight', '700')
        .text('Parking Lot Distribution by Borough');
  
      svgElement.selectAll('circle')
        .on('mouseover', function(event, d) {
          // Visual hover effects
          d3.select(this)
            .attr('opacity', 0.9)
            // .attr('stroke-width', 2)
            // .attr('stroke', '#000000FF');
          
          // Show tooltip
          tooltipText = `${d.boro}\nNumber of lots: ${d3.format(',')(d.number_of_lots)}\nAvg lot size: ${d3.format(',.0f')(d.average_lot_size)} sqm\nTotal area: ${d3.format(',.0f')(d.total_area)} sqm`;
          tooltipVisible = true;
          tooltipX = event.pageX + 15;
          tooltipY = event.pageY - 50;
        })
        .on('mousemove', (event) => {
          tooltipX = event.pageX + 15;
          tooltipY = event.pageY - 50;
        })
        .on('mouseout', function() {
          // Reset visual hover effects
          d3.select(this)
            .attr('opacity', 0.6)
            .attr('stroke-width', 1)
            .attr('stroke', '#FF3300');
          
          // Hide tooltip
          tooltipVisible = false;
        });
    });
  </script>
  
  <div class="chart-container">
    <svg bind:this={svg}></svg>
  </div>
  
  {#if tooltipVisible}
    <div class="tooltip" style="left: {tooltipX}px; top: {tooltipY}px;">
      {#each tooltipText.split('\n') as line}
        {#if line.includes(':')}
          <div><strong>{line.split(':')[0]}:</strong> {line.split(':')[1]}</div>
        {:else}
          <div><strong>{line}</strong></div>
        {/if}
      {/each}
    </div>
  {/if}
  
  <style>
    .chart-container {
      background: #ffffff;
      padding: 1rem;
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      width: 100%;
      max-width: 100%;
    }
    svg {
      width: 100%;
      height: 100%;
      font-family: 'Barlow', sans-serif;
    }
    .tooltip {
      position: fixed;
      padding: 8px;
      background: white;
      border: 1px solid #ddd;
      border-radius: 4px;
      pointer-events: none;
      font-family: 'Barlow', sans-serif;
      font-size: 12px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      z-index: 1000;
      white-space: nowrap;
      max-width: 200px;
      color: #333;
      background: #ffffff;
    }
    :global(.chart-container .domain) {
      stroke: #cccccc;
    }
    :global(.chart-container .tick line) {
      stroke: #cccccc;
    }
    :global(.chart-container .grid line) {
      stroke: #eeeeee;
    }
    :global(.chart-container .grid path) {
      stroke-width: 0;
    }
    :global(.chart-container .tick text) {
      fill: #666666;
    }
  </style>