/**
 * CrimeScope Intel — Cybercrime Intelligence Dashboard
 * Dynamic API Fetch Module
 */

window.CrimeScopeAPI = {
  async fetchSummary() {
    try {
      const response = await fetch("/api/dashboard-summary");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching summary KPIs:", err);
      return null;
    }
  },

  async fetchCrimeTrends() {
    try {
      const response = await fetch("/api/crime-trends");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching crime trends:", err);
      return null;
    }
  },

  async fetchCrimeTypes() {
    try {
      const response = await fetch("/api/crime-types");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching crime types:", err);
      return null;
    }
  },

  async fetchTopCities() {
    try {
      const response = await fetch("/api/top-cities");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching top cities:", err);
      return null;
    }
  },

  async fetchWeapons() {
    try {
      const response = await fetch("/api/weapons");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching weaponry data:", err);
      return null;
    }
  },

  async fetchHeatmap() {
    try {
      const response = await fetch("/api/heatmap");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching heatmap matrix:", err);
      return null;
    }
  },

  async fetchPredictions() {
    try {
      const response = await fetch("/api/predictions");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching predictions data:", err);
      return null;
    }
  },

  async fetchCorrelation() {
    try {
      const response = await fetch("/api/correlation");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching correlation data:", err);
      return null;
    }
  }
};
