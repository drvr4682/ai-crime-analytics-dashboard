/**
 * CrimeScope Intel — Forensic Export Engine
 * Plaintext Forensic Summary Dossier Coordinator
 */

window.CrimeScopeExports = window.CrimeScopeExports || {};

window.CrimeScopeExports.exportTextSummary = function() {
  const log = window.CrimeScopeExports.log;
  const getFilters = window.CrimeScopeExports.getFilters;
  const setLoading = window.CrimeScopeExports.setLoading;
  
  const btnId = "exportTXT";
  const defaultText = `<i class="fa-solid fa-download"></i> Download Text Intel`;
  
  try {
    log("Compiling plaintext forensic intelligence summary...", "info");
    setLoading(btnId, true, defaultText, "Compiling...");

    const filters = getFilters();
    
    // 1. Extract values from DOM KPI cards
    const totalCasesVal = document.querySelector(".kpi-card-glow-cyan .kpi-value, .card-glow-cyan:first-child .kpi-value")?.innerText || "0";
    const closedCasesVal = document.querySelector(".card-glow-emerald .kpi-value")?.innerText || "0";
    const openCasesVal = document.querySelector(".card-glow-yellow .kpi-value")?.innerText || "0";
    const topCityVal = document.querySelector(".card-glow-rose .kpi-value")?.innerText || "N/A";
    const topCrimeVal = document.querySelector(".card-glow-purple .kpi-value")?.innerText || "N/A";
    const closureRateVal = document.querySelector(".kpi-card:last-child .kpi-value, .card-glow-cyan:last-child .kpi-value")?.innerText || "0.0%";

    // 2. Extract AI Neural Insights
    const insightCards = document.querySelectorAll(".insight-card");
    let insightsTxt = "";
    if (insightCards.length > 0) {
      insightCards.forEach((card, idx) => {
        let title = card.querySelector("h4")?.innerText || "Observation";
        // Clean out Hindi/non-ASCII glyphs to guarantee clean plain text
        if (title.includes("/")) {
          title = title.split("/").pop().trim();
        }
        title = title.replace(/[^\x00-\x7F]/g, "").trim().toUpperCase();

        const val = card.querySelector(".insight-metric")?.innerText || "";
        const desc = card.querySelector("p")?.innerText || "";
        insightsTxt += `\n[INSIGHT #${idx + 1}] ${title}: ${val}\n  --> ${desc}\n`;
      });
    } else {
      insightsTxt = "\nNo neural insights loaded in current session.\n";
    }

    // 3. Extract Isolation Forest Anomalies
    const anomalyCards = document.querySelectorAll(".anomaly-alert-card");
    let anomaliesTxt = "";
    if (anomalyCards.length > 0) {
      anomalyCards.forEach((card, idx) => {
        const header = card.querySelector(".anomaly-card-header")?.innerText.replace(/\s+/g, " ") || "";
        const msg = card.querySelector(".anomaly-message")?.innerText || "";
        const footer = card.querySelector(".anomaly-card-footer")?.innerText.replace(/\s+/g, " ") || "";
        anomaliesTxt += `\n[ANOMALY #${idx + 1}] ${header}\n  Message: ${msg}\n  Metadata: ${footer}\n`;
      });
    } else {
      anomaliesTxt = "\nNo critical threat anomalies isolated.\n";
    }

    // 4. Construct Plaintext report
    const timestamp = new Date().toUTCString();
    const reportText = `
======================================================================
                   CRIMESCOPE SYSTEM FORENSIC BRIEFING
======================================================================
Generated: ${timestamp}
Node Status: SECURE REMOTE ACCESS (OK)
Active Year Constraint : ${filters.year}
Active City Constraint : ${filters.city.toUpperCase()}
Active Offense Constraint: ${filters.crimeType.toUpperCase()}

----------------------------------------------------------------------
1. METRIC QUANTIFICATION SUMMARIES (DASHBOARD KPIs)
----------------------------------------------------------------------
Total Cases Cataloged : ${totalCasesVal}
Closed Resolutions    : ${closedCasesVal}
Open Infractions      : ${openCasesVal}
Case Resolution Index : ${closureRateVal}
Primary Threat City   : ${topCityVal}
Primary Threat Vector : ${topCrimeVal}

----------------------------------------------------------------------
2. NEURAL SYNTHESIZED INTEL (AI INSIGHTS ENGINE)
----------------------------------------------------------------------${insightsTxt}
----------------------------------------------------------------------
3. THREAT INTELLIGENCE FEED (ISOLATION FOREST ANOMALIES)
----------------------------------------------------------------------${anomaliesTxt}
======================================================================
                          END OF DOSSIER
======================================================================
`.trim();

    // 5. Trigger download
    const filename = window.CrimeScopeExports.getSanitizedFilename("crime_briefing", "txt");
    const blob = new Blob([reportText], { type: "text/plain;charset=utf-8" });
    const blobUrl = window.URL.createObjectURL(blob);
    
    const downloadLink = document.createElement("a");
    downloadLink.href = blobUrl;
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    window.URL.revokeObjectURL(blobUrl);
    
    log(`Plaintext forensic summary downloaded successfully: ${filename}`, "success");
  } catch (err) {
    log(`TXT export failed: ${err.message}`, "error");
    alert(`TXT Export Failed: ${err.message}`);
  } finally {
    setLoading(btnId, false, defaultText);
  }
};

// Bind TXT export trigger
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("exportTXT");
  if (btn) {
    btn.addEventListener("click", window.CrimeScopeExports.exportTextSummary);
  }
});
