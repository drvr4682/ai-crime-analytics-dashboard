/**
 * CrimeScope Intel — Forensic Export Engine
 * High-Resolution Dashboard HUD Visual Snapshot Coordinator
 */

window.CrimeScopeExports = window.CrimeScopeExports || {};

window.CrimeScopeExports.captureHUDSnapshot = async function() {
  const log = window.CrimeScopeExports.log;
  const setLoading = window.CrimeScopeExports.setLoading;
  
  const btnId = "exportSnapshot";
  const defaultText = `<i class="fa-solid fa-camera"></i> Capture HUD View`;
  
  try {
    log("Initializing high-resolution dashboard HUD snapshot capture...", "info");
    setLoading(btnId, true, defaultText, "Capturing...");

    // 1. Locate ONLY the main-content container
    const mainContent = document.querySelector(".main-content");
    if (!mainContent) {
      throw new Error("Target main content view panel not found.");
    }
    
    log("Rendering visual canvas nodes at double resolution...", "info");
    
    // 2. Execute html2canvas capture with exact user-specified parameters
    const options = {
      scale: 2,                  // Double resolution for sharp vector scaling
      backgroundColor: "#0b1020", // Deep cyberpunk space background
      useCORS: true,             // Avoid cross-origin image blocks
      logging: false             // Suppress internal library logs
    };
    
    const canvas = await html2canvas(mainContent, options);
    
    log("Compressing raster image frames and preparing binary file...", "info");
    
    // 3. Compile dynamic filename
    const dateStr = new Date().toISOString().slice(0, 10);
    const filename = `dashboard_snapshot_${dateStr}.png`;
    
    // 4. Trigger local browser PNG download
    const imgData = canvas.toDataURL("image/png");
    const downloadLink = document.createElement("a");
    downloadLink.href = imgData;
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    
    log(`Captured visual HUD view successfully: ${filename}`, "success");
  } catch (err) {
    log(`HUD snapshot failed: ${err.message}`, "error");
    alert(`Snapshot Failed: ${err.message}`);
  } finally {
    setLoading(btnId, false, defaultText);
  }
};

// Bind Snapshot export trigger
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("exportSnapshot");
  if (btn) {
    btn.addEventListener("click", window.CrimeScopeExports.captureHUDSnapshot);
  }
});
