/**
 * CrimeScope Intel — Security Operations Command (SOC) Alerts Feed Module
 */

window.CrimeScopeAlerts = {
  async fetchAndRender(year = "All", city = "All", crimeType = "All") {
    const feed = document.getElementById("socAlertsFeed");
    if (!feed) return;

    // Show loading indicator
    feed.innerHTML = `
      <div style="text-align: center; padding: 30px; color: var(--accent-rose); font-family: 'Space Mono', monospace;">
        <i class="fa-solid fa-triangle-exclamation fa-beat"></i> DECRYPTING SECURE ALERTS FEED...
      </div>
    `;

    try {
      const url = `/api/alerts?year=${encodeURIComponent(year)}&city=${encodeURIComponent(city)}&crime_type=${encodeURIComponent(crimeType)}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error("Alerts retrieval failed");
      const data = await response.json();

      if (!data || !data.alerts || data.alerts.length === 0) {
        feed.innerHTML = `
          <div style="text-align: center; padding: 40px; color: var(--text-muted); font-family: 'Outfit', sans-serif;">
            <i class="fa-solid fa-circle-check text-glow-emerald" style="font-size: 1.8rem; margin-bottom: 8px;"></i>
            <p style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">No critical alerts detected in this sector.</p>
          </div>
        `;
        return;
      }

      feed.innerHTML = "";

      data.alerts.forEach((al, idx) => {
        const item = document.createElement("div");
        item.className = `soc-alert-item severity-${al.theme_class}`;
        
        // Staggered slide-in animations
        item.style.animation = `slide-in-alert 0.4s ease-out ${idx * 0.06}s both`;
        
        // Define dynamic category icon
        let catIcon = "fa-solid fa-circle-notch";
        if (al.category === "CRIME SPIKE") catIcon = "fa-solid fa-chart-line";
        if (al.category === "WEAPON ESCALATION") catIcon = "fa-solid fa-gun";
        if (al.category === "HOTSPOT ESCALATION") catIcon = "fa-solid fa-fire";
        if (al.category === "ANOMALY WARNING") catIcon = "fa-solid fa-circle-nodes";
        if (al.category === "PREDICTION WARNING") catIcon = "fa-solid fa-brain";

        item.innerHTML = `
          <span class="soc-alert-time"><i class="fa-regular fa-clock text-muted"></i> ${al.timestamp}</span>
          <span class="soc-alert-category"><i class="${catIcon}"></i> ${al.category}</span>
          <span class="soc-alert-text" title="${al.text}">${al.text}</span>
          <span class="soc-alert-severity">${al.severity}</span>
        `;
        feed.appendChild(item);
      });

    } catch (err) {
      console.error("Error updating SOC alerts feed:", err);
      feed.innerHTML = `
        <div style="text-align: center; padding: 30px; color: var(--accent-rose); font-family: 'Space Mono', monospace;">
          <i class="fa-solid fa-triangle-exclamation"></i> DECRYPTION ERROR: SECURE STREAM CORRUPTED
        </div>
      `;
    }
  }
};

// Auto-run on DOM load if we are on dashboard page
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("socAlertsFeed")) {
    window.CrimeScopeAlerts.fetchAndRender();
  }
});
