# COLDCHAIN AI — Hidden Backend Features Report

**Generated:** 2026-09-30  
**Purpose:** Catalog every backend capability that exists but is NOT visible or usable in the frontend  
**Priority:** P0 (critical gap), P1 (significant gap), P2 (minor improvement)

---

## EXECUTIVE SUMMARY

| Category | Count |
|----------|-------|
| Dead API endpoints (fully functional but no frontend consumer) | 8 |
| Orphaned backend functions (exist but never called) | 5 |
| API response fields returned but not displayed | 18 |
| Database columns with rich data but hardcoded in UI | 23+ values |
| Sensors with real data but never analyzed | 2 (CC-02, CC-03) |
| Sensors in DB but completely invisible | 3 (UPLOAD-01, BROWSER-01, TEST-UP) |

**Bottom line:** The backend has a capable data pipeline, but the frontend uses only ~47% of available data fields. 8 of 14 API endpoints have zero active consumers. The entire multi-sensor architecture is wasted — only CC-01 is ever processed through MAD-TCN.

---

## P0 — CRITICAL GAPS

### GAP-01: Multi-Sensor Pipeline is Single-Sensor Only

**Backend reality:**
- Database has 6 sensors with data
- `decision_for_sensor()` accepts ANY sensor as argument
- CC-02 and CC-03 each have 4,000 readings — enough for MAD-TCN inference

**Frontend reality:**
- `home_page()` calls `Sensor.objects.first()` → always CC-01
- `dashboard()` calls `Sensor.objects.first()` → always CC-01
- `page()` calls `Sensor.objects.first()` → always CC-01
- ALL API views call `Sensor.objects.first()` → always CC-01
- `live_monitoring.html` fetches `/api/pipeline/` → CC-01 data only
- CC-02 and CC-03 cards in live monitoring are **100% hardcoded static HTML**
- `sensors.html` fleet table is **100% hardcoded static HTML**

**Impact:** The system claims multi-node IoT monitoring but processes only one node.

**Priority:** P0

---

### GAP-02: Sensor Fleet Page Shows Fabricated Data

**Backend reality:**
- `/api/sensors/` returns real sensor records from DB (6 sensors)
- Database contains real humidity (~70%), ambient (~23.4°C), power (~0.98kW) per reading

**Frontend reality:**
- `sensors.html` **never calls `/api/sensors/`**
- All 3 fleet rows are hardcoded HTML:
  - CC-01: `3.93°C`, `65.0%`, `20.5°C`, `0.42 kW`
  - CC-02: `3.48°C`, `68.2%`, `21.0°C`, `0.38 kW`
  - CC-03: `4.12°C`, `62.5%`, `22.1°C`, `0.45 kW`
- The "Historical Temperature" canvas shows a **sine-wave mock** (`Math.sin(i * 0.45) * 0.35`) instead of real DB readings
- 3 uploaded sensors (UPLOAD-01, BROWSER-01, TEST-UP) are completely invisible

**Impact:** The page displays fabricated values while real data exists in the database.

**Priority:** P0

---

### GAP-03: 8 Dead API Endpoints

These endpoints work perfectly (all return HTTP 200 with real data) but no frontend template fetches them:

| Endpoint | Returns | Frontend Consumer |
|----------|---------|------------------|
| `GET /api/dashboard/` | Full pipeline result (34 fields) | None (legacy `operations_dashboard.html` only) |
| `GET /api/model/` | Model specs + metrics (8 fields) | None (`model.html` hardcodes everything) |
| `GET /api/predictions/` | 15-step forecast array | None (`predictions.html` uses SSR) |
| `GET /api/risk/` | Risk assessment (4 fields) | None (`predictions.html` uses SSR) |
| `GET /api/optimization/` | Recommended solution (7 fields) | None (`optimization.html` uses SSR) |
| `GET /api/alerts/` | Active alerts with cache resolution | None (`alerts.html` uses SSR) |
| `GET /api/sensors/` | All 6 sensor records | None (`sensors.html` hardcodes) |
| `GET /api/reports/` | List of generated report files | None (`reports.html` hardcodes list) |

