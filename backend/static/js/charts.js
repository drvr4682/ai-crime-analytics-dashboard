/**
 * CrimeScope Intel — Cybercrime Intelligence Dashboard
 * High-Fidelity Chart.js Visualizer Configurations
 */

// Global Chart.js Configuration Overrides for Premium Dark Cyberpunk Theme
if (typeof Chart !== 'undefined') {
  Chart.defaults.font.family = "'Outfit', sans-serif";
  Chart.defaults.color = "#64748b"; // --text-muted
  Chart.defaults.plugins.legend.labels.color = "#f1f5f9"; // --text-main
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.boxWidth = 10;
  Chart.defaults.plugins.legend.labels.padding = 15;
  Chart.defaults.responsive = true;
  Chart.defaults.maintainAspectRatio = false;
}

window.CrimeScopeCharts = {
  // Theme Color Presets
  colors: {
    cyan: '#00f2fe',
    emerald: '#00f5c4',
    rose: '#ff3366',
    yellow: '#ffd166',
    purple: '#8b5cf6',
    muted: '#475569',
    grid: 'rgba(255, 255, 255, 0.05)',
    tooltipBg: 'rgba(5, 8, 17, 0.95)',
    tooltipBorder: 'rgba(0, 242, 254, 0.35)'
  },

  // 1. Crime Trends (Monthly Line Chart)
  createTrendsChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Create subtle glow gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(0, 242, 254, 0.2)');
    gradient.addColorStop(1, 'rgba(0, 242, 254, 0.0)');

    return new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.months || [],
        datasets: [{
          label: 'Total Incidents',
          data: data.counts || [],
          borderColor: this.colors.cyan,
          borderWidth: 3,
          pointBackgroundColor: this.colors.cyan,
          pointBorderColor: '#090d16',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7,
          backgroundColor: gradient,
          fill: true,
          tension: 0.4 // Smooth Bezier curves
        }]
      },
      options: {
        plugins: {
          legend: { display: false },
          tooltip: this.getTooltipStyle()
        },
        scales: this.getGridScales()
      }
    });
  },

  // 2. Crime Distribution (Doughnut Chart)
  createTypesChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const palette = [
      this.colors.rose,
      this.colors.cyan,
      this.colors.purple,
      this.colors.yellow,
      this.colors.emerald,
      this.colors.muted
    ];

    return new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: data.crime_types || [],
        datasets: [{
          data: data.counts || [],
          backgroundColor: palette.slice(0, data.counts.length),
          borderWidth: 2,
          borderColor: '#0d1321',
          hoverOffset: 12
        }]
      },
      options: {
        plugins: {
          legend: {
            position: 'right',
            labels: {
              boxWidth: 8,
              font: { size: 12, weight: 600 }
            }
          },
          tooltip: {
            ...this.getTooltipStyle(),
            callbacks: {
              label: function(context) {
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const val = context.raw;
                const pct = ((val / total) * 100).toFixed(1);
                return ` ${context.label}: ${val.toLocaleString()} (${pct}%)`;
              }
            }
          }
        },
        cutout: '65%'
      }
    });
  },

  // 3. Top 10 Cities (Vertical Bar Chart)
  createCitiesChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const barGradients = (data.counts || []).map((_, idx) => {
      const g = ctx.createLinearGradient(0, 0, 0, 300);
      // Give the top city a highly glowing rose hue
      if (idx === 0) {
        g.addColorStop(0, this.colors.rose);
        g.addColorStop(1, 'rgba(255, 51, 102, 0.2)');
      } else {
        g.addColorStop(0, this.colors.cyan);
        g.addColorStop(1, 'rgba(0, 242, 254, 0.2)');
      }
      return g;
    });

    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.cities || [],
        datasets: [{
          label: 'Total Incidents',
          data: data.counts || [],
          backgroundColor: barGradients,
          borderRadius: 4,
          borderWidth: 0,
          barPercentage: 0.6
        }]
      },
      options: {
        plugins: {
          legend: { display: false },
          tooltip: this.getTooltipStyle()
        },
        scales: this.getGridScales()
      }
    });
  },

  // 4. Weapons Involvements (Horizontal Bar Chart)
  createWeaponsChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const gradient = ctx.createLinearGradient(0, 0, 300, 0);
    gradient.addColorStop(0, 'rgba(0, 255, 196, 0.2)');
    gradient.addColorStop(1, this.colors.emerald);

    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.weapons || [],
        datasets: [{
          label: 'Weapon Utilizations',
          data: data.counts || [],
          backgroundColor: gradient,
          borderRadius: 4,
          borderWidth: 0,
          barPercentage: 0.55
        }]
      },
      options: {
        indexAxis: 'y', // Makes the chart horizontal
        plugins: {
          legend: { display: false },
          tooltip: this.getTooltipStyle()
        },
        scales: this.getGridScales()
      }
    });
  },

  // 5. ML Forecast Horizon (Mixed Line & Scatter Predictions Chart)
  createPredictionsChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    const historicalData = (data.historical_labels || []).map((yr, idx) => ({
      x: yr,
      y: data.historical_values[idx]
    }));
    
    const predictedData = (data.predicted_labels || []).map((yr, idx) => ({
      x: yr,
      y: data.predicted_values[idx]
    }));

    // Connect lines smoothly
    const fullLineData = [...historicalData];
    if (predictedData.length > 0 && historicalData.length > 0) {
      fullLineData.push(predictedData[0]); // connect trend line
    }
    const predictedLineData = predictedData.length > 0 ? [historicalData[historicalData.length - 1], ...predictedData] : [];

    return new Chart(ctx, {
      type: 'line',
      data: {
        datasets: [
          {
            label: 'Historical Crimes',
            data: historicalData,
            borderColor: this.colors.cyan,
            backgroundColor: 'rgba(0, 242, 254, 0.1)',
            borderWidth: 3,
            fill: false,
            tension: 0.35,
            pointRadius: 4,
            pointBackgroundColor: this.colors.cyan
          },
          {
            label: 'Forecast Projection',
            data: predictedLineData,
            borderColor: this.colors.rose,
            borderDash: [6, 6], // Dashed line for forecast
            borderWidth: 3,
            fill: false,
            tension: 0.35,
            pointRadius: 0 // handled by scatter plot below
          },
          {
            label: 'Forecast Target',
            type: 'scatter',
            data: predictedData,
            backgroundColor: this.colors.rose,
            borderColor: '#090d16',
            borderWidth: 2,
            pointRadius: 7,
            pointHoverRadius: 9,
            showLine: false
          }
        ]
      },
      options: {
        plugins: {
          legend: {
            position: 'top',
            labels: { font: { size: 11, weight: 600 } }
          },
          tooltip: {
            ...this.getTooltipStyle(),
            callbacks: {
              label: function(context) {
                return ` ${context.dataset.label}: ${context.raw.y.toLocaleString()} Cases (${context.raw.x})`;
              }
            }
          }
        },
        scales: {
          x: {
            type: 'linear',
            position: 'bottom',
            grid: { color: this.colors.grid, drawTicks: false },
            ticks: {
              color: '#64748b',
              stepSize: 1,
              font: { weight: 600 },
              callback: val => val.toFixed(0) // Render year integers
            }
          },
          y: {
            grid: { color: this.colors.grid, drawTicks: false },
            ticks: { color: '#64748b', font: { weight: 600 } }
          }
        }
      }
    });
  },

  // 6. Demographics Correlation (Multi-Colored Scatter Chart)
  createScatterChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Group sample points by their general Crime Domain
    const groups = {};
    (data.data || []).forEach(pt => {
      if (!groups[pt.group]) groups[pt.group] = [];
      groups[pt.group].push({ x: pt.x, y: pt.y });
    });

    const paletteColors = [
      this.colors.cyan,
      this.colors.rose,
      this.colors.yellow,
      this.colors.purple,
      this.colors.emerald
    ];

    const datasets = Object.keys(groups).map((group, idx) => ({
      label: group,
      data: groups[group],
      backgroundColor: paletteColors[idx % paletteColors.length] + '8c', // 55% opacity
      borderColor: paletteColors[idx % paletteColors.length],
      borderWidth: 1,
      pointRadius: 4,
      pointHoverRadius: 6
    }));

    return new Chart(ctx, {
      type: 'scatter',
      data: { datasets },
      options: {
        plugins: {
          legend: {
            position: 'top',
            labels: { font: { size: 10, weight: 600 } }
          },
          tooltip: {
            ...this.getTooltipStyle(),
            callbacks: {
              label: function(context) {
                return ` Age: ${context.raw.x} yrs, Deployed: ${context.raw.y} officers [${context.dataset.label}]`;
              }
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: 'Victim Age Index', color: '#64748b', font: { size: 11, weight: 'bold' } },
            grid: { color: this.colors.grid, drawTicks: false },
            ticks: { color: '#64748b', font: { weight: 600 } }
          },
          y: {
            title: { display: true, text: 'Active Police Deployed', color: '#64748b', font: { size: 11, weight: 'bold' } },
            grid: { color: this.colors.grid, drawTicks: false },
            ticks: { color: '#64748b', font: { weight: 600 } }
          }
        }
      }
    });
  },

  // 7. Custom CSS Grid Heatmap programmatical renderer
  renderHeatmapGrid(containerId, data) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = ""; // Clear existing

    const cities = data.cities || [];
    const months = data.months || [];
    const matrix = data.matrix || [];

    if (cities.length === 0 || months.length === 0) {
      container.innerHTML = `<p class="text-muted" style="padding:20px;text-align:center;">Insufficient telemetry for Heatmap render</p>`;
      return;
    }

    // Configure the Grid template columns size
    container.style.gridTemplateColumns = `90px repeat(${cities.length}, 1fr)`;

    // 1. Create Top Left empty corner block
    const corner = document.createElement("div");
    corner.className = "heatmap-header-cell";
    corner.innerHTML = "MONTH";
    container.appendChild(corner);

    // 2. Append city columns header labels
    cities.forEach(city => {
      const header = document.createElement("div");
      header.className = "heatmap-header-cell";
      header.innerText = city;
      container.appendChild(header);
    });

    // Determine min/max values for thermal intensity mapping
    let maxCount = 1;
    matrix.forEach(row => {
      row.forEach(val => {
        if (val > maxCount) maxCount = val;
      });
    });

    // 3. Render Heatmap matrix row by row (Month label + Cell counts)
    months.forEach((month, mIdx) => {
      // Month label cell
      const monthCell = document.createElement("div");
      monthCell.className = "heatmap-label-cell";
      monthCell.innerText = month;
      container.appendChild(monthCell);

      // Cities counts cells
      cities.forEach((city, cIdx) => {
        const countVal = matrix[mIdx] && matrix[mIdx][cIdx] !== undefined ? matrix[mIdx][cIdx] : 0;
        
        // Calculate heat index scale 0-5
        const pct = countVal / maxCount;
        let heatClass = "heat-0";
        if (pct > 0.8) heatClass = "heat-5";
        else if (pct > 0.6) heatClass = "heat-4";
        else if (pct > 0.4) heatClass = "heat-3";
        else if (pct > 0.2) heatClass = "heat-2";
        else if (pct > 0.0) heatClass = "heat-1";

        const cell = document.createElement("div");
        cell.className = `heatmap-cell ${heatClass}`;
        cell.innerText = countVal;

        // Custom responsive glass tooltip elements
        const tooltip = document.createElement("div");
        tooltip.className = "heatmap-tooltip";
        tooltip.innerHTML = `<i class="fa-solid fa-map-pin text-glow-cyan"></i> <strong>${city}</strong> · ${month}<br><i class="fa-solid fa-folder-closed"></i> ${countVal.toLocaleString()} Incidents`;
        
        cell.appendChild(tooltip);
        container.appendChild(cell);
      });
    });
  },

  // Helpers
  getTooltipStyle() {
    return {
      enabled: true,
      backgroundColor: this.colors.tooltipBg,
      borderColor: this.colors.tooltipBorder,
      borderWidth: 1,
      titleFont: { size: 12, weight: 800 },
      titleColor: '#00f2fe',
      bodyColor: '#f1f5f9',
      bodyFont: { size: 12, weight: 600 },
      padding: 10,
      cornerRadius: 6,
      displayColors: false,
      caretSize: 6
    };
  },

  getGridScales() {
    return {
      x: {
        grid: { color: this.colors.grid, drawTicks: false },
        ticks: { color: '#64748b', font: { weight: 600 } }
      },
      y: {
        grid: { color: this.colors.grid, drawTicks: false },
        ticks: { color: '#64748b', font: { weight: 600 } }
      }
    };
  }
};
