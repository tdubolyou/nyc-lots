<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import lotsData from '../data/lots_pts.json';

  let data = [];
  let chart;

  onMount(() => {
    // Extract features and prepare data for boxplots
    const features = lotsData.features.map(f => f.properties);
    
    // Group data by borough
    const boroughGroups = d3.group(features, d => d.boro_name);
    
    // Calculate quartiles etc for each borough and store raw values
    data = Array.from(boroughGroups, ([key, values]) => {
      const areaValues = values.map(d => d.Area_HA);
      const q1 = d3.quantile(areaValues, 0.25);
      const median = d3.quantile(areaValues, 0.5);
      const q3 = d3.quantile(areaValues, 0.75);
      const iqr = q3 - q1;
      const mean = d3.mean(areaValues);
      
      return {
        boro: key,
        q1: q1,
        median: median,
        q3: q3,
        mean: mean,
        points: areaValues // Store all points for this borough
      };
    });

    // Sort data by median in descending order
    data.sort((a, b) => b.median - a.median);

    // Set up margins
    const margin = { top: 10, right: 30, bottom: 40, left: 60 };

    // Get the container's width and calculate dimensions
    const containerWidth = chart.clientWidth;
    const totalWidth = containerWidth;
    const totalHeight = containerWidth * 0.6667;
    const width = totalWidth - margin.left - margin.right;
    const height = totalHeight - margin.top - margin.bottom;

    // Remove any existing SVG content
    d3.select(chart).selectAll("*").remove();

    // Create tooltip div
    const tooltip = d3.select("body") // Attach to body instead of chart
      .append("div")
      .attr("class", "tooltip")
      .style("position", "absolute")
      .style("background", "rgba(255, 255, 255, 0.9)")
      .style("padding", "8px")
      .style("border", "1px solid #ddd")
      .style("border-radius", "4px")
      .style("font-size", "12px")
      .style("pointer-events", "none")
      .style("opacity", 0)
      .style("z-index", 1000);

    // Append the responsive SVG
    const svg = d3.select(chart)
      .append('svg')
        .attr('width', totalWidth)
        .attr('height', totalHeight)
        .attr('viewBox', `0 0 ${totalWidth} ${totalHeight}`)
        .attr('preserveAspectRatio', 'xMidYMid meet')
      .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // X axis
    const x = d3.scaleBand()
      .range([0, width])
      .domain(data.map(d => d.boro))
      .padding(0.3);

    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
        .style('font-family', 'Barlow, sans-serif')
        .style('font-size', '12px');

    // Y axis
    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d3.max(d.points))])
      .range([height, 0]);

    // Add Y axis
    svg.append('g')
      .call(d3.axisLeft(y).tickFormat(d => `${d.toFixed(1)} ha`))
      .selectAll('text')
        .style('font-family', 'Barlow, sans-serif')
        .style('font-size', '12px');

    // Draw boxplots
    const boxWidth = x.bandwidth();

    // Box elements
    const boxPlots = svg.selectAll('.boxplot')
      .data(data)
      .join('g')
        .attr('class', 'boxplot')
        .attr('transform', d => `translate(${x(d.boro)},0)`);

    // Box from q1 to q3
    boxPlots.append('rect')
      .attr('x', 0)
      .attr('width', boxWidth)
      .attr('y', d => y(d.q3))
      .attr('height', d => y(d.q1) - y(d.q3))
      .attr('fill', '#008080')
      .attr('opacity', 0.7)
      .attr('stroke', '#008080')
      .attr('stroke-width', 1);

    // Median line
    boxPlots.append('line')
      .attr('x1', 0)
      .attr('x2', boxWidth)
      .attr('y1', d => y(d.median))
      .attr('y2', d => y(d.median))
      .style('stroke', '#FF3300')
      .style('stroke-width', 3);

    // Mean marker (diamond shape)
    boxPlots.append('path')
      .attr('d', d => {
        const meanY = y(d.mean);
        const size = 6;
        return `M ${boxWidth/2} ${meanY-size} L ${boxWidth/2+size} ${meanY} L ${boxWidth/2} ${meanY+size} L ${boxWidth/2-size} ${meanY} Z`;
      })
      .attr('fill', '#000')
      .attr('stroke', 'none');

    // Mean label
    boxPlots.append('text')
      .attr('x', boxWidth/2)
      .attr('y', d => y(d.mean) - 10)
      .attr('text-anchor', 'middle')
      .style('font-family', 'Barlow, sans-serif')
      .style('font-size', '10px')
      .text(d => `Mean: ${d.mean.toFixed(2)}`);

    // Add individual points with reduced opacity
    boxPlots.each(function(d) {
      const jitterWidth = boxWidth * 0.8;
      d3.select(this).selectAll('.point')
        .data(d.points)
        .join('circle')
          .attr('class', 'point')
          .attr('cx', () => boxWidth/2 + (Math.random() - 0.5) * jitterWidth)
          .attr('cy', value => y(value))
          .attr('r', 2)
          .attr('fill', '#008080')
          .attr('opacity', 0.3)
          .on('mouseover', function(event, value) {
            // Highlight point
            d3.select(this)
              .attr('r', 4)
              .attr('opacity', 1);
            
            // Show tooltip
            tooltip
              .style("opacity", 1)
              .html(`Size: ${value.toFixed(2)} hectares`)
              .style("left", (event.pageX + 10) + "px")
              .style("top", (event.pageY - 10) + "px");
          })
          .on('mouseout', function() {
            // Reset point
            d3.select(this)
              .attr('r', 2)
              .attr('opacity', 0.3);
              
            // Hide tooltip
            tooltip.style("opacity", 0);
          });
    });

    // Title
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', height + margin.bottom - 5)
      .attr('text-anchor', 'middle')
      .style('font-family', 'Barlow, sans-serif')
      .style('font-size', '10px')
      .style('font-weight', '700')
      .text('Distribution of Parking Lot Sizes (Hectares) by Borough');
  });
</script>

<div bind:this={chart} class="chart-container" role="img" aria-label="Box plot showing distribution of parking lot sizes by borough in hectares. Each borough displays median, quartiles, and outliers for lot size distribution."></div>

<style>
  .chart-container {
    background: #ffffff;
    padding: 1rem;
    border-radius: 4px;
    /* box-shadow: 0 2px 4px rgba(0,0,0,0.1); */
    width: 100%;
    max-width: 100%;
    position: relative;
  }
  :global(.chart-container .domain) {
    stroke: #cccccc;
  }
  :global(.chart-container .tick line) {
    stroke: #cccccc;
  }
  :global(.chart-container .tick text) {
    fill: #666666;
  }
</style>