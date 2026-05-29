/**
 * CrimeScope Intel — Quick Insights Rendering Module
 */

window.CrimeScopeInsights = {
  async fetchAndRender(year = "All", city = "All", crimeType = "All") {
    const grid = document.getElementById("quickInsightsGrid");
    if (!grid) return;

    // Show high-tech loading state
    grid.innerHTML = `
      <div style="grid-column: span 5; text-align: center; padding: 40px; color: var(--accent-cyan); font-family: 'Space Mono', monospace;">
        <i class="fa-solid fa-spinner fa-spin"></i> SYNTHESIZING INTELLIGENCE FEED...
      </div>
    `;

    try {
      const url = `/api/insights?year=${encodeURIComponent(year)}&city=${encodeURIComponent(city)}&crime_type=${encodeURIComponent(crimeType)}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error("Insights retrieval failed");
      const data = await response.json();

      if (!data || !data.insights || data.insights.length === 0) {
        grid.innerHTML = `
          <div class="kpi-card glass-panel card-glow-yellow" style="grid-column: span 5; padding: 24px; text-align: center;">
            <i class="fa-solid fa-triangle-exclamation text-glow-yellow" style="font-size: 1.8rem; margin-bottom: 8px;"></i>
            <p style="font-size: 0.82rem; color: var(--text-muted);">No insights compiled for selected parameters.</p>
          </div>
        `;
        return;
      }

      grid.innerHTML = "";

      // Adapt column count dynamically based on the number of insights returned
      grid.className = `insights-grid five-cols`;

      data.insights.forEach((ins, idx) => {
        const card = document.createElement("div");
        card.className = `kpi-card glass-panel insight-card card-glow-${ins.badge}`;
        // Trigger a subtle staggered sliding fade-in animation
        card.style.animation = `slide-in-alert 0.4s ease-out ${idx * 0.08}s both`;
        
        card.innerHTML = `
          <div class="insight-icon">
            <i class="${ins.icon}"></i>
          </div>
          <div class="insight-content">
            <h4 class="text-glow-${ins.badge}">${ins.title}</h4>
            <p>${ins.text}</p>
          </div>
        `;
        grid.appendChild(card);
      });

    } catch (err) {
      console.error("Error updating quick insights panel:", err);
      grid.innerHTML = `
        <div class="kpi-card glass-panel card-glow-rose" style="grid-column: span 5; padding: 24px; text-align: center;">
          <i class="fa-solid fa-triangle-exclamation text-glow-rose" style="font-size: 1.8rem; margin-bottom: 8px;"></i>
          <p style="font-size: 0.82rem; color: var(--text-muted);">Failed to load active database insights feed.</p>
        </div>
      `;
    }
  }
};

// Auto-run on DOM load if we are on dashboard page
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("quickInsightsGrid")) {
    window.CrimeScopeInsights.fetchAndRender();
  }
});
