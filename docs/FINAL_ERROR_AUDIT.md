# COLDCHAIN AI — Final Hardening & Error Audit Report

**Date:** 2026-09-30  
**Project:** COLDCHAIN AI  
**Title:** AI-driven framework integrating Big Data analytics and energy-aware IoT for cold chain logistics  
**Status:** FULLY HARDENED & VERIFIED  

---

## 1. Executive Summary

A comprehensive, end-to-end audit was conducted across all subsystems of the COLDCHAIN AI platform:
`CODE → DATA → ML → RISK → OPTIMIZATION → API → UI → BROWSER`.

All identified bugs, calculation edge cases, missing API endpoints, coordinate anomalies, and validation gaps have been resolved and verified with automated test suites and live server checks.

---

## 2. External AI & API Key Audit

- **Audit Target:** Search repository for `OPENAI_API_KEY`, `OPENAI`, `GEMINI`, `ANTHROPIC`, `CLAUDE`, `API_KEY`, `.env`, `dotenv`.
- **Finding:**
  - Zero external AI API keys or dependencies are required.
  - The analytical and optimization pipeline is **100% local**:
    - Multi-scale Adaptive Dilated Temporal Convolutional Network (MAD-TCN) runs locally on PyTorch CPU.
    - Non-Dominated Sorting Genetic Algorithm II (NSGA-II) runs locally via `pymoo`.
  - No external LLM or cloud API is referenced or required at runtime.

---

## 3. Detailed Audit & Fix Matrix

### ISSUE-01: Risk Engine Crashes on Empty or Single-Element Predictions
- **Severity:** High
- **Root Cause:** In `core.risk()`, calling `p.min()` on an empty forecast array threw `ValueError: zero-size array to reduction operation minimum which has no identity`. Calling `np.diff(p).mean()` on a single-element array produced `RuntimeWarning: Mean of empty slice` and `NaN`.
- **Fix:** Added guards in `core.risk()`: if `len(p) == 0`, returns safe default risk structure; if `len(p) <= 1`, sets `diff_mean = 0.0`. Replaced non-ASCII en-dash characters with clean ASCII to prevent terminal encoding failures.
- **Files Changed:** [`core.py`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/core.py)

### ISSUE-02: NSGA-II 1D Solution Dimension Handling
- **Severity:** Medium-High
- **Root Cause:** When `pymoo.optimize.minimize` returns a single non-dominated solution, `r.X` and `r.F` may have 1D shapes (`(3,)` and `(2,)`). Zipping across 1D arrays resulted in element-wise scalar iteration rather than row iteration.
- **Fix:** Wrapped `r.X` and `r.F` in `np.atleast_2d()` and added robust fallback candidate generation in case of empty optimization return.
- **Files Changed:** [`optimization/nsga2_optimizer.py`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/optimization/nsga2_optimizer.py)

### ISSUE-03: Missing Required API Endpoints
- **Severity:** Medium
- **Root Cause:** The specification required `/api/report/`, `/api/file_content/`, `/api/save_case/`, and `/api/profile/`, but these were not mapped in `urls.py`.
- **Fix:** Implemented handlers for:
  - `GET /api/report/?sensor=<id>`: Returns structured decision audit data.
  - `POST /api/report/`: Triggers report generation package (JSON, MD, CSV).
  - `GET /api/file_content/?name=<filename>`: Securely reads report files with directory traversal prevention (`Path(name).name`).
  - `GET /api/save_case/?sensor=<id>`: Persists decision snapshot into cache session history.
  - `GET /api/profile/?profile=<name>`: Returns product safety thresholds (`PROFILES` limits).
- **Files Changed:** [`apps/monitoring/views.py`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/apps/monitoring/views.py), [`apps/monitoring/urls.py`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/apps/monitoring/urls.py)

### ISSUE-04: Static Sensor Fleet & Sine-Wave Mock Graphs
- **Severity:** High
- **Root Cause:** `sensors.html` had hardcoded static table rows and rendered synthetic sine waves (`Math.sin(i * 0.45) * 0.35`) rather than displaying actual SQLite telemetry records.
- **Fix:**
  - Enhanced `/api/sensors/` to compute and return real aggregates: `reading_count`, `latest_temperature`, `temp_min`, `temp_max`, `temp_avg`, `latest_humidity`, `latest_ambient`, `latest_power_kw`.
  - Created `/api/sensors/<sensor_id>/history/` to fetch real chronological reading traces.
  - Rewrote `sensors.html` to dynamically populate all registered sensors and draw real historical temperature curves.
- **Files Changed:** [`apps/monitoring/views.py`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/apps/monitoring/views.py), [`templates/sensors.html`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/templates/sensors.html)

### ISSUE-05: Single-Sensor Limitation Across Control Center
- **Severity:** High
- **Root Cause:** All views and endpoints invoked `Sensor.objects.first()`, ignoring nodes CC-02, CC-03, and uploaded datasets.
- **Fix:** Added universal `_get_sensor(request)` helper supporting `?sensor=<id>` across all views and APIs. Added dynamic sensor selector widget in `base_control_center.html` preserving selection across navigation.
- **Files Changed:** [`apps/monitoring/views.py`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/apps/monitoring/views.py), [`templates/base_control_center.html`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/templates/base_control_center.html)

