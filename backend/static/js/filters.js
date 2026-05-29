/**
 * CrimeScope Intel — Cybercrime Intelligence Dashboard
 * Central Reactive Filters & Dashboard Lifecycle State Manager
 */

document.addEventListener("DOMContentLoaded", async () => {
  // Ensure elements exist (we are on dashboard view)
  const yearFilter = document.getElementById("yearFilter");
  const cityFilter = document.getElementById("cityFilter");
  const crimeTypeFilter = document.getElementById("crimeTypeFilter");
  const resetBtn = document.getElementById("resetFilters");
  const spinner = document.getElementById("filterSpinner");

  if (!yearFilter || !cityFilter || !crimeTypeFilter) {
    console.log("Ingestion layout. Terminating filter reactive handlers.");
    return;
  }

  console.log("Reactive Filtering engine loading. Preparing dropdown parameters...");

  // ═══════════════════ CENTRAL LOGGING FEED INTEGRATION ═══════════════════
  const appendTerminalLog = (logText, type = "info") => {
    const terminalBody = document.querySelector(".terminal-body");
    if (!terminalBody) return;

    const now = new Date();
    const timeStr = now.toTimeString().split(" ")[0];
    let typeSpan = `<span class="t-info">[INFO]</span>`;

    if (type === "success") typeSpan = `<span class="t-success">[OK]</span>`;
    if (type === "warning") typeSpan = `<span class="t-warning">[WARN]</span>`;

    const logLine = document.createElement("p");
    logLine.className = "t-line";
    logLine.innerHTML = `<span class="t-time">[${timeStr}]</span> ${typeSpan} ${logText}`;
    
    const blinkLine = terminalBody.querySelector(".blink-line");
    if (blinkLine) {
      terminalBody.insertBefore(logLine, blinkLine);
    } else {
      terminalBody.appendChild(logLine);
    }
    terminalBody.scrollTop = terminalBody.scrollHeight;
  };

  // ═══════════════════ STATE LOADING OVERLAY CONTROLLERS ═══════════════════
  const setLoadingState = (isLoading) => {
    yearFilter.disabled = isLoading;
    cityFilter.disabled = isLoading;
    crimeTypeFilter.disabled = isLoading;
    if (resetBtn) resetBtn.disabled = isLoading;

    if (spinner) {
      spinner.style.display = isLoading ? "inline-flex" : "none";
    }
  };

  // ═══════════════════ DYNAMIC DROPDOWN POPULATOR ═══════════════════
  const populateDropdowns = async () => {
    setLoadingState(true);
    appendTerminalLog("Ingesting dropdown option parameters...", "info");

    const options = await window.CrimeScopeAPI.fetchFilterOptions();
    if (!options) {
      appendTerminalLog("Failed to fetch dynamic filter options.", "warning");
      setLoadingState(false);
      return;
    }

    // Populate Year Dropdown
    if (options.years) {
      options.years.forEach(yr => {
        const opt = document.createElement("option");
        opt.value = yr;
        opt.innerText = yr;
        yearFilter.appendChild(opt);
      });
    }

    // Populate City Dropdown
    if (options.cities) {
      options.cities.forEach(city => {
        const opt = document.createElement("option");
        opt.value = city;
        opt.innerText = city;
        cityFilter.appendChild(opt);
      });
    }

    // Populate Crime Type Dropdown
    if (options.crime_types) {
      options.crime_types.forEach(type => {
        const opt = document.createElement("option");
        opt.value = type;
        opt.innerText = type;
        crimeTypeFilter.appendChild(opt);
      });
    }

    appendTerminalLog("Dynamic dropdown selectors populated successfully.", "success");
    setLoadingState(false);
  };

  // Trigger populating dropdown options immediately
  await populateDropdowns();

  // ═══════════════════ KPI CARD DOM UPDATING & COUNT ANIMATIONS ═══════════════════
  const animateValue = (el, start, end, duration, format = false, isRate = false) => {
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      const current = progress * (end - start) + start;
      
      if (isRate) {
        el.innerText = `${current.toFixed(1)}%`;
      } else if (format) {
        el.innerText = Math.floor(current).toLocaleString();
      } else {
        el.innerText = Math.floor(current);
      }
      
      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        if (isRate) {
          el.innerText = `${end.toFixed(1)}%`;
        } else {
          el.innerText = format ? end.toLocaleString() : end;
        }
      }
    };
    window.requestAnimationFrame(step);
  };

  const updateKPICards = (summary) => {
    const totalCasesEl = document.querySelector(".kpi-card-glow-cyan .kpi-value, .card-glow-cyan:first-child .kpi-value");
    const closedCasesEl = document.querySelector(".card-glow-emerald .kpi-value");
    const openCasesEl = document.querySelector(".card-glow-yellow .kpi-value");
    const topCityEl = document.querySelector(".card-glow-rose .kpi-value");
    const topCrimeEl = document.querySelector(".card-glow-purple .kpi-value");
    const closureRateEl = document.querySelector(".kpi-card:last-child .kpi-value, .card-glow-cyan:last-child .kpi-value");

    if (summary) {
      // 1. Total Cases
      if (totalCasesEl) {
        const target = parseInt(summary.total_cases) || 0;
        animateValue(totalCasesEl, 0, target, 1000, true);
      }

      // 2. Closed Cases
      if (closedCasesEl) {
        const target = parseInt(summary.closed_cases) || 0;
        animateValue(closedCasesEl, 0, target, 1000, true);
      }

      // 3. Open Cases
      if (openCasesEl) {
        const target = parseInt(summary.open_cases) || 0;
        animateValue(openCasesEl, 0, target, 1000, true);
      }

      // 4. Epicenter City (Text swap)
      if (topCityEl) {
        topCityEl.innerText = summary.top_city || "N/A";
        topCityEl.className = "kpi-value city-val text-glow-rose";
      }

      // 5. Epicenter Offense (Text swap)
      if (topCrimeEl) {
        topCrimeEl.innerText = summary.top_crime || "N/A";
        topCrimeEl.className = "kpi-value crime-val text-glow-purple";
      }

      // 6. Closure Rate
      if (closureRateEl && summary.closure_rate) {
        const targetPct = parseFloat(summary.closure_rate.replace(/[^\d.]/g, "")) || 0;
        animateValue(closureRateEl, 0, targetPct, 1000, false, true);
        
        // Update Subtitle
        const closedSub = document.querySelector(".card-glow-emerald .kpi-sub");
        if (closedSub) {
          closedSub.innerText = `Resolution rate: ${summary.closure_rate}`;
        }
      }
    }
  };

  // ═══════════════════ DYNAMIC CHART INSTANCE LIFECYCLE ═══════════════════
  const destroyActiveCharts = () => {
    if (window.CrimeScopeInstances) {
      Object.keys(window.CrimeScopeInstances).forEach(key => {
        if (window.CrimeScopeInstances[key] && typeof window.CrimeScopeInstances[key].destroy === 'function') {
          window.CrimeScopeInstances[key].destroy();
          window.CrimeScopeInstances[key] = null;
        }
      });
    }
  };

  // ═══════════════════ CENTRAL TELEMETRY DASHBOARD RE-RENDERER ═══════════════════
  const updateDashboard = async () => {
    setLoadingState(true);
    
    const year = yearFilter.value;
    const city = cityFilter.value;
    const crimeType = crimeTypeFilter.value;

    appendTerminalLog(`Applying telemetry filter constraints: [Yr: ${year}, City: ${city.toUpperCase()}, Type: ${crimeType.toUpperCase()}]`, "warning");

    const data = await window.CrimeScopeAPI.fetchFilteredData(year, city, crimeType);
    
    if (!data) {
      appendTerminalLog("Failed to retrieve filtered dynamic dataset.", "warning");
      setLoadingState(false);
      return;
    }

    // 1. Safely destroy active Chart.js configurations to prevent visual bugs
    destroyActiveCharts();

    // 2. Perform smooth DOM updates for all 6 KPI cards
    updateKPICards(data.summary);
    
    // Check if the dataset returned is completely empty
    const totalRecords = data.summary ? parseInt(data.summary.total_cases) : 0;
    if (totalRecords === 0) {
      appendTerminalLog("Filter criteria returned zero active records. Visual charts disabled.", "warning");
      
      // Clear heatmaps and outputs
      const heatmapGrid = document.getElementById("heatmapGrid");
      if (heatmapGrid) heatmapGrid.innerHTML = `<p class="text-muted" style="padding:40px;text-align:center;"><i class="fa-solid fa-triangle-exclamation text-glow-rose"></i> Zero incident logs match the criteria.</p>`;
      
      setLoadingState(false);
      return;
    }

    // 3. Re-render dynamic Chart.js canvas elements
    window.CrimeScopeInstances = window.CrimeScopeInstances || {};

    if (data.crime_trends && document.getElementById("trendsChart")) {
      window.CrimeScopeInstances.trends = window.CrimeScopeCharts.createTrendsChart("trendsChart", data.crime_trends);
    }
    if (data.crime_types && document.getElementById("typesChart")) {
      window.CrimeScopeInstances.types = window.CrimeScopeCharts.createTypesChart("typesChart", data.crime_types);
    }
    if (data.top_cities && document.getElementById("citiesChart")) {
      window.CrimeScopeInstances.cities = window.CrimeScopeCharts.createCitiesChart("citiesChart", data.top_cities);
    }
    if (data.weapons && document.getElementById("weaponsChart")) {
      window.CrimeScopeInstances.weapons = window.CrimeScopeCharts.createWeaponsChart("weaponsChart", data.weapons);
    }
    if (data.heatmap && document.getElementById("heatmapGrid")) {
      window.CrimeScopeCharts.renderHeatmapGrid("heatmapGrid", data.heatmap);
    }
    if (data.predictions && document.getElementById("predictionsChart")) {
      window.CrimeScopeInstances.predictions = window.CrimeScopeCharts.createPredictionsChart("predictionsChart", data.predictions);
      
      // Update predictions panel texts
      const scoreEl = document.querySelector(".meta-item:nth-child(2) .meta-val");
      if (scoreEl && data.predictions.r2_score) {
        scoreEl.innerText = data.predictions.r2_score;
      }
    }
    if (data.correlation && document.getElementById("correlationChart")) {
      window.CrimeScopeInstances.correlation = window.CrimeScopeCharts.createScatterChart("correlationChart", data.correlation);
    }

    // Phase 4 Upgrade: Sync AI Prediction Command Center UI
    if (window.CrimeScopeML && typeof window.CrimeScopeML.init === 'function') {
      await window.CrimeScopeML.init();
    }

    // Phase 5 Upgrade: Sync AI Insights & Live Alerts feeds reactively
    if (window.CrimeScopeInsights && typeof window.CrimeScopeInsights.fetchAndRender === 'function') {
      appendTerminalLog("Synthesizing dynamic AI natural-language insights...", "info");
      await window.CrimeScopeInsights.fetchAndRender(year, city, crimeType);
    }
    if (window.CrimeScopeAlerts && typeof window.CrimeScopeAlerts.fetchAndRender === 'function') {
      appendTerminalLog("Synthesizing real-time SOC threat intel alerts...", "info");
      await window.CrimeScopeAlerts.fetchAndRender(year, city, crimeType);
    }

    appendTerminalLog(`Successfully synthesized telemetry feeds. Counted ${totalRecords.toLocaleString()} active logs.`, "success");
    setLoadingState(false);
  };

  // ═══════════════════ EVENT REGISTRATIONS ═══════════════════
  yearFilter.addEventListener("change", updateDashboard);
  cityFilter.addEventListener("change", updateDashboard);
  crimeTypeFilter.addEventListener("change", updateDashboard);

  if (resetBtn) {
    resetBtn.addEventListener("click", async () => {
      if (yearFilter.value === "All" && cityFilter.value === "All" && crimeTypeFilter.value === "All") {
        return; // Already reset
      }

      appendTerminalLog("Resetting all active filter constraints back to baseline...", "warning");
      yearFilter.value = "All";
      cityFilter.value = "All";
      crimeTypeFilter.value = "All";

      await updateDashboard();
    });
  }

});
