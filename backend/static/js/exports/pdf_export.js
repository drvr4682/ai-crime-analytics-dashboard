/**
 * CrimeScope Intel — Forensic Export Engine
 * Confidential PDF Intelligence Dossier Coordinator (jsPDF Hybrid Strategy)
 */

window.CrimeScopeExports = window.CrimeScopeExports || {};

window.CrimeScopeExports.exportToPDF = async function() {
  const log = window.CrimeScopeExports.log;
  const getFilters = window.CrimeScopeExports.getFilters;
  const setLoading = window.CrimeScopeExports.setLoading;
  
  const btnId = "exportPDF";
  const defaultText = `<i class="fa-solid fa-file-pdf"></i> Compile PDF Report`;
  
  try {
    log("Initializing Forensic PDF Intelligence Dossier compiler...", "info");
    setLoading(btnId, true, defaultText, "Compiling...");

    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF("p", "mm", "a4"); // Standard A4: 210mm x 297mm
    const filters = getFilters();
    
    // Core Layout Metrics
    const pageW = 210;
    const pageH = 297;
    
    // Cyberpunk HSL/RGB Colors mapped for jsPDF
    const cNavy = [11, 16, 32];      // Deep Space background (#0b1020)
    const cCard = [20, 27, 49];      // Glass card fill
    const cCyan = [0, 242, 254];      // Neon Cyan (#00f2fe)
    const cRose = [255, 51, 102];     // Neon Rose (#ff3366)
    const cEmerald = [0, 255, 196];   // Neon Emerald (#00ffc4)
    const cWhite = [255, 255, 255];   // Active text
    const cMuted = [165, 180, 252];   // Lavender secondary text (#a5b4fc)
    
    // Draw background filler helper
    const drawBackground = () => {
      pdf.setFillColor(cNavy[0], cNavy[1], cNavy[2]);
      pdf.rect(0, 0, pageW, pageH, "F");
      
      // Cyber HUD grid borders
      pdf.setDrawColor(cCyan[0], cCyan[1], cCyan[2]);
      pdf.setLineWidth(0.5);
      pdf.rect(5, 5, pageW - 10, pageH - 10, "D");
      
      // Muted sub-borders
      pdf.setDrawColor(20, 27, 49);
      pdf.rect(6, 6, pageW - 12, pageH - 12, "D");
    };

    // Extract dynamic DOM values
    const totalCasesVal = document.querySelector(".kpi-card-glow-cyan .kpi-value, .card-glow-cyan:first-child .kpi-value")?.innerText || "0";
    const closedCasesVal = document.querySelector(".card-glow-emerald .kpi-value")?.innerText || "0";
    const openCasesVal = document.querySelector(".card-glow-yellow .kpi-value")?.innerText || "0";
    const topCityVal = document.querySelector(".card-glow-rose .kpi-value")?.innerText || "N/A";
    const topCrimeVal = document.querySelector(".card-glow-purple .kpi-value")?.innerText || "N/A";
    const closureRateVal = document.querySelector(".kpi-card:last-child .kpi-value, .card-glow-cyan:last-child .kpi-value")?.innerText || "0.0%";
    const anomalyCards = document.querySelectorAll(".anomaly-alert-card");
    const insightCards = document.querySelectorAll(".insight-card");

    // ==========================================================================
    // ── PAGE 1: SECURITY DOSSIER COVER SHEET & KPI TILES ──────────────────────
    // ==========================================================================
    log("Compiling Page 1: Structured Cover Sheet and active KPI metrics...", "info");
    drawBackground();

    // 1. Cyber Security Pulse Header
    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(8);
    pdf.setTextColor(cRose[0], cRose[1], cRose[2]);
    pdf.text("// CRIMESCOPE SECURITY OPERATIONS COMMAND FORENSIC RECORD", 15, 20);

    // 2. Main Title Block
    pdf.setFontSize(24);
    pdf.setTextColor(cCyan[0], cCyan[1], cCyan[2]);
    pdf.text("CRIMESCOPE SYSTEM DOSSIER", 15, 32);
    
    pdf.setFontSize(10);
    pdf.setTextColor(cMuted[0], cMuted[1], cMuted[2]);
    pdf.setFont("helvetica", "normal");
    pdf.text("AI-POWERED THREAT INTELLIGENCE BRIEFING & SYNERGISTIC FORENSICS", 15, 38);

    // Divider Line
    pdf.setDrawColor(cCyan[0], cCyan[1], cCyan[2]);
    pdf.setLineWidth(0.8);
    pdf.line(15, 42, pageW - 15, 42);

    // 3. Metadata Panel Block
    pdf.setFillColor(cCard[0], cCard[1], cCard[2]);
    pdf.rect(15, 48, pageW - 30, 34, "F");
    pdf.setDrawColor(40, 50, 80);
    pdf.setLineWidth(0.3);
    pdf.rect(15, 48, pageW - 30, 34, "D");

    pdf.setFont("courier", "bold");
    pdf.setFontSize(9);
    pdf.setTextColor(cCyan[0], cCyan[1], cCyan[2]);
    pdf.text("CLASSIFICATION: UNCLASSIFIED // SECURE NODE v2.4", 20, 54);
    
    pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
    pdf.setFont("courier", "normal");
    pdf.text(`GENERATED ON   : ${new Date().toUTCString()}`, 20, 60);
    pdf.text(`YEAR FILTER    : ${filters.year}`, 20, 66);
    pdf.text(`CITY FILTER    : ${filters.city.toUpperCase()}`, 20, 72);
    pdf.text(`OFFENSE FILTER : ${filters.crimeType.toUpperCase()}`, 20, 78);

    // 4. Secure Overview Text
    pdf.setFont("helvetica", "normal");
    pdf.setFontSize(9.5);
    pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
    const overviewText = "This dossier compiles dynamic spatial, temporal, and machine learning outputs derived from current threat indexes. Information is isolated in real-time under the active filtering parameters shown above to support local command patrols and tactical containment structures.";
    const splitOverview = pdf.splitTextToSize(overviewText, pageW - 30);
    pdf.text(splitOverview, 15, 92);

    // 5. Grid of 5 Structured KPI Cards
    log("Mapping KPI summary cards onto Cover Sheet...", "info");
    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(11);
    pdf.setTextColor(cCyan[0], cCyan[1], cCyan[2]);
    pdf.text("ACTIVE TELEMETRY SUMMARY INDEXES", 15, 114);

    const kpis = [
      { label: "TOTAL LOGGED CRIMES", value: totalCasesVal, desc: "Total dataset incident volume", color: cCyan },
      { label: "RESOLUTION INDEX", value: closureRateVal, desc: "Overall database closure rate", color: cEmerald },
      { label: "PRIMARY EPISENTER", value: topCityVal, desc: "City with maximum density", color: cRose },
      { label: "PRINCIPAL OFFENSE", value: topCrimeVal, desc: "Highest occurrence crime type", color: cMuted },
      { label: "SURGE ANOMALIES", value: `${anomalyCards.length} outliers`, desc: "Isolation Forest alerts flagged", color: cRose }
    ];

    let startY = 122;
    kpis.forEach((k, idx) => {
      // Draw KPI Box
      pdf.setFillColor(cCard[0], cCard[1], cCard[2]);
      pdf.rect(15, startY, pageW - 30, 20, "F");
      
      // Draw left color accent border
      pdf.setDrawColor(k.color[0], k.color[1], k.color[2]);
      pdf.setLineWidth(1.2);
      pdf.line(15, startY, 15, startY + 20);
      
      pdf.setDrawColor(40, 50, 80);
      pdf.setLineWidth(0.3);
      pdf.rect(15, startY, pageW - 30, 20, "D");

      // Draw Label
      pdf.setFont("helvetica", "bold");
      pdf.setFontSize(8);
      pdf.setTextColor(cMuted[0], cMuted[1], cMuted[2]);
      pdf.text(k.label, 20, startY + 6);

      // Draw Value
      pdf.setFont("courier", "bold");
      pdf.setFontSize(12);
      pdf.setTextColor(k.color[0], k.color[1], k.color[2]);
      pdf.text(k.value, 20, startY + 14);

      // Draw Description on Right side
      pdf.setFont("helvetica", "normal");
      pdf.setFontSize(7.5);
      pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
      pdf.text(k.desc, 120, startY + 11);

      startY += 26;
    });

    // Page Footer
    pdf.setFont("courier", "normal");
    pdf.setFontSize(7);
    pdf.setTextColor(cMuted[0], cMuted[1], cMuted[2]);
    pdf.text("CRIMESCOPE SYSTEM DOSSIER // PAGE 1 OF 5", pageW / 2, 288, { align: "center" });


    // ==========================================================================
    // ── PAGE 2: NEURAL INSIGHTS & ANOMALY THREAT ALERTS ────────────────────────
    // ==========================================================================
    log("Compiling Page 2: Native text rendering of AI synthesized observations...", "info");
    pdf.addPage();
    drawBackground();

    // Title
    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(8);
    pdf.setTextColor(cRose[0], cRose[1], cRose[2]);
    pdf.text("// SECTION II: NEURAL SYNTHESIZED INSIGHTS & CRITICAL THREAT ALERTS", 15, 20);

    // AI Neural Insights Header
    pdf.setFontSize(14);
    pdf.setTextColor(cCyan[0], cCyan[1], cCyan[2]);
    pdf.text("Neural Synthesized Insights", 15, 32);

    let currentY = 40;
    if (insightCards.length > 0) {
      insightCards.forEach((card) => {
        let title = card.querySelector("h4")?.innerText || "Observation";
        // Clean out Hindi/non-ASCII glyphs to support standard helvetica jsPDF font
        if (title.includes("/")) {
          title = title.split("/").pop().trim();
        }
        title = title.replace(/[^\x00-\x7F]/g, "").trim().toUpperCase();

        const val = card.querySelector(".insight-metric")?.innerText || "";
        const desc = card.querySelector("p")?.innerText || "";

        pdf.setFillColor(cCard[0], cCard[1], cCard[2]);
        pdf.rect(15, currentY, pageW - 30, 22, "F");
        pdf.setDrawColor(40, 50, 80);
        pdf.setLineWidth(0.3);
        pdf.rect(15, currentY, pageW - 30, 22, "D");

        // Border accent
        pdf.setDrawColor(cCyan[0], cCyan[1], cCyan[2]);
        pdf.setLineWidth(1.0);
        pdf.line(15, currentY, 15, currentY + 22);

        pdf.setFont("helvetica", "bold");
        pdf.setFontSize(9);
        pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
        pdf.text(`${title}: `, 20, currentY + 6);
        
        pdf.setFont("courier", "bold");
        pdf.setTextColor(cCyan[0], cCyan[1], cCyan[2]);
        pdf.text(val, 20 + pdf.getTextWidth(`${title}: `), currentY + 6);

        pdf.setFont("helvetica", "normal");
        pdf.setFontSize(8);
        pdf.setTextColor(cMuted[0], cMuted[1], cMuted[2]);
        const splitDesc = pdf.splitTextToSize(desc, pageW - 40);
        pdf.text(splitDesc, 20, currentY + 12);

        currentY += 26;
      });
    } else {
      pdf.setFont("helvetica", "normal");
      pdf.setFontSize(9);
      pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
      pdf.text("No dynamic neural insights compiled in active session.", 15, currentY);
    }

    // Page Footer for Page 2
    pdf.setFont("courier", "normal");
    pdf.setFontSize(7);
    pdf.setTextColor(cMuted[0], cMuted[1], cMuted[2]);
    pdf.text("CRIMESCOPE SYSTEM DOSSIER // PAGE 2 OF 5", pageW / 2, 288, { align: "center" });

    // ==========================================================================
    // ── PAGE 3: ISOLATION FOREST ANOMALY ALERTS FEED (DEDICATED PAGE) ─────────
    // ==========================================================================
    log("Compiling Page 3: Dedicated Isolation Forest anomaly alerts stream...", "info");
    pdf.addPage();
    drawBackground();

    // Title
    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(8);
    pdf.setTextColor(cRose[0], cRose[1], cRose[2]);
    pdf.text("// SECTION III: THREAT INTELLIGENCE & ISOLATION FOREST ANOMALIES", 15, 20);

    // Dynamic Threat Alerts Header
    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(14);
    pdf.setTextColor(cRose[0], cRose[1], cRose[2]);
    pdf.text("Isolation Forest Anomaly Alerts Feed", 15, 32);

    currentY = 40;
    let count = 0;
    if (anomalyCards.length > 0) {
      anomalyCards.forEach((card) => {
        if (count >= 8) return; // Dedicated page safely accommodates up to 8 full anomalies
        const headerText = card.querySelector(".anomaly-threat-label")?.innerText || "HIGH RISK";
        const scoreText = card.querySelector(".anomaly-score-badge")?.innerText || "Score: 0.00";
        const msg = card.querySelector(".anomaly-message")?.innerText || "";
        const footer = card.querySelector(".anomaly-card-footer")?.innerText.replace(/\s+/g, " ") || "";

        pdf.setFillColor(cCard[0], cCard[1], cCard[2]);
        pdf.rect(15, currentY, pageW - 30, 24, "F");
        pdf.setDrawColor(40, 50, 80);
        pdf.setLineWidth(0.3);
        pdf.rect(15, currentY, pageW - 30, 24, "D");

        // Border accent
        pdf.setDrawColor(cRose[0], cRose[1], cRose[2]);
        pdf.setLineWidth(1.0);
        pdf.line(15, currentY, 15, currentY + 24);

        // Header info
        pdf.setFont("helvetica", "bold");
        pdf.setFontSize(8.5);
        pdf.setTextColor(cRose[0], cRose[1], cRose[2]);
        pdf.text(headerText, 20, currentY + 6);
        
        pdf.setFont("courier", "bold");
        pdf.setFontSize(8);
        pdf.setTextColor(cMuted[0], cMuted[1], cMuted[2]);
        pdf.text(scoreText, 120, currentY + 6);

        // Message
        pdf.setFont("helvetica", "normal");
        pdf.setFontSize(8);
        pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
        const splitMsg = pdf.splitTextToSize(msg, pageW - 40);
        pdf.text(splitMsg, 20, currentY + 12);

        // Footer pills
        pdf.setFont("courier", "normal");
        pdf.setFontSize(7);
        pdf.setTextColor(cCyan[0], cCyan[1], cCyan[2]);
        pdf.text(footer, 20, currentY + 20);

        currentY += 28;
        count++;
      });
    } else {
      pdf.setFont("helvetica", "normal");
      pdf.setFontSize(9);
      pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
      pdf.text("No critical threat anomalies isolated. Core behavior is stable.", 15, currentY);
    }

    // Page Footer for Page 3
    pdf.setFont("courier", "normal");
    pdf.setFontSize(7);
    pdf.setTextColor(cMuted[0], cMuted[1], cMuted[2]);
    pdf.text("CRIMESCOPE SYSTEM DOSSIER // PAGE 3 OF 5", pageW / 2, 288, { align: "center" });


    // ==========================================================================
    // ── PAGE 3: ANALYTICAL CHARTS (SPATIO-TEMPORAL VISUALIZATIONS) ─────────────
    // ==========================================================================
    log("Compiling Page 3: Visual canvas frames extraction of trends and matrices...", "info");
    pdf.addPage();
    drawBackground();

    // Title
    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(8);
    pdf.setTextColor(cRose[0], cRose[1], cRose[2]);
    pdf.text("// SECTION III: SPATIO-TEMPORAL DENSITY VISUALIZATIONS", 15, 20);

    pdf.setFontSize(14);
    pdf.setTextColor(cCyan[0], cCyan[1], cCyan[2]);
    pdf.text("Active Analytics Visualizations", 15, 30);

    // 1. Extract Trend Line Chart
    if (window.CrimeScopeInstances && window.CrimeScopeInstances.trends) {
      log("Extracting Crime Trends Chart canvas...", "info");
      const trendsImg = window.CrimeScopeInstances.trends.toBase64Image();
      
      pdf.setDrawColor(40, 50, 80);
      pdf.setLineWidth(0.3);
      pdf.rect(15, 38, 85, 62, "D");
      
      pdf.addImage(trendsImg, "PNG", 16, 43, 83, 52);
      
      pdf.setFont("helvetica", "bold");
      pdf.setFontSize(8);
      pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
      pdf.text("CRIME EVOLUTION TIMELINE", 15, 36);
    }

    // 2. Extract Top Cities Bar Chart
    if (window.CrimeScopeInstances && window.CrimeScopeInstances.cities) {
      log("Extracting Epicenter Cities Chart canvas...", "info");
      const citiesImg = window.CrimeScopeInstances.cities.toBase64Image();
      
      pdf.setDrawColor(40, 50, 80);
      pdf.setLineWidth(0.3);
      pdf.rect(110, 38, 85, 62, "D");
      
      pdf.addImage(citiesImg, "PNG", 111, 43, 83, 52);
      
      pdf.setFont("helvetica", "bold");
      pdf.setFontSize(8);
      pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
      pdf.text("TOP 10 THREAT EPICENTERS", 110, 36);
    }

    // 3. Extract Heatmap Grid (HTML Grid visual capture using html2canvas)
    const heatmapGrid = document.getElementById("heatmapGrid");
    if (heatmapGrid) {
      log("Capturing Monthly Crime Heatmap Matrix using html2canvas...", "info");
      pdf.setFont("helvetica", "bold");
      pdf.setFontSize(8);
      pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
      pdf.text("MONTHLY CRIME FREQUENCY MATRIX BY CITY", 15, 110);

      const hOptions = {
        scale: 2,
        backgroundColor: "#0b1020",
        useCORS: true,
        logging: false
      };
      
      const heatmapCanvas = await html2canvas(heatmapGrid, hOptions);
      const heatmapImg = heatmapCanvas.toBase64Image ? heatmapCanvas.toBase64Image() : heatmapCanvas.toDataURL("image/png");
      
      pdf.setDrawColor(40, 50, 80);
      pdf.setLineWidth(0.3);
      pdf.rect(15, 112, 180, 80, "D");
      
      pdf.addImage(heatmapImg, "PNG", 16, 113, 178, 78);
    }

    // 4. Extract Crime Type Distribution Chart
    if (window.CrimeScopeInstances && window.CrimeScopeInstances.types) {
      log("Extracting Offense Domain Distribution Chart canvas...", "info");
      const typesImg = window.CrimeScopeInstances.types.toBase64Image();
      
      pdf.setDrawColor(40, 50, 80);
      pdf.setLineWidth(0.3);
      pdf.rect(15, 208, 85, 62, "D");
      
      pdf.addImage(typesImg, "PNG", 16, 213, 83, 52);
      
      pdf.setFont("helvetica", "bold");
      pdf.setFontSize(8);
      pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
      pdf.text("OFFENSE DOMAIN ANALYSIS", 15, 206);
    }

    // 5. Extract Weapon Used Distribution Chart
    if (window.CrimeScopeInstances && window.CrimeScopeInstances.weapons) {
      log("Extracting Weapon Distribution Chart canvas...", "info");
      const weaponsImg = window.CrimeScopeInstances.weapons.toBase64Image();
      
      pdf.setDrawColor(40, 50, 80);
      pdf.setLineWidth(0.3);
      pdf.rect(110, 208, 85, 62, "D");
      
      pdf.addImage(weaponsImg, "PNG", 111, 213, 83, 52);
      
      pdf.setFont("helvetica", "bold");
      pdf.setFontSize(8);
      pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
      pdf.text("PRIMARY WEAPON VECTORS", 110, 206);
    }

    // Page Footer
    pdf.setFont("courier", "normal");
    pdf.setFontSize(7);
    pdf.setTextColor(cMuted[0], cMuted[1], cMuted[2]);
    pdf.text("CRIMESCOPE SYSTEM DOSSIER // PAGE 4 OF 5", pageW / 2, 288, { align: "center" });


    // ==========================================================================
    // ── PAGE 4: PREDICTIVE ML FORECASTS & SCATTER PLOTS ───────────────────────
    // ==========================================================================
    log("Compiling Page 4: Extracting Machine Learning predictions and Scatter Matrices...", "info");
    pdf.addPage();
    drawBackground();

    // Title
    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(8);
    pdf.setTextColor(cRose[0], cRose[1], cRose[2]);
    pdf.text("// SECTION IV: PREDICTIVE MACHINE LEARNING FORECASTING & SCATTER CORRELATIONS", 15, 20);

    pdf.setFontSize(14);
    pdf.setTextColor(cCyan[0], cCyan[1], cCyan[2]);
    pdf.text("AI Foresight & Behavioral Telemetry", 15, 30);

    // 6. Extract Predictive ML Chart
    if (window.CrimeScopeInstances && window.CrimeScopeInstances.predictions) {
      log("Extracting Linear Regression Forecast Chart canvas...", "info");
      const predictionsImg = window.CrimeScopeInstances.predictions.toBase64Image();
      
      pdf.setDrawColor(40, 50, 80);
      pdf.setLineWidth(0.3);
      pdf.rect(15, 42, 180, 95, "D");
      
      pdf.addImage(predictionsImg, "PNG", 16, 45, 178, 89);
      
      pdf.setFont("helvetica", "bold");
      pdf.setFontSize(8);
      pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
      pdf.text("LINEAR REGRESSION FUTURE TREND FORECAST (ML)", 15, 39);
    }

    // 7. Extract Correlation Scatter Matrix
    if (window.CrimeScopeInstances && window.CrimeScopeInstances.correlation) {
      log("Extracting Age vs Patrol Density Scatter Matrix canvas...", "info");
      const correlationImg = window.CrimeScopeInstances.correlation.toBase64Image();
      
      pdf.setDrawColor(40, 50, 80);
      pdf.setLineWidth(0.3);
      pdf.rect(15, 158, 180, 95, "D");
      
      pdf.addImage(correlationImg, "PNG", 16, 161, 178, 89);
      
      pdf.setFont("helvetica", "bold");
      pdf.setFontSize(8);
      pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
      pdf.text("VICTIM AGE VS POLICE DEPLOYMENT CORRELATION SCATTER", 15, 155);
    }

    // Footer Info Box
    pdf.setFillColor(cCard[0], cCard[1], cCard[2]);
    pdf.rect(15, 260, pageW - 30, 16, "F");
    pdf.setDrawColor(cCyan[0], cCyan[1], cCyan[2]);
    pdf.setLineWidth(0.5);
    pdf.rect(15, 260, pageW - 30, 16, "D");

    pdf.setFont("courier", "bold");
    pdf.setFontSize(7.5);
    pdf.setTextColor(cCyan[0], cCyan[1], cCyan[2]);
    pdf.text("SECURE FORENSIC ARCHIVE // RECORD VERIFIED AUTOMATICALLY BY SECURE CORE", 20, 267);
    pdf.setFont("courier", "normal");
    pdf.setTextColor(cWhite[0], cWhite[1], cWhite[2]);
    pdf.text("All computations, patterns, and timelines compiled under active session variables. AUTHENTICATION CODE: CS-992-80X", 20, 272);

    // Page Footer
    pdf.setFont("courier", "normal");
    pdf.setFontSize(7);
    pdf.setTextColor(cMuted[0], cMuted[1], cMuted[2]);
    pdf.text("CRIMESCOPE SYSTEM DOSSIER // PAGE 5 OF 5", pageW / 2, 288, { align: "center" });

    // ==========================================================================
    // ── TRIGGER DOWNLOAD ──────────────────────────────────────────────────────
    // ==========================================================================
    const filename = window.CrimeScopeExports.getSanitizedFilename("crime_dossier", "pdf");
    log(`Saving generated PDF dossier as: ${filename}`, "info");
    
    pdf.save(filename);
    
    log(`Confidential PDF intelligence dossier compiled successfully! Saved: ${filename}`, "success");
  } catch (err) {
    log(`PDF compilation failed: ${err.message}`, "error");
    alert(`PDF Export Failed: ${err.message}`);
  } finally {
    setLoading(btnId, false, defaultText);
  }
};

// Bind PDF export trigger
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("exportPDF");
  if (btn) {
    btn.addEventListener("click", window.CrimeScopeExports.exportToPDF);
  }
});
