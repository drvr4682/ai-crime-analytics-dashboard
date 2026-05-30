# 🛡️ CrimeScope Intel — AI-Powered Cybercrime Command HUD & Forensic Analysis Suite

Welcome to **CrimeScope Intel**, a state-of-the-art, high-fidelity AI-powered forensics command dashboard. This platform transforms raw regional security logs and cyber incident files into actionable, real-time threat intelligence.

Equipped with a **multi-model Scikit-Learn machine learning suite** and a cybersecurity-style **Security Operations Center (SOC) live alert feed**, the system enables security specialists to perform dynamic spatio-temporal filtering, forecasting, anomaly isolation, and risk clustering inside a premium cyberpunk dark neon glassmorphic interface.

---

## 🚀 Key Features

* **🔮 Multi-Model AI Analytics & Predictors**:
  * **Time-Series Forecasting (Linear Regression)**: Predicts upcoming municipal incident indices based on multi-year statistical variables.
  * **Dynamic Category Classifier (Random Forest)**: Classifies and isolates target likely crime categories (Confidence %) based on age, gender, month, city, and weaponry.
  * **Unsupervised Risk Cluster (KMeans)**: Categorizes cities into Risk Danger Tiers (*Critical*, *Warning*, *Low Risk*) mapped against resolution statistics and police densities.
  * **Outlier Threat Isolation (Isolation Forest)**: Trains on multivariate features to isolate the top 2% highly anomalous security infractions and automatically yields risk-graded alert cards.
* **🛡️ Security Operations Center (SOC) Live Alerts Feed**: Graded threat logs (Low, Medium, High, Critical) complete with custom system timestamps and localized infraction summaries.
* **💡 AI-Generated Quick Insights Grid**: Dynamically generates 5 natural-language observations (Hotspot Epicenter, Primary Category, Seasonal Density, YoY Growing Threat, and Tactical Weapon Index).
* **📈 High-Fidelity Interactive Visualizations**: Features sleek, fully interactive Chart.js charts including Monthly Crime Evolution timelines, proportional doughnut maps, horizontal weaponry index metrics, and scatter plots.
* **📂 In-Memory Ingest Engine**: Automatically validates headers, purges duplicate records, standardizes case formats, and pre-warms Scikit-Learn models in-memory for sub-millisecond responses without database bottlenecks.

---

## 🏛️ MVC Architecture & Project Layout

The codebase has been refactored into a highly clean, scalable Model-View-Controller (MVC) organization with absolute separation of concerns:

```text
crime-data-analysis/
│
├── backend/
│   ├── app.py                      # Production-grade Minimal Bootstrap Loader
│   │
│   ├── routes/                     # Controller Blueprint Layer
│   │   ├── dashboard_routes.py     # Main templates rendering & upload logic
│   │   ├── api_routes.py           # Core visual telemetry REST endpoints
│   │   ├── ml_routes.py            # AI Suite metrics & classifier predictors
│   │   ├── alert_routes.py         # SOC thread intelligence feeds
│   │   └── filter_routes.py        # Spatio-temporal queries & natural language insights
│   │
│   ├── services/                   # Business Logic Services Layer
│   │   ├── dashboard_service.py    # Singleton Data Cache & Session Hydration coordinator
│   │   ├── filter_service.py       # Pandas query filtering & timeline aggregates
│   │   ├── chart_service.py        # Chart.js JSON payload formatting mapper
│   │   ├── ml_service.py           # Regression projections & RF classifier coordinate
│   │   └── analytics_service.py    # Core numerical KPI and timeline aggregators
│   │
│   ├── ml/                         # Machine Learning Domain Algorithms
│   │   ├── linear_regression_model.py
│   │   ├── random_forest_model.py
│   │   ├── kmeans_model.py
│   │   ├── isolation_forest_model.py
│   │   ├── preprocessing.py
│   │   └── evaluation.py
│   │
│   ├── analysis/                   # Analytics Summaries & Natural-Language Engines
│   │   ├── insights_engine.py      # AI Natural-language statement generator
│   │   ├── alert_engine.py         # Graded rules-based SOC alert generator
│   │   ├── trend_analysis.py       # YoY growth & seasonal peak calculations
│   │   ├── hotspot_analysis.py     # KMeans cluster translation & risk categorizer
│   │   └── anomaly_analysis.py     # Isolation Forest outlier threat describer
│   │
│   ├── utils/                      # Centralized Utility Helper functions
│   │   ├── config.py               # Settings manager (Uploads, Data, Graphs paths)
│   │   ├── data_loader.py          # CSV parser & structural cleaning pipeline
│   │   ├── file_handler.py         # Extension validation & safe disk storage
│   │   ├── logger.py               # Rotating rotating-file logging configurator
│   │   └── validators.py           # Ingestion CSV headers & parameter validation
│   │
│   ├── static/                     # Static Web Assets
│   │   ├── css/                    # Cyberpunk Dark Glassmorphic Stylesheets
│   │   │   ├── style.css           # Core premium HUD styles
│   │   │   ├── dashboard.css       # Layout overrides
│   │   │   └── animations.css      # Custom keyframes
│   │   ├── js/                     # AJAX Fetching Modules & Controllers
│   │   │   ├── api.js              # Central AJAX HTTP clients
│   │   │   ├── charts.js           # Dynamic Chart.js canvas drawers
│   │   │   ├── dashboard.js        # DOM page controller & UI shell bindings
│   │   │   ├── filters.js          # Spatio-temporal reactive hooks
│   │   │   ├── insights.js         # Dynamic AI insights renderer
│   │   │   └── alerts.js           # Smart SOC alerts stream injector
│   │   └── graphs/                 # Temporary compiled summaries
│   │
│   └── templates/                  # Modular Presentation Templates
│       ├── index.html              # Clean Dataset Ingestion Gateway
│       ├── dashboard.html          # Dynamic Command HUD metrics command panel
│       └── components/             # Reusable modular Jinja template includes
│           ├── sidebar.html        # Fixed sidebar navigator
│           ├── navbar.html         # Dynamic query top navigation bar
│           ├── charts.html         # Charts grid canvas wrappers
│           ├── alerts.html         # Cybersecurity SOC alerts stream wrap
│           └── insights.html       # AI Quick Insights grids container
│
├── data/                           # Local sample datasets
├── uploads/                        # User-uploaded incident CSV files
├── reports/                        # Persistent analytical log report downloads
├── requirements.txt                # Unified dependency configurations
└── README.md                       # Product documentation
```

