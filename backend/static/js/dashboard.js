/**
 * CrimeScope Intel — Cybercrime Intelligence Dashboard
 * Core Glue & Page Controller
 */

document.addEventListener("DOMContentLoaded", async () => {
  // Check if we are on the dashboard view page (canvas nodes must be present)
  const isDashboardView = !!document.getElementById("trendsChart");
  if (!isDashboardView) {
    console.log("Ingestion mode loaded. Terminating chart controllers.");
    return;
  }

  console.log("Telemetry Dashboard mode loaded. Activating dynamic REST nodes...");

  // Reference the active console logger function if it exists inside base script.js
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

  appendTerminalLog("Fetching secure telemetry datasets...", "info");

  // Load and render all charts in parallel for speed optimization
  try {
    const fetchPromises = [
      window.CrimeScopeAPI.fetchCrimeTrends(),
      window.CrimeScopeAPI.fetchCrimeTypes(),
      window.CrimeScopeAPI.fetchTopCities(),
      window.CrimeScopeAPI.fetchWeapons(),
      window.CrimeScopeAPI.fetchHeatmap(),
      window.CrimeScopeAPI.fetchPredictions(),
      window.CrimeScopeAPI.fetchCorrelation()
    ];

    const [trends, types, cities, weapons, heatmap, predictions, correlation] = await Promise.all(fetchPromises);

    appendTerminalLog("Datasets fetched. Compiling interactive UI visual charts...", "success");

    // 1. Render Monthly trends line chart
    if (trends && document.getElementById("trendsChart")) {
      window.CrimeScopeCharts.createTrendsChart("trendsChart", trends);
      appendTerminalLog("Compiled Crime Evolution timeline coordinates.", "success");
    }

    // 2. Render Doughnut Crime Types chart
    if (types && document.getElementById("typesChart")) {
      window.CrimeScopeCharts.createTypesChart("typesChart", types);
      appendTerminalLog("Compiled Domain classification profiles.", "success");
    }

    // 3. Render Top 10 Cities vertical bar chart
    if (cities && document.getElementById("citiesChart")) {
      window.CrimeScopeCharts.createCitiesChart("citiesChart", cities);
      appendTerminalLog("Mapped top urban crime epicenters.", "success");
    }

    // 4. Render Weapons horizontal bar chart
    if (weapons && document.getElementById("weaponsChart")) {
      window.CrimeScopeCharts.createWeaponsChart("weaponsChart", weapons);
      appendTerminalLog("Mapped weaponry vector distribution indexes.", "success");
    }

    // 5. Render custom CSS Grid Heatmap
    if (heatmap && document.getElementById("heatmapGrid")) {
      window.CrimeScopeCharts.renderHeatmapGrid("heatmapGrid", heatmap);
      appendTerminalLog("Rendered City-Month thermal correlation matrix.", "success");
    }

    // 6. Render ML predictions Mixed Line chart
    if (predictions && document.getElementById("predictionsChart")) {
      window.CrimeScopeCharts.createPredictionsChart("predictionsChart", predictions);
      appendTerminalLog("Executed Linear regression model overlays.", "success");
    }

    // 7. Render Demographics scatter chart
    if (correlation && document.getElementById("correlationChart")) {
      window.CrimeScopeCharts.createScatterChart("correlationChart", correlation);
      appendTerminalLog("Mapped deployment-demographics scatter fields.", "success");
    }

    appendTerminalLog("Interactive telemetry fully synthesized. Ready for analysis.", "success");

  } catch (err) {
    console.error("Critical error building visual dashboard widgets:", err);
    appendTerminalLog("Fatal error rendering dynamic visual charts.", "warning");
  }
});
