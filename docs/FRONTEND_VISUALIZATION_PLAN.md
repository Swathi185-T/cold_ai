# COLDCHAIN AI — Frontend Visualization Plan

**Generated:** 2026-09-30  
**Purpose:** Recommended visualization approach for every hidden backend feature  
**Rule:** No implementation until user approval

---

## PLAN OVERVIEW

This document proposes how to surface every hidden backend feature identified in `HIDDEN_BACKEND_FEATURES.md`. Changes are grouped into implementation phases by priority.

---

## PHASE 1: Multi-Sensor Pipeline (P0)

### 1.1 — Dynamic Sensor Selection Across All Pages

**Current:** Every view calls `Sensor.objects.first()` → always CC-01.

**Proposed backend change:**
- Add `?sensor=CC-02` query parameter support to `page()`, `dashboard()`, `home_page()`, and all `derived()` API views
- Default to `CC-01` if no parameter given
- Validate sensor exists, return 404 if not

**Proposed frontend change:**
- Add a **sensor selector dropdown** to the `base_control_center.html` sidebar (below the brand)
- Populated dynamically from `GET /api/sensors/`
- On selection change, reload the current page with `?sensor=<id>` parameter
- All pages automatically re-render with the selected sensor's pipeline data

**Visualization:** Compact dropdown styled as a dark glass pill, showing sensor ID + location.

---

### 1.2 — Dynamic Sensor Fleet Table

**Current:** `sensors.html` hardcodes 3 rows. `/api/sensors/` returns only `Sensor` model fields (no readings).

**Proposed backend change:**
- Enhance `/api/sensors/` to return per-sensor reading statistics:
  ```json
  {
    "results": [
      {
        "sensor_id": "CC-01",
        "location": "...",
        "product_type": "Food",
        "active": true,
        "reading_count": 4000,
        "latest_temperature": 3.93,
        "latest_humidity": 70.0,
        "latest_ambient": 19.2,
        "latest_power_kw": 1.0,
        "latest_compressor_state": true,
        "latest_door_open": false,
        "latest_timestamp": "2026-01-03T18:39:00Z",
        "temp_min": 3.51,
        "temp_max": 9.94,
        "temp_avg": 5.42
      }
    ]
  }
  ```

**Proposed frontend change:**
- `sensors.html` fetches `/api/sensors/` on load
- Fleet table rows generated dynamically from API response
- Show ALL 6 sensors (including uploaded ones)
- Click a sensor → fetch real historical readings and plot them

**Visualization:**
- Fleet table: dark glass table with status indicators (green dot = active, gray = inactive)
- Historical chart: Replace sine-wave mock with real DB query (new API endpoint: `GET /api/sensors/<id>/history/?limit=50`)

---

### 1.3 — Multi-Sensor Live Monitoring

**Current:** CC-02 and CC-03 are hardcoded static HTML. Only CC-01 updates.

**Proposed backend change:**
- New API endpoint: `GET /api/pipeline/?sensor=CC-02` (or separate per-sensor endpoint)
- Alternatively: `GET /api/pipeline/all/` returning data for all active simulation sensors

**Proposed frontend change:**
- `live_monitoring.html` polls `/api/pipeline/?sensor=<id>` for EACH active sensor
- All 3 sensor cards update dynamically
- Each card has its own timeline chart
- Or: single timeline with 3 colored traces (CC-01 blue, CC-02 green, CC-03 amber)

**Visualization:**
- 3 sensor cards with live-updating values (already structured, just needs dynamic data)
- Unified timeline canvas with multi-trace overlay
- Footer shows real `reading.timestamp` from API instead of client time

---

## PHASE 2: Data Fidelity (P1)

### 2.1 — Real Pareto Canvas Mapping

**Current:** Fixed coordinates `(50%, 50%)` or `(45%, 55%)`.

**Proposed frontend change (no backend change needed):**
- `server_dashboard.html` and `optimization.html`: Map `(estimated_energy_kwh, safety_risk)` to actual canvas pixel coordinates
- X-axis: energy (kWh), Y-axis: safety risk score
- Scale axes based on data range with padding
- When multiple Pareto points exist, plot all with the selected one highlighted
- Tooltip on hover showing all 5 fields per solution

**Visualization:**
- Scatter plot with proper axis labels and gridlines
- Selected solution: larger marker + ring + label
- Each non-dominated point clickable to show its decision variables

---

### 2.2 — Real Historical Observed Data in Predictions

**Current:** 10 mock points via `Math.sin(i * 0.7) * 0.2`.

**Proposed backend change:**
- Add last 20 real temperature readings to the `page()` context for predictions:
  ```python
  historical = list(sensor.readings.order_by('-timestamp')[:20].values_list('temperature', flat=True))
  historical.reverse()
  ```

**Proposed frontend change:**
- `predictions.html` canvas: Plot real historical readings before the forecast trajectory
- Clear visual transition point (vertical dashed line) between "Observed" and "Predicted"
- Observed points in solid color, predicted in gradient/dashed

---

### 2.3 — Surface Pipeline Data in Live Monitoring

**Current:** `/api/pipeline/` returns forecast, risk, Pareto, recommendation — all discarded.

**Proposed frontend change (no backend change):**
- Below the sensor cards, add a collapsible "AI Analysis" panel showing:
  - Mini forecast sparkline (15 points)
  - Risk badge with score
  - Recommended action summary (cooling %, duty %)
  - Updates on each poll cycle

**Visualization:**
- Compact panel with 3 mini-cards: FORECAST (sparkline), RISK (meter), ACTION (parameters)
- Updates every poll cycle alongside the sensor readings

---

### 2.4 — Fix Predictions Safety Margin

**Current:** `{{ 5.0|add:"-1" }}` outputs `4.0` for every row.