---

## 🛠️ Technology Stack

* **Backend Engine**: Python, Flask, Jinja2 Template Engine
* **Numerical & Data Processing**: Pandas, NumPy
* **Artificial Intelligence Core**: Scikit-Learn
* **Presentation UI (Vanilla JS)**: Chart.js, HTML5, HSL Hues, Hign-fidelity Vanilla CSS3
* **Iconography & Typography**: FontAwesome, Google Fonts (Outfit, Space Mono)

---

## ⚙️ REST API Endpoints Guide

The system exposes structured, highly responsive JSON REST endpoints:

### Primary Telemetry APIs
* `GET /api/dashboard-summary` — Serves high-level KPI card metrics.
* `GET /api/crime-trends` — Serves monthly crime timelines.
* `GET /api/crime-types` — Serves dominant category classifications.
* `GET /api/weapons` — Mapped weaponry distribution index.
* `GET /api/top-cities` — Top ten high-density municipal epicenters.
* `GET /api/heatmap` — Two-dimensional frequency matrix for seasonal analysis.
* `GET /api/predictions` — Future projected timelines formatted for Chart.js.
* `GET /api/correlation` — Demographic scatter points.
* `GET /api/filter-options` — Populates dropdown filters dynamically based on dataset features.

### Machine Learning & Intelligence APIs
* `GET /api/ml/predictions` — Scikit-Learn Linear Regression forecasted values and metrics.
* `GET /api/ml/accuracy` — Consolidated evaluation metrics (R², F1-Score, Silhouette Coeff).
* `GET /api/ml/hotspots` — KMeans clustered cities with assigned risk tiers.
* `GET /api/ml/anomalies` — Isolation Forest outliers and decision scores.
* `POST /api/ml/predict-category` — Dynamic Random Forest crime category classifier (takes JSON inputs).
* `GET /api/insights` — Dynamic natural-language insights based on active filters.
* `GET /api/alerts` — Real-time cybersecurity SOC threats stream based on active filters.

---

## 🚀 Quick Start & Installation

### 1. Pre-requisites
Ensure you have **Python 3.10+** installed on your workstation.

### 2. Sandbox Setup
Clone or map the project directory to your workspace, navigate to the folder, and configure a virtual environment:
```bash
# Set up sandbox virtual environment
python -m venv myenv

# Active sandbox environment (Windows PowerShell)
.\myenv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Fire Up the Telemetry Hub
```bash
python backend/run.py
```
Open **`http://127.0.0.1:5000`** in your browser to access the Dataset Ingestion Gateway!
