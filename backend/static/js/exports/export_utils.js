/**
 * CrimeScope Intel — Forensic Export Engine
 * Central Shared Export Utilities & HUD Diagnostics Logger
 */

window.CrimeScopeExports = window.CrimeScopeExports || {};

// 1. Central HUD Diagnostics Terminal Logger
window.CrimeScopeExports.log = function(message, type = "info") {
  const terminalBody = document.querySelector(".terminal-body");
  if (!terminalBody) {
    console.log(`[Exports LOG] ${type.toUpperCase()}: ${message}`);
    return;
  }

  const now = new Date();
  const timeStr = now.toTimeString().split(" ")[0];
  let typeSpan = `<span class="t-info">[INFO]</span>`;

  if (type === "success") typeSpan = `<span class="t-success" style="color: var(--accent-emerald); font-weight: bold;">[SUCCESS]</span>`;
  if (type === "warning") typeSpan = `<span class="t-warning" style="color: var(--accent-yellow); font-weight: bold;">[WARN]</span>`;
  if (type === "error") typeSpan = `<span class="t-error" style="color: var(--accent-rose); font-weight: bold;">[ERROR]</span>`;

  const logLine = document.createElement("p");
  logLine.className = "t-line";
  logLine.style.margin = "0";
  logLine.innerHTML = `<span class="t-time" style="color: #4f46e5;">[${timeStr}]</span> ${typeSpan} ${message}`;
  
  const blinkLine = terminalBody.querySelector(".blink-line");
  if (blinkLine) {
    terminalBody.insertBefore(logLine, blinkLine);
  } else {
    terminalBody.appendChild(logLine);
  }
  
  // Auto-scroll to keep recent logs visible
  terminalBody.scrollTop = terminalBody.scrollHeight;
};

// 2. Active DOM Dropdown Filters Reader
window.CrimeScopeExports.getFilters = function() {
  const yearEl = document.getElementById("yearFilter");
  const cityEl = document.getElementById("cityFilter");
  const typeEl = document.getElementById("crimeTypeFilter");

  return {
    year: yearEl ? yearEl.value : "All",
    city: cityEl ? cityEl.value : "All",
    crimeType: typeEl ? typeEl.value : "All"
  };
};

// 3. Dynamic Sanitized Filename Generator
window.CrimeScopeExports.getSanitizedFilename = function(prefix, ext) {
  const filters = window.CrimeScopeExports.getFilters();
  const dateStr = new Date().toISOString().slice(0, 10);
  
  const cleanCity = filters.city.replace(/[^a-zA-Z0-9]/g, "") || "AllCities";
  const cleanYear = filters.year.toString();
  const cleanType = filters.crimeType.replace(/[^a-zA-Z0-9]/g, "").slice(0, 15) || "AllOffenses";
  
  return `${prefix}_${cleanYear}_${cleanCity}_${cleanType}_${dateStr}.${ext}`;
};

// 4. Visual Loading State & Button Toggler
window.CrimeScopeExports.setLoading = function(btnId, isLoading, defaultText, loadingText) {
  const btn = document.getElementById(btnId);
  if (!btn) return;

  btn.disabled = isLoading;
  if (isLoading) {
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> ${loadingText}`;
    btn.style.opacity = "0.7";
    btn.style.cursor = "not-allowed";
  } else {
    btn.innerHTML = defaultText;
    btn.style.opacity = "1";
    btn.style.cursor = "pointer";
  }
};