**Proposed fix:**
- Compute safety margin in JS: `(5.0 - forecastTemp).toFixed(2)`
- Or compute in the view and pass as context
- Color-code: green if margin > 1°C, yellow if 0–1°C, red if negative

---

### 2.5 — Functional Simulation Cursor

**Current:** Cursor increments but `decision_for_sensor()` always uses the latest 100 readings.

**Proposed backend change:**
- Modify `decision_for_sensor()` to accept an optional `offset` parameter
- When simulation cursor is active, use `readings[cursor:cursor+100]` instead of the last 100
- This makes START/PAUSE/RESET actually change the data the AI processes

**Impact:** Simulation becomes meaningful — stepping through time shows how risk and recommendations change.

---

### 2.6 — Post-Upload Analysis

**Current:** Upload succeeds but data is never analyzed.

**Proposed frontend change:**
- After successful upload, show a "Run Analysis" button
- Button calls `GET /api/pipeline/?sensor=<uploaded_sensor_id>`
- Display the forecast, risk, and recommendation for the uploaded data
- Or redirect to the predictions page with `?sensor=<id>`

---

## PHASE 3: Polish (P2)

### 3.1 — Model Page Uses API Data

Replace hardcoded values in `model.html` with data from either:
- SSR context `metrics` (already passed by `page()` but unused), or
- Fetch `/api/model/` on load

### 3.2 — Show Sensor ID on Dashboard

Add `{{ data.sensor }}` badge to the dashboard header so the user knows which sensor is being analyzed.

### 3.3 — Show Recommendation Explanation

Add `{{ data.recommended_solution.explanation }}` to the home page optimization section.

### 3.4 — Show All Pareto Decision Variables

On optimization page, add a table showing all Pareto solutions with ALL 5 fields:
- `cooling_intensity`, `compressor_duty_cycle`, `target_temperature_offset`, `safety_risk`, `estimated_energy_kwh`

### 3.5 — Upload Preview Shows All Columns

Expand the upload preview table to show humidity, ambient_temperature, power_kw, compressor_state, door_open.

### 3.6 — Show Upload Provenance

Display the `provenance` field returned by the upload API.

### 3.7 — Error Handling for POST Endpoints

Add proper error handling for simulation, alert resolve, and report generation POST calls. Currently, responses are ignored — if the server returns an error, the user sees no feedback.

### 3.8 — Reports List from API

Replace the hardcoded report table in `reports.html` with data from `GET /api/reports/`. This would show any dynamically generated reports.

### 3.9 — Explain `target_temperature_offset`

Add a tooltip or footnote explaining the third NSGA-II decision variable.

---

## NEW API ENDPOINTS NEEDED

| Endpoint | Method | Purpose | Phase |
|----------|--------|---------|-------|
| `GET /api/sensors/<id>/history/` | GET | Return last N readings for a specific sensor | Phase 1 |
| `GET /api/sensors/<id>/stats/` | GET | Return min/max/avg/count for a sensor | Phase 1 |
| `GET /api/pipeline/?sensor=<id>` | GET | Run pipeline for a specific sensor | Phase 1 |

---

## BACKEND CHANGES NEEDED

| Change | Scope | Phase |
|--------|-------|-------|
| Add `?sensor=` parameter to views | `views.py` — 5 view functions | Phase 1 |
| Enhance `/api/sensors/` with reading stats | `views.py:sensors_api` | Phase 1 |
| New `/api/sensors/<id>/history/` endpoint | New view + URL | Phase 1 |
| Add historical readings to predictions context | `views.py:page()` | Phase 2 |
| Make simulation cursor affect data window | `analysis_service.py` | Phase 2 |

---

## FRONTEND CHANGES NEEDED

| Template | Changes | Phase |
|----------|---------|-------|
| `base_control_center.html` | Add sensor selector dropdown | Phase 1 |
| `sensors.html` | Dynamic fleet table from API, real history chart | Phase 1 |
| `live_monitoring.html` | Poll all sensors, display all dynamically | Phase 1 |
| `server_dashboard.html` | Fix Pareto canvas coordinates, show sensor ID | Phase 2 |
| `optimization.html` | Fix Pareto canvas, show all solution variables | Phase 2 |
| `predictions.html` | Real observed data, fix safety margin | Phase 2 |
| `model.html` | Use SSR context or API for metrics | Phase 3 |
| `upload.html` | Post-upload analysis, expanded preview | Phase 3 |
| `reports.html` | Use `/api/reports/` for file list | Phase 3 |
| `alerts.html` | Error handling, use GET alerts API | Phase 3 |

---

## IMPLEMENTATION PRIORITY MATRIX

| Priority | Gap IDs | Effort | Impact |
|----------|---------|--------|--------|
| **P0-Critical** | GAP-01, GAP-02, GAP-03 | Medium-High | Eliminates fabricated data, activates dead APIs |
| **P1-Significant** | GAP-04, GAP-05, GAP-06, GAP-07, GAP-09 | Medium | Surfaces hidden AI computations, fixes data fidelity |
| **P2-Minor** | GAP-08, GAP-10 through GAP-17 | Low | Polish, error handling, completeness |

---

## ⚠️ WAITING FOR USER APPROVAL

**No implementation will begin until this plan is reviewed and approved.**

Key decisions for the user:

1. **Multi-sensor support:** Should ALL 6 sensors be selectable, or only CC-01/02/03?
2. **SSR vs API:** Should pages stay SSR-rendered, or migrate to client-side fetch from APIs?
3. **Simulation cursor:** Should we make it functional (changes data) or remove it?
4. **Phase scope:** Implement all 3 phases, or start with Phase 1 only?
5. **Orphaned functions:** Should `core.py` dead functions be removed or preserved as research reference?
