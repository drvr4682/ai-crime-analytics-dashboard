/**
 * CrimeScope Intel — Cybercrime Intelligence Dashboard
 * JavaScript UI Interactions (Vanilla JS, No jQuery)
 */

document.addEventListener("DOMContentLoaded", () => {
  console.log("CrimeScope Intel System Initialized...");

  // ═══════════════════ MOBILE SIDEBAR INTERACTION ═══════════════════
  const sidebar = document.getElementById("sidebar");
  const mobileToggle = document.getElementById("mobileToggle");
  const sidebarOverlay = document.getElementById("sidebar-overlay");

  if (mobileToggle && sidebar && sidebarOverlay) {
    // Open Sidebar
    mobileToggle.addEventListener("click", () => {
      sidebar.classList.add("open");
      sidebarOverlay.classList.add("open");
    });

    // Close Sidebar on Overlay Click
    sidebarOverlay.addEventListener("click", () => {
      sidebar.classList.remove("open");
      sidebarOverlay.classList.remove("open");
    });

    // Close Sidebar when nav items are clicked (on mobile)
    const sidebarLinks = sidebar.querySelectorAll(".nav-link");
    sidebarLinks.forEach(link => {
      link.addEventListener("click", () => {
        if (window.innerWidth <= 992) {
          sidebar.classList.remove("open");
          sidebarOverlay.classList.remove("open");
        }
      });
    });
  }

  // ═══════════════════ SMART SMOOTH SCROLLING & SCROLL SPY ═══════════════════
  const sections = document.querySelectorAll("#dashboard, #trends, #types, #heatmap, #weapon, #predictions, #reports, #alerts");
  const navLinks = document.querySelectorAll(".sidebar .nav-link");
  const headerOffset = 90; // Topbar height + padding spacing

  // Smooth Scroll Trigger
  navLinks.forEach(link => {
    link.addEventListener("click", (e) => {
      const targetId = link.getAttribute("href");
      if (targetId && targetId.startsWith("#")) {
        e.preventDefault();
        const targetSection = document.querySelector(targetId);
        
        if (targetSection) {
          const elementPosition = targetSection.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

          window.scrollTo({
            top: offsetPosition,
            behavior: "smooth"
          });

          // Fallback active state highlighting
          navLinks.forEach(n => n.classList.remove("active"));
          link.classList.add("active");
        }
      }
    });
  });

  // Scroll Spy Active Link Highlighting
  window.addEventListener("scroll", () => {
    let currentActiveId = "";
    const scrollPos = window.scrollY + headerOffset + 40;

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;

      if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
        currentActiveId = section.getAttribute("id");
      }
    });

    if (currentActiveId) {
      navLinks.forEach(link => {
        link.classList.remove("active");
        if (link.getAttribute("href") === `#${currentActiveId}`) {
          link.classList.add("active");
        }
      });
    }
  });

  // ═══════════════════ DYNAMIC UPLOAD FORM PROGRESS ═══════════════════
  const uploadForm = document.getElementById("uploadForm");
  const progressWrap = document.getElementById("progressWrap");
  const progressFill = document.getElementById("progressFill");
  const progressLabel = document.getElementById("progressLabel");
  const uploadActions = document.querySelector(".upload-actions");

  if (uploadForm && progressWrap && progressFill && progressLabel) {
    const hackerSteps = [
      "Securing analytical node tunnel...",
      "Parsing CSV file headers...",
      "Stripping leading/trailing spaces...",
      "Resolving date candidates...",
      "Auto-purging duplicate rows...",
      "Filling missing text entries with [Unknown]...",
      "Normalizing categorical columns to title case...",
      "Running Linear Regression models on Scikit-Learn...",
      "Synthesizing forensic charts & correlation metrics...",
      "Compiling intelligence dashboard output..."
    ];

    uploadForm.addEventListener("submit", (e) => {
      // Show loader
      progressWrap.style.display = "block";
      if (uploadActions) {
        uploadActions.style.display = "none";
      }

      let stepIdx = 0;
      progressFill.style.width = "0%";
      
      // Cycle through hacker steps to simulate computation
      const stepTimer = setInterval(() => {
        if (stepIdx < hackerSteps.length) {
          progressLabel.innerHTML = `<i class="fa-solid fa-cog fa-spin icon-accent-emerald"></i> ${hackerSteps[stepIdx]}`;
          // Increment mock bar fill
          const currentPct = Math.round(((stepIdx + 1) / hackerSteps.length) * 100);
          progressFill.style.width = `${currentPct}%`;
          stepIdx++;
        } else {
          clearInterval(stepTimer);
        }
      }, 750);
    });
  }

  // ═══════════════════ DYNAMIC METRIC COUNTER ANIMATIONS ═══════════════════
  const kpiValues = document.querySelectorAll(".kpi-value");

  const animateCounters = () => {
    kpiValues.forEach(kpi => {
      const rawText = kpi.innerText.trim();
      
      // Skip strings that do not contain numbers
      if (!/\d/.test(rawText)) return;

      // Extract number components
      const hasPercent = rawText.includes("%");
      const cleanNum = parseFloat(rawText.replace(/[^\d.]/g, ""));

      if (isNaN(cleanNum)) return;

      const duration = 1500; // Counter timing in milliseconds
      const frames = 60;
      const increment = cleanNum / frames;
      let currentVal = 0;
      let frame = 0;

      const timer = setInterval(() => {
        frame++;
        currentVal += increment;
        
        if (frame >= frames) {
          clearInterval(timer);
          kpi.innerText = rawText; // Set original nicely formatted text at the end
        } else {
          if (hasPercent) {
            kpi.innerText = `${currentVal.toFixed(1)}%`;
          } else {
            kpi.innerText = Math.floor(currentVal).toLocaleString();
          }
        }
      }, duration / frames);
    });
  };

  // Trigger KPI counters animation instantly
  animateCounters();

  // ═══════════════════ MOCK FILTER BEHAVIOR (ALERTS CONSOLE PRINTS) ═══════════════════
  const yearFilter = document.getElementById("yearFilter");
  const cityFilter = document.getElementById("cityFilter");
  const terminalBody = document.querySelector(".terminal-body");

  if ((yearFilter || cityFilter) && terminalBody) {
    const appendTerminalLog = (logText, type = "info") => {
      const now = new Date();
      const timeStr = now.toTimeString().split(" ")[0];
      let typeSpan = `<span class="t-info">[INFO]</span>`;

      if (type === "success") typeSpan = `<span class="t-success">[OK]</span>`;
      if (type === "warning") typeSpan = `<span class="t-warning">[WARN]</span>`;

      const logLine = document.createElement("p");
      logLine.className = "t-line";
      logLine.innerHTML = `<span class="t-time">[${timeStr}]</span> ${typeSpan} ${logText}`;
      
      // Insert right before the input waiting indicator
      const blinkLine = terminalBody.querySelector(".blink-line");
      if (blinkLine) {
        terminalBody.insertBefore(logLine, blinkLine);
      } else {
        terminalBody.appendChild(logLine);
      }

      // Scroll to bottom
      terminalBody.scrollTop = terminalBody.scrollHeight;
    };

    if (yearFilter) {
      yearFilter.addEventListener("change", (e) => {
        const selected = e.target.value;
        appendTerminalLog(`Recalibrating model filters for Year parameter: [${selected.toUpperCase()}].`, "warning");
        setTimeout(() => {
          appendTerminalLog(`Temporal indexes compiled successfully for [${selected.toUpperCase()}].`, "success");
        }, 800);
      });
    }

    if (cityFilter) {
      cityFilter.addEventListener("change", (e) => {
        const selected = e.target.value;
        appendTerminalLog(`Applying spatial filter constraint on City parameter: [${selected.toUpperCase()}].`, "warning");
        setTimeout(() => {
          appendTerminalLog(`Spatial boundaries recalculated. Epicenter mapped.`, "success");
        }, 800);
      });
    }
  }

  // ═══════════════════ GLASS CARDS REFLECTIVE RADIAL HIGHLIGHTS ═══════════════════
  const glassCards = document.querySelectorAll(".glass-panel");
  glassCards.forEach(card => {
    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left; // x position inside element
      const y = e.clientY - rect.top;  // y position inside element
      
      // Update background with active radial light spotlight highlight
      card.style.background = `radial-gradient(circle 120px at ${x}px ${y}px, rgba(255,255,255,0.06), var(--surface-glass))`;
    });

    card.addEventListener("mouseleave", () => {
      card.style.background = ""; // Reset inline style to allow CSS class definitions
    });
  });

});
