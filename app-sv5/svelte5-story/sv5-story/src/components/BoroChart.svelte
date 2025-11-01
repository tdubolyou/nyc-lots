<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import lotsData from '../data/lots_pts.json';

  let data = [];
  let chart;

  onMount(() => {
    // Extract features and aggregate data by borough
    const features = lotsData.features.map(f => f.properties);
    data = d3.rollup(
      features,
      v => v.length,  // Count the records
      d => d.boro_name
    );
    data = Array.from(data, ([key, value]) => ({
      boro: key, 
      count: value
    }));
    
    // Sort data by count in descending order
    data.sort((a, b) => b.count - a.count);

    // Set up margins
    const margin = { top: 10, right: 30, bottom: 40, left: 0 };

    // Get the container's width and calculate dimensions based on a fixed aspect ratio
    const containerWidth = chart.clientWidth;
    // Original design used 600 x 400 so ratio = 400/600 = 0.6667
    const totalWidth = containerWidth;
    const totalHeight = containerWidth * 0.6667; // total svg height proportional to container width
    const width = totalWidth - margin.left - margin.right;
    const height = totalHeight - margin.top - margin.bottom;

    // Remove any existing SVG content
    d3.select(chart).selectAll("*").remove();

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
      .domain([0, d3.max(data, d => d.count)])
      .range([height, 0]);

    // svg.append('g')
    //   .call(d3.axisLeft(y).tickFormat('').tickSize(0));

    // Bars
    svg.selectAll('rect')
      .data(data)
      .join('rect')
        .attr('x', d => x(d.boro))
        .attr('y', d => y(d.count))
        .attr('width', x.bandwidth())
        .attr('height', d => height - y(d.count))
        .attr('fill', '#008080')
        .attr('opacity', 0.8);

    // Bar labels
    svg.selectAll('.bar-label')
      .data(data)
      .join('text')
        .attr('class', 'bar-label')
        .attr('x', d => x(d.boro) + x.bandwidth() / 2)
        .attr('y', d => y(d.count) + 20)  // Position inside the bar
        .attr('text-anchor', 'middle')
        .style('font-family', 'Barlow, sans-serif')
        .style('font-size', '14px')
        .style('font-weight', 'bold')
        .style('fill', 'white')
        .text(d => d.count);

    // Title
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', height + margin.bottom - 2)
      .attr('text-anchor', 'middle')
      .style('font-family', 'Barlow, sans-serif')
      .style('font-size', '14px')
      .style('font-weight', '700')
      .style('fill', '#b0b0b0')

      .text('Number of Parking Lots by Borough');

    // Y axis label
    // svg.append('text')
    //   .attr('transform', 'rotate(-90)')
    //   .attr('y', -margin.left)
    //   .attr('x', -height / 2)
    //   .attr('dy', '1em')
    //   .style('text-anchor', 'middle')
    //   .style('font-family', 'Barlow, sans-serif')
    //   .style('font-size', '14px')
    //   .text('Number of Lots');
  });
</script>

<div bind:this={chart} class="chart-container"></div>

<style>
  .chart-container {
    background: #ffffff;
    padding: 1rem;
    border-radius: 4px;
    /* box-shadow: 0 2px 4px rgba(0,0,0,0.1); */
    width: 100%;
    max-width: 100%;
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