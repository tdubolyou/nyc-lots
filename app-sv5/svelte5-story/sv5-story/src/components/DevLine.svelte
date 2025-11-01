<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import devData from '../data/dev_pts.json';

  let svg; // Bind to SVG element for D3 manipulation

  onMount(() => {
    if (!devData || !devData.features) {
      console.error('Invalid data format');
      return;
    }

    // ===========================================
    // DATA PROCESSING PHASE
    // ===========================================
    // Extract properties from GeoJSON features (each feature represents a development point)
    const properties = devData.features.map(f => f.properties);

    // Group data hierarchically: first by borough, then by year within each borough
    // This creates a nested structure for multi-line visualization
    const groupedData = d3.groups(properties, d => d.Borough)
      .map(([borough, boroughData]) => {
        // For each borough, group by year and calculate average density
        const yearlyData = d3.groups(boroughData, d => d.YearBuilt)
          .map(([year, yearData]) => ({
            year: +year % 100, // Convert to 2-digit year (e.g., 2015 → 15)
            avg_units_ha: d3.mean(yearData, d => d.UnitsHA) // Calculate mean density for this borough-year
          }))
          .sort((a, b) => a.year - b.year); // Sort chronologically for proper line drawing

        return {
          borough: borough,
          values: yearlyData // Array of {year, avg_units_ha} objects
        };
      });

    // ===========================================
    // SVG SETUP AND DIMENSIONS
    // ===========================================
    // Create responsive dimensions based on container width
    const containerWidth = svg.parentNode.clientWidth;
    const margin = { top: 60, right: 140, bottom: 60, left: 80 }; // Space for axes and labels
    const width = containerWidth - margin.left - margin.right;
    const height = containerWidth * 0.8 - margin.top - margin.bottom; // Maintain aspect ratio

    // Clear any existing content (important for re-renders)
    d3.select(svg).selectAll("*").remove();

    // Create main SVG group with margin transform (standard D3 pattern)
    const svgElement = d3.select(svg)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Add chart title
    svgElement.append('text')
      .attr('x', width / 2)
      .attr('y', -30)
      .attr('text-anchor', 'middle')
      .attr('font-size', '16px')
      .attr('font-weight', 'bold')
      .text('Density of Recent Housing');

    // ===========================================
    // SCALES SETUP
    // ===========================================
    // X-scale: maps years to horizontal pixel positions
    const x = d3.scaleLinear()
      .domain([
        d3.min(groupedData, d => d3.min(d.values, v => v.year)), // Earliest year across all boroughs
        d3.max(groupedData, d => d3.max(d.values, v => v.year))  // Latest year across all boroughs
      ])
      .range([0, width]); // Map to full width of chart area

    // Y-scale: maps density values to vertical pixel positions
    const y = d3.scaleLinear()
      .domain([0, d3.max(groupedData, d => d3.max(d.values, v => v.avg_units_ha))]) // Start at 0, max density
      .nice() // Round domain to nice numbers
      .range([height, 0]); // Invert: high values at top (SVG coordinates are flipped)

    // ===========================================
    // AXES CREATION
    // ===========================================
    // X-axis: horizontal axis at bottom showing years
    svgElement.append('g')
      .attr('transform', `translate(0,${height})`) // Position at bottom
      .call(d3.axisBottom(x).ticks(8).tickFormat(d => `'${d3.format('02d')(d)}`)) // Format as '15, '16, etc.
      .style('font-size', '12px')
      .call(g => g.select('.domain').attr('stroke-opacity', 0.2)) // Subtle axis line
      .call(g => g.selectAll('.tick line').attr('stroke-opacity', 0.2)); // Subtle tick marks

    // Y-axis: vertical axis on left showing density values
    svgElement.append('g')
      .call(d3.axisLeft(y).ticks(6))
      .style('font-size', '12px')
      .call(g => g.select('.domain').attr('stroke-opacity', 0.2))
      .call(g => g.selectAll('.tick line') // Extend tick lines across chart (grid lines)
        .attr('x2', width)
        .attr('stroke-opacity', 0.2));

    // Axis labels for clarity
    svgElement.append('text')
      .attr('x', -height/2)
      .attr('y', -60)
      .attr('transform', 'rotate(-90)') // Rotate for vertical text
      .attr('text-anchor', 'middle')
      .attr('font-size', '14px')
      .text('Average Units per Hectare');

    svgElement.append('text')
      .attr('x', width/2)
      .attr('y', height + 40)
      .attr('text-anchor', 'middle')
      .attr('font-size', '14px')
      .text('Year Built');

    // ===========================================
    // LINE GENERATOR
    // ===========================================
    // D3 line generator: converts data points to SVG path string
    const line = d3.line()
      .x(d => x(d.year))           // X position using year scale
      .y(d => y(d.avg_units_ha))   // Y position using density scale
      .curve(d3.curveMonotoneX);   // Smooth curve interpolation

    // ===========================================
    // SMART LABEL POSITIONING
    // ===========================================
    // Sort boroughs by their final density value to handle overlapping labels
    groupedData.sort((a, b) => {
      const aLastY = a.values[a.values.length - 1].avg_units_ha;
      const bLastY = b.values[b.values.length - 1].avg_units_ha;
      return bLastY - aLastY; // Highest density first
    });

    // ===========================================
    // DRAW LINES AND POINTS FOR EACH BOROUGH
    // ===========================================
    groupedData.forEach((borough, i) => {
      // Draw the line path for this borough
      svgElement.append('path')
        .datum(borough.values) // Bind the time series data
        .attr('fill', 'none')
        .attr('stroke', '#008080') // Consistent color for all boroughs
        .attr('stroke-width', 2.5)
        .attr('opacity', 0.8)
        .attr('d', line); // Use line generator to create path

      // ===========================================
      // INTERACTIVE POINTS
      // ===========================================
      // Create groups for each data point (allows multiple elements per point)
      const points = svgElement.selectAll(`.point-group-${borough.borough}`)
        .data(borough.values)
        .enter()
        .append('g')
        .attr('class', `point-group-${borough.borough}`);

      // Add circles at each data point
      points.append('circle')
        .attr('cx', d => x(d.year))
        .attr('cy', d => y(d.avg_units_ha))
        .attr('r', 3)
        .attr('fill', '#008080')
        .attr('opacity', 0.8);

      // Add value labels (hidden by default, shown on hover)
      points.append('text')
        .attr('x', d => x(d.year))
        .attr('y', d => y(d.avg_units_ha) - 12) // Position above point
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('font-weight', '500')
        .text(d => d3.format('.1f')(d.avg_units_ha)) // Format to 1 decimal place
        .style('opacity', 0); // Initially hidden

      // ===========================================
      // HOVER INTERACTIONS
      // ===========================================
      points.on('mouseenter', function() {
        // Show value label and enlarge point on hover
        d3.select(this).select('text')
          .style('opacity', 1);
        d3.select(this).select('circle')
          .attr('r', 5)
          .attr('opacity', 1);
      })
      .on('mouseleave', function() {
        // Hide label and restore point size
        d3.select(this).select('text')
          .style('opacity', 0);
        d3.select(this).select('circle')
          .attr('r', 3)
          .attr('opacity', 0.8);
      });

      // ===========================================
      // END-OF-LINE BOROUGH LABELS
      // ===========================================
      // Add borough name at the end of each line with smart positioning
      const lastPoint = borough.values[borough.values.length - 1];
      const labelHeight = 18; // Minimum spacing between labels
      const baseY = y(lastPoint.avg_units_ha); // Natural position based on data
      
      // Adjust label position to avoid overlaps with previous labels
      let labelY = baseY;
      if (i > 0) {
        const prevY = y(groupedData[i-1].values[groupedData[i-1].values.length-1].avg_units_ha);
        if (Math.abs(labelY - prevY) < labelHeight) {
          labelY = prevY + labelHeight; // Offset to avoid overlap
        }
      }
      
      // Draw connecting line if label was moved from natural position
      if (Math.abs(labelY - baseY) > 2) {
        svgElement.append('line')
          .attr('x1', x(lastPoint.year))     // Start at data point
          .attr('y1', baseY)
          .attr('x2', x(lastPoint.year) + 10) // Short horizontal line
          .attr('y2', labelY)
          .attr('stroke', '#008080')
          .attr('stroke-width', 1)
          .attr('opacity', 0.8);
      }
      
      // Add the borough name label
      svgElement.append('text')
        .attr('x', x(lastPoint.year) + 12) // Offset from line end
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
