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

    // Group and calculate averages by borough and year
    const groupedData = d3.groups(properties, d => d.Borough)
      .map(([borough, boroughData]) => {
        const yearlyData = d3.groups(boroughData, d => d.YearBuilt)
          .map(([year, yearData]) => ({
            year: +year % 100, // Convert to 2-digit year
            avg_units_ha: d3.mean(yearData, d => d.UnitsHA)
          }))
          .sort((a, b) => a.year - b.year); // Sort by year

        return {
          borough: borough,
          values: yearlyData
        };
      });

    // Set up dimensions - increased height multiplier
    const containerWidth = svg.parentNode.clientWidth;
    const margin = { top: 60, right: 140, bottom: 60, left: 80 }; // Increased margins
    const width = containerWidth - margin.left - margin.right;
    const height = containerWidth * 0.8 - margin.top - margin.bottom; // Increased height ratio

    // Clear existing content
    d3.select(svg).selectAll("*").remove();

    // Create SVG
    const svgElement = d3.select(svg)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Add title
    svgElement.append('text')
      .attr('x', width / 2)
      .attr('y', -30)
      .attr('text-anchor', 'middle')
      .attr('font-size', '16px')
      .attr('font-weight', 'bold')
      .text('Density of Recent Housing');

    // Set up scales
    const x = d3.scaleLinear()
      .domain([
        d3.min(groupedData, d => d3.min(d.values, v => v.year)),
        d3.max(groupedData, d => d3.max(d.values, v => v.year))
      ])
      .range([0, width]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(groupedData, d => d3.max(d.values, v => v.avg_units_ha))])
      .nice()
      .range([height, 0]);

    // Add axes with refined styling
    svgElement.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(8).tickFormat(d => `'${d3.format('02d')(d)}`))
      .style('font-size', '12px')
      .call(g => g.select('.domain').attr('stroke-opacity', 0.2))
      .call(g => g.selectAll('.tick line').attr('stroke-opacity', 0.2));

    svgElement.append('g')
      .call(d3.axisLeft(y).ticks(6))
      .style('font-size', '12px')
      .call(g => g.select('.domain').attr('stroke-opacity', 0.2))
      .call(g => g.selectAll('.tick line')
        .attr('x2', width)
        .attr('stroke-opacity', 0.2));

    // Add axis labels
    svgElement.append('text')
      .attr('x', -height/2)
      .attr('y', -60)
      .attr('transform', 'rotate(-90)')
      .attr('text-anchor', 'middle')
      .attr('font-size', '14px')
      .text('Average Units per Hectare');

    svgElement.append('text')
      .attr('x', width/2)
      .attr('y', height + 40)
      .attr('text-anchor', 'middle')
      .attr('font-size', '14px')
      .text('Year Built');

    // Create line generator with curve
    const line = d3.line()
      .x(d => x(d.year))
      .y(d => y(d.avg_units_ha))
      .curve(d3.curveMonotoneX);

    // Sort boroughs by final y-value to handle label placement
    groupedData.sort((a, b) => {
      const aLastY = a.values[a.values.length - 1].avg_units_ha;
      const bLastY = b.values[b.values.length - 1].avg_units_ha;
      return bLastY - aLastY;
    });

    // Add lines and points for each borough
    groupedData.forEach((borough, i) => {
      // Add the line
      svgElement.append('path')
        .datum(borough.values)
        .attr('fill', 'none')
        .attr('stroke', '#de4f31')
        .attr('stroke-width', 2.5)
        .attr('opacity', 0.8)
        .attr('d', line);

      // Create a group for each data point
      const points = svgElement.selectAll(`.point-group-${borough.borough}`)
        .data(borough.values)
        .enter()
        .append('g')
        .attr('class', `point-group-${borough.borough}`);

      // Add points
      points.append('circle')
        .attr('cx', d => x(d.year))
        .attr('cy', d => y(d.avg_units_ha))
        .attr('r', 3)
        .attr('fill', '#de4f31')
        .attr('opacity', 0.8);

      // Add labels (initially hidden)
      points.append('text')
        .attr('x', d => x(d.year))
        .attr('y', d => y(d.avg_units_ha) - 12)
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('font-weight', '500')
        .text(d => d3.format('.1f')(d.avg_units_ha))
        .style('opacity', 0);

      // Add hover interactions
      points.on('mouseenter', function() {
        d3.select(this).select('text')
          .style('opacity', 1);
        d3.select(this).select('circle')
          .attr('r', 5)
          .attr('opacity', 1);
      })
      .on('mouseleave', function() {
        d3.select(this).select('text')
          .style('opacity', 0);
        d3.select(this).select('circle')
          .attr('r', 3)
          .attr('opacity', 0.8);
      });

      // Add borough name at the end of line with smarter label placement
      const lastPoint = borough.values[borough.values.length - 1];
      const labelHeight = 18;
      const baseY = y(lastPoint.avg_units_ha);
      
      let labelY = baseY;
      if (i > 0) {
        const prevY = y(groupedData[i-1].values[groupedData[i-1].values.length-1].avg_units_ha);
        if (Math.abs(labelY - prevY) < labelHeight) {
          labelY = prevY + labelHeight;
        }
      }
      
      if (Math.abs(labelY - baseY) > 2) {
        svgElement.append('line')
          .attr('x1', x(lastPoint.year))
          .attr('y1', baseY)
          .attr('x2', x(lastPoint.year) + 10)
          .attr('y2', labelY)
          .attr('stroke', '#de4f31')
          .attr('stroke-width', 1)
          .attr('opacity', 0.8);
      }
      
      svgElement.append('text')
        .attr('x', x(lastPoint.year) + 12)
        .attr('y', labelY)
        .attr('dominant-baseline', 'middle')
        .attr('font-size', '14px')
        .attr('font-weight', '500')
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
    max-width: 1200px; /* Increased from 1000px */
    margin: 0 auto;
    padding: 20px;
    background-color: #ffffff;
  }
  
  svg {
    width: 100%;
    height: auto;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
</style>
