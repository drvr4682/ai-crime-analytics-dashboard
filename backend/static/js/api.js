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
  },

  async fetchFilterOptions() {
    try {
      const response = await fetch("/api/filter-options");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching filter options:", err);
      return null;
    }
  },

  async fetchFilteredData(year, city, crimeType) {
    try {
      const url = `/filter-data?year=${encodeURIComponent(year)}&city=${encodeURIComponent(city)}&crime_type=${encodeURIComponent(crimeType)}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching filtered data:", err);
      return null;
    }
  },

  // ── Phase 4 Upgrades: AI Command Center REST APIs ──────────────────────────
  async fetchMLPredictions() {
    try {
      const response = await fetch("/api/ml/predictions");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching ML predictions:", err);
      return null;
    }
  },

  async fetchMLAccuracy() {
    try {
      const response = await fetch("/api/ml/accuracy");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching ML accuracy scores:", err);
      return null;
    }
  },

  async fetchMLHotspots() {
    try {
      const response = await fetch("/api/ml/hotspots");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching KMeans hotspots:", err);
      return null;
    }
  },

  async fetchMLAnomalies() {
    try {
      const response = await fetch("/api/ml/anomalies");
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error fetching IsolationForest anomalies:", err);
      return null;
    }
  },

  async predictCategory(city, month, victimAge, victimGender, weaponUsed) {
    try {
      const url = `/api/ml/predict-category?city=${encodeURIComponent(city)}&month=${encodeURIComponent(month)}&victim_age=${encodeURIComponent(victimAge)}&victim_gender=${encodeURIComponent(victimGender)}&weapon_used=${encodeURIComponent(weaponUsed)}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error("API call failed");
      return await response.json();
    } catch (err) {
      console.error("Error predicting category profile:", err);
      return null;
    }
  }
};
