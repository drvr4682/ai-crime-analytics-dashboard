/**
 * CrimeScope Intel — Forensic Export Engine
 * Excel Worksheet Data Export Coordinator
 */

window.CrimeScopeExports = window.CrimeScopeExports || {};

window.CrimeScopeExports.exportToExcel = async function() {
  const log = window.CrimeScopeExports.log;
  const getFilters = window.CrimeScopeExports.getFilters;
  const setLoading = window.CrimeScopeExports.setLoading;
  
  const btnId = "exportExcel";
  const defaultText = `<i class="fa-solid fa-file-excel"></i> Stream Spreadsheet`;
  
  try {
    // 1. Initialize log sequence
    log("Initializing spreadsheet data extraction sequence...", "info");
    setLoading(btnId, true, defaultText, "Extracting...");

    // 2. Fetch live dropdown filters
    const filters = getFilters();
    log(`Formulating secure query for [Year: ${filters.year}, City: ${filters.city.toUpperCase()}, Type: ${filters.crimeType.toUpperCase()}]`, "info");
    
    // 3. Construct endpoint URL
    const url = `/api/export/excel?year=${encodeURIComponent(filters.year)}&city=${encodeURIComponent(filters.city)}&crime_type=${encodeURIComponent(filters.crimeType)}`;
    log("Requesting Excel-compatible CSV stream from secure backend...", "info");
    
    // 4. Perform fetch with blood blob download to capture API validation errors
    const response = await fetch(url);
    if (!response.ok) {
      const errorJson = await response.json().catch(() => ({}));
      const errorMsg = errorJson.error || "Internal Server Error during data compile.";
      throw new Error(errorMsg);
    }
    
    // 5. Read filename from content-disposition header if available, or generate dynamic
    const contentDisposition = response.headers.get("Content-Disposition");
    let filename = window.CrimeScopeExports.getSanitizedFilename("crime_report", "csv");
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1];
      }
    }
    
    // 6. Receive dynamic CSV blob and trigger browser download
    const blob = await response.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    const downloadLink = document.createElement("a");
    downloadLink.href = blobUrl;
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    window.URL.revokeObjectURL(blobUrl);
    
    log(`Excel dataset compilation complete. Extracted: ${filename}`, "success");
  } catch (err) {
    log(`Excel export failed: ${err.message}`, "error");
    alert(`Export Failed: ${err.message}`);
  } finally {
    setLoading(btnId, false, defaultText);
  }
};

// Bind Excel export trigger
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("exportExcel");
  if (btn) {
    btn.addEventListener("click", window.CrimeScopeExports.exportToExcel);
  }
});
