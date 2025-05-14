<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import devData from '../data/dev_pts.json';

  let svg;

  onMount(() => {
    if (!devData || !devData.features) {
      console.error('Invalid data format');
      return;
    }

    // Extract properties and group by borough and year
    const properties = devData.features.map(f => f.properties);
    const groupedData = d3.rollups(
      properties,
      v => ({
        avg_units_ha: d3.mean(v, d => d.Units_HA)
      }),
      d => d.boro_name,
      d => d.year
    ).map(([boro, yearData]) => ({
      borough: boro,
      values: yearData.map(([year, data]) => ({
        year: +year,
        avg_units_ha: data.avg_units_ha
      }))
    }));

    // Set up dimensions
    const containerWidth = svg.parentNode.clientWidth;
    const margin = { top: 40, right: 120, bottom: 40, left: 60 };
    const width = containerWidth - margin.left - margin.right;
    const height = containerWidth * 0.5 - margin.top - margin.bottom;

    // Clear existing content
    d3.select(svg).selectAll("*").remove();

    // Create SVG
    const svgElement = d3.select(svg)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Set up scales
    const x = d3.scaleLinear()
      .domain(d3.extent(properties, d => d.year))
      .range([0, width]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(properties, d => d.Units_HA)])
      .nice()
      .range([height, 0]);

    // Add axes
    svgElement.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(5).tickFormat(d3.format('d')));

    svgElement.append('g')
      .call(d3.axisLeft(y).ticks(5));

    // Create line generator
    const line = d3.line()
      .x(d => x(d.year))
      .y(d => y(d.avg_units_ha));

    // Add lines for each borough
    groupedData.forEach(borough => {
      const path = svgElement.append('path')
        .datum(borough.values)
        .attr('fill', 'none')
        .attr('stroke', '#FF5A30')
        .attr('stroke-width', 2)
        .attr('d', line);

      // Add points and labels
      borough.values.forEach(d => {
        svgElement.append('circle')
          .attr('cx', x(d.year))
          .attr('cy', y(d.avg_units_ha))
          .attr('r', 3)
          .attr('fill', '#FF5A30');

        svgElement.append('text')
          .attr('x', x(d.year))
          .attr('y', y(d.avg_units_ha) - 10)
          .attr('text-anchor', 'middle')
          .attr('font-size', '10px')
          .text(d3.format('.1f')(d.avg_units_ha));
      });

      // Add borough name at the end of line
      const lastPoint = borough.values[borough.values.length - 1];
      svgElement.append('text')
        .attr('x', x(lastPoint.year) + 10)
        .attr('y', y(lastPoint.avg_units_ha))
        .attr('dominant-baseline', 'middle')
        .attr('font-size', '12px')
        .attr('font-weight', 'bold')
        .text(borough.borough);
    });
  });
</script>

<div class="chart-container">
  <svg bind:this={svg}></svg>
</div>

<style>
  .chart-container {
    width: 100%;
    max-width: 1000px;
    margin: 0 auto;
  }
  
  svg {
    width: 100%;
    height: auto;
  }
</style>