### ISSUE-06: Live Monitoring Discarding AI Computations & Static Node 2/3
- **Severity:** Medium-High
- **Root Cause:** `live_monitoring.html` only updated CC-01, leaving CC-02 and CC-03 hardcoded. Furthermore, the pipeline's 15-step forecast, risk score, and NSGA-II actions were discarded.
- **Fix:** Rewrote `live_monitoring.html` to query all nodes dynamically, render multi-trace timeline curves, and added an **AI Pipeline Decision Support** panel showing continuous forecast sparklines, risk score meters, and NSGA-II actions.
- **Files Changed:** [`templates/live_monitoring.html`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/templates/live_monitoring.html)

### ISSUE-07: Fixed Coordinates on Pareto Frontier Visualizations
- **Severity:** Medium
- **Root Cause:** `dashboardParetoCanvas` and `optParetoCanvas` mapped solution points to fixed canvas coordinates (`50%, 50%` and `45%, 55%`) instead of scaling to actual energy and risk values.
- **Fix:** Implemented real coordinate transforms (`getPX`, `getPY`) with dynamic bounds, axis tick labels, and gridlines. Added `Target Temperature Offset` decision variable to all Pareto tables.
- **Files Changed:** [`templates/server_dashboard.html`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/templates/server_dashboard.html), [`templates/optimization.html`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/templates/optimization.html)

### ISSUE-08: Predictions Safety Margin Expression Bug & Mock History
- **Severity:** Medium
- **Root Cause:** `predictions.html` rendered `{{ 5.0|add:"-1" }}` (always displaying `4.0`), and plotted mock sine waves for observed history.
- **Fix:** Injected `historical_json` from real SQLite readings, plotted true observed data with a dashed horizon divider, and computed exact mathematical safety margins.
- **Files Changed:** [`apps/monitoring/views.py`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/apps/monitoring/views.py), [`templates/predictions.html`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/templates/predictions.html)

### ISSUE-09: Upload Data Decoupling & Ingestion Incomplete Display
- **Severity:** Low-Medium
- **Root Cause:** Upload preview table displayed only 3 columns, and users had no way to analyze newly ingested sensor data.
- **Fix:** Expanded preview table to display all 8 telemetry columns, showed provenance disclaimer, and added a 1-click CTA to launch predictive analysis on the uploaded sensor.
- **Files Changed:** [`templates/upload.html`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/templates/upload.html)

### ISSUE-10: Reports Center Disconnected from API
- **Severity:** Low-Medium
- **Root Cause:** `reports.html` hardcoded report artifact rows and never called `GET /api/reports/`.
- **Fix:** Made table dynamically populated via `loadReportList()` calling `/api/reports/`, with robust error handling for generation and viewing.
- **Files Changed:** [`templates/reports.html`](file:///c:/Projects/GitHub-Research%20(2)/GitHub-Research/COLD_CHAIN_AI/templates/reports.html)

---

## 4. Scientific Honesty & Data Disclosures

All UI templates and generated reports explicitly maintain scientific honesty:
1. **DEMONSTRATION / SIMULATION DATA:** Sensor readings originate from a 12,000-record physics-based thermal simulation model (CC-01, CC-02, CC-03).
2. **ESTIMATED / SIMULATED ENERGY:** Energy consumption values ($E$) are computed via thermodynamic estimation equations based on ambient-current delta, cooling intensity, and compressor duty cycle—**not physical utility wattmetering**.
3. **LOCAL ML EXECUTION:** PyTorch MAD-TCN inference executes locally on CPU without external API dependencies.
4. **NO PHYSICAL ACTUATOR VALIDATION:** Recommendations are decision-support setpoints and do not actuate real industrial hardware.

---

## 5. Automated Verification Results

### Django System Check
```
manage.py check
System check identified no issues (0 silenced).
```

### Migration Check
```
manage.py makemigrations --check
No changes detected.
manage.py migrate --plan
No planned migration operations.
```

### Automated Unit & Workflow Test Suite
```
manage.py test tests
Ran 31 tests in 7.971s
OK (31 / 31 passed)
```

### End-to-End Pipeline
```
python -m scripts.end_to_end
PASS
```

### Runtime Validator (`scripts/validate_runtime.py`)
- Rendered all 11 user-facing pages: **11 / 11 HTTP 200 OK**
- Validated JavaScript syntax using Node.js: **19 / 19 script blocks VALID**
- Tested all 19 REST API endpoints: **19 / 19 HTTP 200 OK**

### Live Server Route Verification (HTTP 200)
- `/`
- `/dashboard/`
- `/live-monitoring/`
- `/predictions/`
- `/optimization/`
- `/alerts/`
- `/model/`
- `/sensors/`
- `/reports/`
- `/upload/`
- `/methodology/`
- `/api/dashboard/`
- `/api/sensors/`
- `/api/sensors/CC-01/history/?limit=5`
- `/api/pipeline/?sensor=CC-01`
- `/api/model/`
- `/api/predictions/?sensor=CC-01`
- `/api/risk/?sensor=CC-01`
- `/api/optimization/?sensor=CC-01`
- `/api/alerts/?sensor=CC-01`
- `/api/report/?sensor=CC-01`
- `/api/reports/`
- `/api/file_content/?name=coldchain_report.json`
- `/api/save_case/?sensor=CC-01`
- `/api/profile/?profile=Vaccine`

---

## 6. Audit Scorecard

```
TOTAL ISSUES FOUND:     10
TOTAL ISSUES FIXED:     10
TOTAL TESTS:            31
PASSED:                 31
FAILED:                  0
WARNINGS:                0
REMAINING ISSUES:        0
```