**Impact:** APIs exist for a REST-driven SPA architecture but the frontend is SSR-only (except for 4 POST endpoints). The REST API layer is essentially a dead codebase.

**Priority:** P0 (if the project claims REST API architecture) / P1 (if SSR is acceptable)

---

## P1 — SIGNIFICANT GAPS

### GAP-04: Live Monitoring Discards Rich Pipeline Data

**Backend returns from `/api/pipeline/`:**
- ✅ `reading.temperature` — displayed
- ✅ `reading.humidity` — displayed (CC-01 only)
- ✅ `reading.ambient_temperature` — displayed (CC-01 only)
- ✅ `reading.power_kw` — displayed (CC-01 only)
- ✅ `reading.compressor_state` — displayed (CC-01 only)
- ✅ `reading.door_open` — displayed (CC-01 only)
- ❌ `reading.timestamp` — replaced with client `new Date()`
- ❌ `forecast` (15 values) — **completely discarded**
- ❌ `risk.risk_score` — discarded
- ❌ `risk.risk_reason` — discarded
- ❌ `risk.predicted_breach_time` — discarded
- ❌ `pareto_solutions` — discarded
- ❌ `recommended_solution` — discarded
- ❌ `sensor` — discarded
- ❌ `current_temperature` — discarded

**Impact:** The pipeline runs full MAD-TCN + NSGA-II on every poll but the page shows only raw sensor readings. The expensive AI computation is wasted.

**Priority:** P1

---

### GAP-05: Pareto Canvas Shows Fixed Coordinates

**Backend returns:** Real `(safety_risk, estimated_energy_kwh)` coordinate pairs for each non-dominated solution, plus `cooling_intensity`, `compressor_duty_cycle`, and `target_temperature_offset`.

**Frontend reality:**
- `server_dashboard.html`: Pareto point drawn at **fixed `(50%, 50%)`** canvas coordinates
- `optimization.html`: Pareto point drawn at **fixed `(45%, 55%)`** canvas coordinates
- Neither template maps actual values to the coordinate space
- `cooling_intensity`, `compressor_duty_cycle`, and `target_temperature_offset` are ignored on both canvases

**Impact:** The Pareto visualization is cosmetic — it doesn't represent real optimization trade-off geometry.

**Priority:** P1

---

### GAP-06: Predictions Page Uses Mock Historical Data

**Backend has:** 4,000 real historical temperature readings per sensor in the database.

**Frontend does:** Generates 10 mock "observed" points via `currentTemp + Math.sin(i * 0.7) * 0.2` before plotting the real 15-step MAD-TCN forecast.

**Impact:** The observed trajectory on the predictions chart is synthetic, not from the database. The transition from observed to predicted is fabricated.

**Priority:** P1

---

### GAP-07: Uploaded Sensor Data Never Analyzed

**Backend reality:**
- Upload API successfully persists data to DB (verified: UPLOAD-01, BROWSER-01, TEST-UP exist)
- `decision_for_sensor()` could run on any sensor with ≥60 readings

**Frontend reality:**
- After upload, the success message says "Data ingested into SQLite storage"
- But no page ever runs inference on uploaded data
- Uploaded sensors don't appear in the sensor fleet table
- No way to select a sensor for analysis

**Impact:** The upload feature is a dead end — data goes in but never comes out.

**Priority:** P1

---

### GAP-08: Upload Preview Hides Most Columns

**Backend returns:** Full row dictionaries with all columns (timestamp, sensor_id, temperature, humidity, ambient_temperature, power_kw, compressor_state, door_open).

**Frontend shows:** Only timestamp, sensor_id, temperature in the preview table.

**Also hidden:** `provenance` field (`"Upload data; training is not triggered."`) is never shown.

**Priority:** P2

---

### GAP-09: Simulation Cursor Has No Effect

**Backend reality:**
- `/api/simulation/start/` increments `simulation_cursor` in cache
- `/api/simulation/reset/` sets cursor to 0

