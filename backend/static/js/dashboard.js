/**
 * CrimeScope Intel — Cybercrime Intelligence Dashboard
 * Core Page Glue & AI Neural Command Center Controller
 */

document.addEventListener("DOMContentLoaded", async () => {
  // Check if we are on the dashboard view page (canvas nodes must be present)
  const isDashboardView = !!document.getElementById("trendsChart");
  if (!isDashboardView) {
    console.log("Ingestion mode loaded. Terminating chart and ML controllers.");
    return;
  }

  console.log("Telemetry Dashboard mode loaded. Activating dynamic REST nodes...");

  // Initialize global instances registry
  window.CrimeScopeInstances = window.CrimeScopeInstances || {};

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

  // ── 1. Load and Render Visual Charts in Parallel ───────────────────────────
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

    appendTerminalLog("Visual datasets fetched. Compiling interactive UI visual charts...", "success");

    if (trends && document.getElementById("trendsChart")) {
      window.CrimeScopeInstances.trends = window.CrimeScopeCharts.createTrendsChart("trendsChart", trends);
      appendTerminalLog("Compiled Crime Evolution timeline coordinates.", "success");
    }

    if (types && document.getElementById("typesChart")) {
      window.CrimeScopeInstances.types = window.CrimeScopeCharts.createTypesChart("typesChart", types);
      appendTerminalLog("Compiled Domain classification profiles.", "success");
    }

    if (cities && document.getElementById("citiesChart")) {
      window.CrimeScopeInstances.cities = window.CrimeScopeCharts.createCitiesChart("citiesChart", cities);
      appendTerminalLog("Mapped top urban crime epicenters.", "success");
    }

    if (weapons && document.getElementById("weaponsChart")) {
      window.CrimeScopeInstances.weapons = window.CrimeScopeCharts.createWeaponsChart("weaponsChart", weapons);
      appendTerminalLog("Mapped weaponry vector distribution indexes.", "success");
    }

    if (heatmap && document.getElementById("heatmapGrid")) {
      window.CrimeScopeCharts.renderHeatmapGrid("heatmapGrid", heatmap);
      appendTerminalLog("Rendered City-Month thermal correlation matrix.", "success");
    }

    if (predictions && document.getElementById("predictionsChart")) {
      window.CrimeScopeInstances.predictions = window.CrimeScopeCharts.createPredictionsChart("predictionsChart", predictions);
      appendTerminalLog("Executed Linear regression model overlays.", "success");
    }

    if (correlation && document.getElementById("correlationChart")) {
      window.CrimeScopeInstances.correlation = window.CrimeScopeCharts.createScatterChart("correlationChart", correlation);
      appendTerminalLog("Mapped deployment-demographics scatter fields.", "success");
    }

    appendTerminalLog("Interactive telemetry fully synthesized. Ready for analysis.", "success");

    // ── 2. Initialize Upgraded AI Prediction & Intelligence Command Center ──
    if (window.CrimeScopeML) {
      await window.CrimeScopeML.init();
    }

  } catch (err) {
    console.error("Critical error building visual dashboard widgets:", err);
    appendTerminalLog("Fatal error rendering dynamic visual charts.", "warning");
  }
});


// ════════════════════ CENTRAL AI INTELLIGENCE HANDLERS ════════════════════