**Frontend reality:**
- The cursor value is returned in the API response but **completely ignored**
- `decision_for_sensor()` always uses `sensor.readings.order_by('-timestamp')[:100]` regardless of cursor position
- The simulation doesn't actually "step through records" — it always returns the same latest 100 readings

**Impact:** The simulation is cosmetic. START/PAUSE/RESET buttons change UI state but the data never changes.

**Priority:** P1

---

### GAP-10: Model Page Hardcodes Values Available via API

**Backend endpoint `/api/model/` returns:**
```json
{
  "model": "MAD-TCN",
  "input": "60 x 12",
  "output_steps": 15,
  "device": "CPU",
  "metrics": {"mae": 1.2501, "rmse": 1.4672, "dataset": "SIMULATION"}
}
```

**Frontend `model.html`:** Hardcodes all these values as static HTML text. MAE/RMSE are hardcoded as `"1.2501 / 1.4672"`. The metrics from `metrics.json` are passed in the SSR context via `page()` view but never referenced in the template.

**Priority:** P2

---

## P2 — MINOR IMPROVEMENTS

### GAP-11: Explanation Field Hidden on Home Page

`data.recommended_solution.explanation` is passed in context but never rendered on `home.html`.

### GAP-12: Sensor ID Not Shown on Dashboard

`data.sensor` (e.g., `"CC-01"`) is returned by the pipeline but never displayed on the dashboard or home page. The user doesn't know which sensor is being analyzed.

### GAP-13: Alert Response Ignored

Both `POST /api/alerts/{id}/resolve/` and `POST /api/simulation/{action}/` return structured JSON responses that the frontend completely ignores. No error handling if the POST fails.

### GAP-14: Reports Generate Response Ignored

`POST /api/reports/generate/` returns `{"files": [...]}` but the frontend ignores the `files` list and hardcodes the three filenames.

### GAP-15: Pareto Solution Details Hidden

Each Pareto solution contains `cooling_intensity`, `compressor_duty_cycle`, and `target_temperature_offset`, but canvases only plot `(safety_risk, estimated_energy_kwh)`. The 3 decision variables are invisible.

### GAP-16: `target_temperature_offset` Never Explained

NSGA-II's third decision variable (`target_temperature_offset`, range 0.0–1.0) is computed and returned but never shown or explained anywhere in the UI.

### GAP-17: Predictions Safety Margin Bug

`predictions.html` uses `{{ 5.0|add:"-1" }}` for safety margin, which outputs `4.0` for every row regardless of actual predicted temperature. Should be `{{ 5.0 }} - {{ t }}` or computed in JS.

---

## 5 ORPHANED BACKEND FUNCTIONS

| Function | Location | Purpose | Why Unused |
|----------|----------|---------|------------|
| `clean_frame()` | `core.py:7-15` | Alternative preprocessing | Replaced by `core_preprocessing.prepare()` |
| `predict_future()` | `core.py:16-17` | Linear extrapolation | Replaced by MAD-TCN `ml.inference.forecast()` |
| `energy()` | `core.py:20` | Standalone energy calc | NSGA-II `_evaluate()` has its own inline version |
| `optimize()` | `core.py:21-27` | Grid-search optimizer | Replaced by pymoo NSGA-II |
| `prediction_guided_optimization()` | `core.py:28-29` | Combined linear+grid pipeline | Replaced by `analysis_service.decision_for_sensor()` |
| `sequences()` | `core_preprocessing.py:12-13` | Training window extraction | Only used during offline training, not by the web app |

---

## CONCLUSION

The backend is more capable than the frontend reveals. The most impactful changes would be:

1. **Make the sensor fleet dynamic** — fetch `/api/sensors/` and query real reading stats
2. **Process all sensors** — allow sensor selection in views, not just `Sensor.objects.first()`
3. **Use the forecast data in live monitoring** — it's already being computed and returned
4. **Fix the Pareto canvas** — map real coordinates instead of fixed positions
5. **Show real historical data** — query DB for observed trajectory instead of sine waves
6. **Make the simulation cursor actually advance the data window**
7. **Surface uploaded sensor data** for analysis

None of these require new backend code — the data already exists and is already computed. The gap is purely in the frontend's consumption of it.