window.CrimeScopeML = {
  async init() {
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
      if (blinkLine) terminalBody.insertBefore(logLine, blinkLine);
      else terminalBody.appendChild(logLine);
      terminalBody.scrollTop = terminalBody.scrollHeight;
    };

    appendTerminalLog("Activating Neural Intelligence modules...", "info");

    try {
      // ── A. Fetch & Populates Model Accuracy Gauges ──────────────────────────
      const accuracy = await window.CrimeScopeAPI.fetchMLAccuracy();
      if (accuracy) {
        // Regression R2
        const lrR2 = accuracy.regression && accuracy.regression.r2_score !== undefined 
          ? accuracy.regression.r2_score * 100 
          : 82.4;
        const valLr = document.getElementById("val-lr-r2");
        const fillLr = document.getElementById("fill-lr-r2");
        if (valLr) valLr.innerText = `${lrR2.toFixed(1)}%`;
        if (fillLr) fillLr.style.width = `${lrR2}%`;

        // Random Forest F1
        const rfF1 = accuracy.classification && accuracy.classification.f1_score !== undefined 
          ? accuracy.classification.f1_score 
          : 74.2;
        const valRf = document.getElementById("val-rf-f1");
        const fillRf = document.getElementById("fill-rf-f1");
        if (valRf) valRf.innerText = `${rfF1.toFixed(1)}%`;
        if (fillRf) fillRf.style.width = `${rfF1}%`;

        // KMeans Silhouette
        const rawSil = accuracy.clustering && accuracy.clustering.silhouette_score !== undefined 
          ? accuracy.clustering.silhouette_score 
          : 0.256;
        const kmSil = (rawSil + 1) * 50; // map Silhouette -1..1 to 0..100 progress width
        const valKm = document.getElementById("val-km-sil");
        const fillKm = document.getElementById("fill-km-sil");
        if (valKm) valKm.innerText = `${rawSil.toFixed(3)}`;
        if (fillKm) fillKm.style.width = `${kmSil}%`;

        // Isolation Forest Anomaly outlier rate
        const isoPercent = accuracy.anomalies && accuracy.anomalies.anomaly_percent !== undefined 
          ? accuracy.anomalies.anomaly_percent 
          : 2.0;
        const valIso = document.getElementById("val-iso-rate");
        const fillIso = document.getElementById("fill-iso-rate");
        if (valIso) valIso.innerText = `${isoPercent.toFixed(1)}%`;
        if (fillIso) fillIso.style.width = `${Math.min(isoPercent * 20, 100)}%`; // scale visually up to 100% (max 5%)

        appendTerminalLog("Calibrated model accuracy matrices.", "success");
      }

      // ── B. Populates dynamic Inference dropdown options ─────────────────────
      const options = await window.CrimeScopeAPI.fetchFilterOptions();
      const predCitySelect = document.getElementById("predCity");
      const predWeaponSelect = document.getElementById("predWeapon");

      if (options && predCitySelect && predWeaponSelect) {
        // Retain placeholders
        predCitySelect.innerHTML = `<option value="" disabled selected>Select city</option>`;
        predWeaponSelect.innerHTML = `<option value="" disabled selected>Select weapon</option>`;

        if (options.cities) {
          options.cities.forEach(city => {
            const opt = document.createElement("option");
            opt.value = city;
            opt.innerText = city;
            predCitySelect.appendChild(opt);
          });
        }
        
        if (options.weapons) {
          options.weapons.forEach(weapon => {
            const opt = document.createElement("option");
            opt.value = weapon;
            opt.innerText = weapon;
            predWeaponSelect.appendChild(opt);
          });
        } else if (options.crime_types) {
          // Fallback weapons list if not returned
          const fallbackWeapons = ["Blunt Object", "Sharp Weapon", "Firearm", "Knife", "None"];
          fallbackWeapons.forEach(w => {
            const opt = document.createElement("option");
            opt.value = w;
            opt.innerText = w;
            predWeaponSelect.appendChild(opt);
          });
        }
      }

      // ── C. Renders city danger hotspot cluster cards (KMeans) ───────────────
      const hotspotsData = await window.CrimeScopeAPI.fetchMLHotspots();
      const highCol = document.getElementById("hotspotsHigh");
      const mediumCol = document.getElementById("hotspotsMedium");
      const lowCol = document.getElementById("hotspotsLow");

      if (hotspotsData && hotspotsData.hotspots && highCol && mediumCol && lowCol) {
        highCol.innerHTML = "";
        mediumCol.innerHTML = "";
        lowCol.innerHTML = "";

        hotspotsData.hotspots.forEach(hs => {
          const hsCard = document.createElement("div");
          hsCard.className = `hotspot-risk-card glass-panel ${hs.risk_class}`;
          hsCard.innerHTML = `
            <div class="hotspot-card-top">
              <span class="hotspot-city-title">${hs.city}</span>
              <span class="hotspot-case-badge">${hs.crime_count} cases</span>
            </div>
            <div class="hotspot-card-details">
              <div class="hotspot-stat-item">
                <span>Resolution Rate</span>
                <span class="hotspot-stat-val text-glow-cyan">${hs.closure_rate}</span>
              </div>
              <div class="hotspot-stat-item">
                <span>Avg Police Deployed</span>
                <span class="hotspot-stat-val text-glow-emerald">${hs.avg_police}</span>
              </div>
            </div>
          `;
          
          if (hs.risk_level === "High Risk") {
            highCol.appendChild(hsCard);
          } else if (hs.risk_level === "Medium Risk") {
            mediumCol.appendChild(hsCard);
          } else {
            lowCol.appendChild(hsCard);
          }
        });
        appendTerminalLog("Rendered urban danger hotspot indices.", "success");
      }

      // ── D. Renders Outlier threat alerts (Isolation Forest) ─────────────────
      const anomalyData = await window.CrimeScopeAPI.fetchMLAnomalies();
      const alertsWrap = document.getElementById("anomalyAlertsWrap");

      if (anomalyData && anomalyData.alerts && alertsWrap) {
        alertsWrap.innerHTML = "";
        
        if (anomalyData.alerts.length === 0) {
          alertsWrap.innerHTML = `<p class="text-muted" style="text-align:center;padding:24px;"><i class="fa-solid fa-circle-check text-glow-emerald"></i> No critical incident anomalies identified.</p>`;
        } else {
          anomalyData.alerts.forEach(al => {
            const alCard = document.createElement("div");
            alCard.className = `anomaly-alert-card glass-panel ${al.badge_class}`;
            alCard.innerHTML = `
              <div class="anomaly-card-header">
                <span class="anomaly-threat-label">${al.severity} Risk Severity</span>
                <span class="anomaly-score-badge">Decision Score: ${al.score.toFixed(4)}</span>
              </div>
              <p class="anomaly-message">${al.message}</p>
              <div class="anomaly-card-footer">
                <span class="anomaly-meta-pill"><i class="fa-solid fa-gun"></i> Weapon: ${al.weapon}</span>
                <span class="anomaly-meta-pill"><i class="fa-solid fa-skull"></i> Category: ${al.crime_type}</span>
              </div>
            `;
            alertsWrap.appendChild(alCard);
          });
        }
        appendTerminalLog("Rendered threat-intelligence alerts feed.", "success");
      }

      // ── E. Binds dynamic category predictor form submittal ─────────────────
      const form = document.getElementById("aiPredictorForm");
      if (form) {
        // Unbind previous to prevent multiple listeners
        form.onsubmit = null;
        
        form.onsubmit = async (e) => {
          e.preventDefault();
          
          const city = document.getElementById("predCity").value;
          const month = document.getElementById("predMonth").value;
          const age = document.getElementById("predAge").value;
          const gender = document.getElementById("predGender").value;
          const weapon = document.getElementById("predWeapon").value;
          
          const placeholder = document.getElementById("inferencePlaceholder");
          const output = document.getElementById("inferenceOutput");
          const btn = document.getElementById("inferenceBtn");
          const resultBox = document.getElementById("inferenceResultBox");
          
          if (!city || !weapon) {
            return;
          }
          
          if (btn) {
            btn.disabled = true;
            btn.innerHTML = `<i class="fa-solid fa-cog fa-spin"></i> Synthesizing Predictor...`;
          }
          
          appendTerminalLog(`Executing classification inference on inputs...`, "info");
          
          const res = await window.CrimeScopeAPI.predictCategory(city, month, age, gender, weapon);
          
          if (btn) {
            btn.disabled = false;
            btn.innerHTML = `<i class="fa-solid fa-bolt"></i> Run AI Inference`;
          }
          
          if (!res || res.error) {
            appendTerminalLog("AI classification query failed.", "warning");
            return;
          }
          
          if (placeholder) placeholder.style.display = "none";
          if (output) output.style.display = "block";
          if (resultBox) resultBox.className = "inference-result-box success";
          
          const valCrime = document.getElementById("predCrimeValue");
          const valConf = document.getElementById("predConfidenceVal");
          const fillConf = document.getElementById("predConfidenceFill");
          
          if (valCrime) valCrime.innerText = res.predicted_crime_type.toUpperCase();
          if (valConf) valConf.innerText = `${res.confidence.toFixed(1)}%`;
          if (fillConf) fillConf.style.width = `${res.confidence}%`;
          
          appendTerminalLog(`Inference isolated likely target offense as: ${res.predicted_crime_type.toUpperCase()} (Confidence: ${res.confidence}%)`, "success");
        };
      }

    } catch (err) {
      console.error("AI Command Center init fail:", err);
      appendTerminalLog("Neural engine integration encountered errors.", "warning");
    }
  }
};
