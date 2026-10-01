# COLDCHAIN AI — Complete Backend → Frontend Feature Inventory

**Generated:** 2026-09-30  
**Scope:** Every database model, backend function, API endpoint, and their frontend visibility  
**Method:** Direct source-code inspection + template audit (no assumptions)

---

## 1. DATABASE SCHEMA INVENTORY

### Model: `Sensor` (table: `monitoring_sensor`)

| Field | Type | Default | Nullable | Used by API | Displayed in Frontend |
|-------|------|---------|----------|-------------|----------------------|
| `id` | AutoField (PK) | auto | No | `/api/sensors/` | ❌ Never shown |
| `sensor_id` | CharField(64, unique) | — | No | `/api/sensors/`, `/api/pipeline/`, `/api/dashboard/` | ⚠️ Partially — shown in `alerts.html` via `{{ data.sensor }}`, hardcoded elsewhere |
| `location` | CharField(120) | `'Cold room'` | No | `/api/sensors/` | ❌ Hardcoded in `sensors.html` as static text |
| `product_type` | CharField(40) | `'Food'` | No | `/api/sensors/`, risk engine input | ❌ Hardcoded in `sensors.html` as static text |
| `active` | BooleanField | `True` | No | `/api/sensors/` | ❌ Hardcoded in `sensors.html` as "Active" |

**Row counts:** 6 sensors total (CC-01, CC-02, CC-03 = simulation; UPLOAD-01, BROWSER-01, TEST-UP = uploaded)

---

### Model: `SensorReading` (table: `monitoring_sensorreading`)

| Field | Type | Default | Nullable | Used by API | Displayed in Frontend |
|-------|------|---------|----------|-------------|----------------------|
| `id` | AutoField (PK) | auto | No | Never exposed | ❌ |
| `sensor_id` | FK → Sensor | — | No | Used internally | ❌ Direct FK never shown |
| `timestamp` | DateTimeField (indexed) | — | No | `/api/pipeline/` → `reading.timestamp` | ⚠️ Returned but replaced with client `new Date()` in `live_monitoring.html` |
| `temperature` | FloatField | — | No | `/api/pipeline/`, `/api/dashboard/` → `current_temperature` | ✅ Shown in multiple pages |
| `humidity` | FloatField | — | Yes | `/api/pipeline/` → `reading.humidity` | ⚠️ Shown only for CC-01 in `live_monitoring.html`; **hardcoded** for CC-02, CC-03, sensors page |
| `ambient_temperature` | FloatField | — | Yes | `/api/pipeline/` → `reading.ambient_temperature` | ⚠️ Same as humidity — CC-01 only dynamic |
| `power_kw` | FloatField | — | Yes | `/api/pipeline/` → `reading.power_kw` | ⚠️ Same as humidity — CC-01 only dynamic |
| `compressor_state` | BooleanField | `False` | No | `/api/pipeline/` → `reading.compressor_state` | ⚠️ Same as humidity — CC-01 only dynamic |
| `door_open` | BooleanField | `False` | No | `/api/pipeline/` → `reading.door_open` | ⚠️ Same as humidity — CC-01 only dynamic |

**Unique constraint:** `(sensor, timestamp)`  
**Row counts:** 12,003 total. CC-01/02/03: 4,000 each. Temp range: ~3.5–9.9°C. Humidity avg: ~70%. Ambient avg: ~23.4°C. Power avg: ~0.98 kW.

---

## 2. API ENDPOINT INVENTORY

### 2.1 `GET /api/dashboard/` → `dashboard_api()`

**Source:** `views.py:74-79`  
**Pipeline:** Calls `decision_for_sensor(first_sensor)`, strips `latest_reading`

| Response Field | Type | Source | Frontend Usage |
|---------------|------|--------|----------------|
| `sensor` | string | `sensor.sensor_id` | ❌ Only fetched by `operations_dashboard.html` (legacy fallback); **never by `server_dashboard.html`** |
| `current_temperature` | float | `readings[-1].temperature` | ❌ `server_dashboard.html` uses SSR context, not this API |
| `forecast` | list[float] (15 items) | MAD-TCN inference | ❌ Same — SSR only |
| `risk` | object | `core.risk()` | ❌ Same — SSR only |
| `risk.risk_score` | float | computed | ❌ |
| `risk.risk_level` | string | LOW/MEDIUM/HIGH/CRITICAL | ❌ |
| `risk.risk_reason` | string | formatted | ❌ |
| `risk.predicted_breach_time` | int or null | first breach step | ❌ |
| `pareto_solutions` | list[object] | NSGA-II results | ❌ |
| `pareto_solutions[].cooling_intensity` | float | decision var | ❌ |
| `pareto_solutions[].compressor_duty_cycle` | float | decision var | ❌ |
| `pareto_solutions[].target_temperature_offset` | float | decision var | ❌ |
| `pareto_solutions[].safety_risk` | float | objective 1 | ❌ |
| `pareto_solutions[].estimated_energy_kwh` | float | objective 2 | ❌ |
| `recommended_solution` | object | min weighted | ❌ |
| `recommended_solution.cooling_intensity` | float | raw (0-1) | ❌ |
| `recommended_solution.compressor_duty_cycle` | float | raw (0-1) | ❌ |
| `recommended_solution.target_temperature_offset` | float | raw (0-1) | ❌ |
| `recommended_solution.safety_risk` | float | objective | ❌ |
| `recommended_solution.estimated_energy_kwh` | float | objective | ❌ |
| `recommended_solution.expected_temperature` | float | computed | ❌ |
| `recommended_solution.explanation` | string | static text | ❌ |

> **FINDING:** This entire API endpoint is **dead** — only the legacy `operations_dashboard.html` template calls it, and the primary `server_dashboard.html` uses SSR context instead.

---

### 2.2 `GET /api/pipeline/` → `pipeline()`

**Source:** `views.py:81-85`  
**Pipeline:** Full `decision_for_sensor()` + latest reading row

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `success` | boolean | ✅ Checked in `live_monitoring.html` |
| `data.reading.timestamp` | ISO string | ⚠️ Returned but **replaced** with client-side `new Date()` |
| `data.reading.temperature` | float | ✅ Displayed for CC-01 |
| `data.reading.humidity` | float | ✅ Displayed for CC-01 (with `|| 65` fallback) |
| `data.reading.ambient_temperature` | float | ✅ Displayed for CC-01 (with `|| 20` fallback) |
| `data.reading.power_kw` | float | ✅ Displayed for CC-01 (with `|| 0.4` fallback) |
| `data.reading.compressor_state` | boolean | ✅ Displayed for CC-01 |
| `data.reading.door_open` | boolean | ✅ Displayed for CC-01 |
| `data.sensor` | string | ❌ Unused |
| `data.current_temperature` | float | ❌ Unused (duplicate of reading.temperature) |
| `data.forecast` | list[float] | ❌ **UNUSED** — 15-step forecast is returned but never displayed in live monitoring |
| `data.risk.risk_level` | string | ✅ Displayed for CC-01 |
| `data.risk.risk_score` | float | ❌ Unused |
| `data.risk.risk_reason` | string | ❌ Unused |
| `data.risk.predicted_breach_time` | int/null | ❌ Unused |
| `data.pareto_solutions` | list[object] | ❌ Unused |
| `data.recommended_solution` | object | ❌ Unused |

> **FINDING:** The pipeline API returns the **full decision payload** but `live_monitoring.html` uses only 8 of 20+ fields.

---

### 2.3 `GET /api/model/` → `model_api()`

**Source:** `views.py:86-89`

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `success` | boolean | ❌ |
| `data.model` | string (`"MAD-TCN"`) | ❌ **DEAD** — `model.html` hardcodes this |
| `data.input` | string (`"60 x 12"`) | ❌ Hardcoded |
| `data.output_steps` | int (15) | ❌ Hardcoded |
| `data.device` | string (`"CPU"`) | ❌ Hardcoded |
| `data.metrics.mae` | float | ❌ Hardcoded as `"1.2501 / 1.4672"` |
| `data.metrics.rmse` | float | ❌ Hardcoded |
| `data.metrics.dataset` | string | ❌ Hardcoded |

> **FINDING:** This entire API endpoint is **dead** — `model.html` never fetches it.

---

### 2.4 `GET /api/predictions/` → `derived(kind='predictions')`

**Source:** `views.py:90-99`  
**Returns:** `{'success': True, 'data': result['forecast']}` → list of 15 floats

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `success` | boolean | ❌ |
| `data` | list[float] (15 items) | ❌ **DEAD** — `predictions.html` uses SSR `{{ data.forecast }}` |

> **FINDING:** Dead endpoint.

---

### 2.5 `GET /api/risk/` → `derived(kind='risk')`

**Source:** `views.py:90-99`  
**Returns:** `{'success': True, 'data': result['risk']}`

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `success` | boolean | ❌ |
| `data.risk_score` | float | ❌ **DEAD** — pages use SSR context |
| `data.risk_level` | string | ❌ |
| `data.risk_reason` | string | ❌ |
| `data.predicted_breach_time` | int/null | ❌ |

> **FINDING:** Dead endpoint.

---

### 2.6 `GET /api/optimization/` → `derived(kind='optimization')`

**Source:** `views.py:90-99`  
**Returns:** `{'success': True, 'data': result['recommended_solution']}`

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `success` | boolean | ❌ |
| `data.cooling_intensity` | float | ❌ **DEAD** — `optimization.html` uses SSR |
| `data.compressor_duty_cycle` | float | ❌ |
| `data.target_temperature_offset` | float | ❌ |
| `data.safety_risk` | float | ❌ |
| `data.estimated_energy_kwh` | float | ❌ |
| `data.expected_temperature` | float | ❌ |
| `data.explanation` | string | ❌ |

> **FINDING:** Dead endpoint.

---

### 2.7 `GET /api/alerts/` → `derived(kind='alerts')`

**Source:** `views.py:94-97`  
**Returns:** `{'success': True, 'data': [alert_objects]}` — dynamic from risk + cache

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `success` | boolean | ❌ |
| `data[]` | array | ❌ **DEAD** — `alerts.html` uses SSR context + hardcoded Alert 2 |
| `data[].id` | string | ❌ |
| `data[].severity` | string | ❌ |
| `data[].sensor` | string | ❌ |
| `data[].message` | string | ❌ |
| `data[].resolved` | boolean | ❌ |

> **FINDING:** Dead GET endpoint. Only the POST `/api/alerts/<id>/resolve/` is used.

---

### 2.8 `GET /api/sensors/` → `sensors_api()`

**Source:** `views.py:80`  
**Returns:** `{'results': list(Sensor.objects.values())}`

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `results[]` | array | ❌ **DEAD** |
| `results[].id` | int | ❌ |
| `results[].sensor_id` | string | ❌ — `sensors.html` hardcodes CC-01/02/03 |
| `results[].location` | string | ❌ — Hardcoded |
| `results[].product_type` | string | ❌ — Hardcoded |
| `results[].active` | boolean | ❌ — Hardcoded |

> **FINDING:** Dead endpoint. Also: returns ONLY `Sensor` model fields — does NOT return any reading aggregates (min/max/avg temp, latest reading, humidity, power). The `sensors.html` page needs this data but hardcodes it instead.

---

### 2.9 `GET /api/reports/` → `reports_api()`

**Source:** `views.py:160-161`  
**Returns:** `{'success': True, 'files': [filenames]}`

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `success` | boolean | ❌ |
| `files[]` | array of strings | ❌ **DEAD** — `reports.html` hardcodes report file list |

> **FINDING:** Dead endpoint.

---

### 2.10 `POST /api/simulation/{start|pause|reset}/` → `simulation()`

**Source:** `views.py:100-114`

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `success` | boolean | ❌ Ignored by `live_monitoring.html` JS |
| `data.simulation_state` | string | ❌ Ignored — UI updates optimistically |
| `data.simulation_cursor` | int | ❌ Ignored |
| `data.source` | string | ❌ Ignored |

> **FINDING:** Response payload completely ignored. The JS updates UI optimistically.

---

### 2.11 `POST /api/alerts/{alert_id}/resolve/` → `resolve_alert()`

**Source:** `views.py:115-118`

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `success` | boolean | ❌ Ignored — DOM manipulated unconditionally |
| `data.id` | string | ❌ Ignored |
| `data.resolved` | boolean | ❌ Ignored |

---

### 2.12 `POST /api/upload/` → `upload_api()`

**Source:** `views.py:119-142`

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `success` | boolean | ✅ Checked |
| `rows_received` | int | ✅ Displayed in `#statRowsReceived` |
| `rows_valid` | int | ✅ Displayed in `#statRowsValid` |
| `rows_persisted` | int | ✅ Displayed in `#statRowsPersisted` |
| `preview` | array of row dicts | ⚠️ Partially — only `timestamp`, `sensor_id`, `temperature` shown in table |
| `preview[].humidity` | float | ❌ Not shown in preview |
| `preview[].ambient_temperature` | float | ❌ Not shown in preview |
| `preview[].power_kw` | float | ❌ Not shown in preview |
| `preview[].compressor_state` | string | ❌ Not shown in preview |
| `preview[].door_open` | string | ❌ Not shown in preview |
| `provenance` | string | ❌ Never rendered |
| `errors` | array of strings | ✅ Displayed on failure |

---

### 2.13 `POST /api/reports/generate/` → `generate_report()`

**Source:** `views.py:146-159`

| Response Field | Type | Frontend Usage |
|---------------|------|----------------|
| `success` | boolean | ✅ Checked |
| `files` | array of strings | ❌ Ignored — hardcoded in template |

---

### 2.14 `GET /reports/{name}/` → `report_file()`

**Source:** `views.py:162-165`  
**Returns:** FileResponse (binary download or text)

| Usage | Frontend |
|-------|----------|
| Download link | ✅ Used by `reports.html` download buttons |
| Inline viewer | ✅ Used by `reports.html` `viewReport()` |

---

## 3. BACKEND FUNCTION INVENTORY

### 3.1 Active Pipeline Functions (used by `analysis_service.decision_for_sensor()`)

| Function | Module | Purpose | Exposed via API | Shown in Frontend |
|----------|--------|---------|-----------------|-------------------|
| `decision_for_sensor(sensor)` | `analysis_service.py` | Central pipeline bridge | Yes (all APIs) | Yes (SSR + some API) |
| `prepare(frame)` | `core_preprocessing.py` | Feature engineering (12 features) | Indirectly | ❌ Feature values never shown |
| `forecast(sequence)` | `ml/inference.py` | MAD-TCN inference | Yes → `forecast` list | ✅ Charts + tables |
| `risk(prediction, profile)` | `core.py` | Future risk scoring | Yes → `risk` dict | ✅ Multiple pages |
| `run_nsga2(current, ambient, risk)` | `optimization/nsga2_optimizer.py` | NSGA-II optimization | Yes → `pareto_solutions` + `recommended_solution` | ✅ Multiple pages |

### 3.2 UNUSED Backend Functions (exist but NOT called by active pipeline)

| Function | Module | Purpose | Called By | Frontend Visibility |
|----------|--------|---------|-----------|---------------------|
| `clean_frame(frame)` | `core.py:7-15` | Alternative preprocessing | **NOTHING** | ❌ |
| `predict_future(temperatures, horizon=15)` | `core.py:16-17` | Linear extrapolation forecast | **NOTHING** | ❌ |
| `energy(current, ambient, intensity, duty)` | `core.py:20` | Standalone energy calc | **NOTHING** (NSGA-II has its own inline version) | ❌ |
| `optimize(current, ambient, future_risk)` | `core.py:21-27` | Grid-search optimizer | **NOTHING** (replaced by pymoo NSGA-II) | ❌ |
| `prediction_guided_optimization(state, profile)` | `core.py:28-29` | Combined pipeline using linear forecast + grid search | **NOTHING** | ❌ |
| `sequences(df, window, horizon)` | `core_preprocessing.py:12-13` | Training data windowing | **NOTHING** (training is offline) | ❌ |

### 3.3 Backend Computations Available but NOT Surfaced

| Computation | Source | Available Data | Frontend Visibility |
|------------|--------|----------------|---------------------|
| Per-sensor reading statistics (min/max/avg/count for all 6 sensors) | Database query on `SensorReading` | All 12,003 rows queryable | ❌ Hardcoded in sensors page |
| Historical temperature timeseries | Database `SensorReading.objects.filter(sensor=...)` | 4,000 points per sim sensor | ❌ Replaced with sine-wave mock |
| Multi-sensor forecasting | Could call `decision_for_sensor()` per sensor | CC-01, CC-02, CC-03 | ❌ Only CC-01 is processed |
| Reading field aggregates (humidity, ambient, power) | Database aggregation | Rich multivariate data | ❌ Hardcoded static values |
| Per-sensor risk assessment | `decision_for_sensor()` per sensor | Separate risk per zone | ❌ Only CC-01 assessed |
| Upload data analysis | Uploaded sensors exist in DB | UPLOAD-01, BROWSER-01, TEST-UP | ❌ Never analyzed after upload |
| Preprocessing feature values | `prepare()` output DataFrame | All 12 engineered features | ❌ Never exposed |
| Pareto solution details | `run_nsga2()` | `cooling_intensity`, `compressor_duty_cycle`, `target_temperature_offset` per point | ⚠️ Only `safety_risk` and `energy` plotted; other 3 vars ignored on canvas |
| Simulation cursor state | Cache-backed | Cursor position, state string | ❌ Response ignored by frontend |

---

## 4. SSR CONTEXT vs API USAGE MATRIX

| Page Template | Data Source | SSR Context Variables Used | API Calls Made |
|---------------|-----------|---------------------------|----------------|
| `home.html` | SSR only | `data`, `metrics`, `forecast_json`, `pareto_json`, `has_data`, `sensor_count` | None |
| `server_dashboard.html` | SSR only | `data`, `sensor_count`, `now` | None |
| `live_monitoring.html` | SSR + API | `data.current_temperature`, `data.risk.risk_level` | `/api/simulation/{action}/`, `/api/pipeline/` |
| `predictions.html` | SSR only | `data.forecast`, `data.risk`, `metrics` | None |
| `optimization.html` | SSR only | `data.pareto_solutions`, `data.recommended_solution` | None |
| `alerts.html` | SSR + API | `data.sensor`, `data.risk` | `POST /api/alerts/{id}/resolve/` |
| `sensors.html` | SSR only | `sensor_count` (only!) | None |
| `model.html` | Neither | Nothing from context used | None |
| `upload.html` | API only | Nothing from context used | `POST /api/upload/` |
| `reports.html` | API only | Nothing from context used | `POST /api/reports/generate/`, `GET /reports/{file}/` |
| `methodology.html` | Neither | Nothing from context used | None |

---

## 5. ROUTE MAP

### Page Routes

| URL | View Function | Template | Notes |
|-----|--------------|----------|-------|
| `/` | `home_page()` | `home.html` | Product landing page |
| `/dashboard/` | `dashboard()` | `server_dashboard.html` | Operations center |
| `/live-monitoring/` | `page(name='Live Monitoring')` | `live_monitoring.html` | IoT simulation |
| `/predictions/` | `page(name='Predictions')` | `predictions.html` | MAD-TCN forecasts |
| `/optimization/` | `page(name='Optimization')` | `optimization.html` | NSGA-II results |
| `/alerts/` | `page(name='Alerts')` | `alerts.html` | Alert management |
| `/sensors/` | `page(name='Sensors')` | `sensors.html` | Sensor fleet |
| `/model/` | `page(name='Model')` | `model.html` | Architecture specs |
| `/upload/` | `page(name='Upload')` | `upload.html` | CSV ingestion |
| `/reports/` | `page(name='Reports')` | `reports.html` | Report generation |
| `/methodology/` | `page(name='Methodology')` | `methodology.html` | Research docs |

### API Routes

| URL | Method | View Function | Status |
|-----|--------|--------------|--------|
| `/api/dashboard/` | GET | `dashboard_api()` | 🔴 DEAD (no active frontend consumer) |
| `/api/pipeline/` | GET | `pipeline()` | 🟡 Partially used (by `live_monitoring.html` only) |
| `/api/model/` | GET | `model_api()` | 🔴 DEAD |
| `/api/predictions/` | GET | `derived('predictions')` | 🔴 DEAD |
| `/api/risk/` | GET | `derived('risk')` | 🔴 DEAD |
| `/api/optimization/` | GET | `derived('optimization')` | 🔴 DEAD |
| `/api/alerts/` | GET | `derived('alerts')` | 🔴 DEAD |
| `/api/sensors/` | GET | `sensors_api()` | 🔴 DEAD |
| `/api/reports/` | GET | `reports_api()` | 🔴 DEAD |
| `/api/simulation/{action}/` | POST | `simulation()` | 🟡 Called but response ignored |
| `/api/alerts/{id}/resolve/` | POST | `resolve_alert()` | 🟡 Called but response ignored |
| `/api/upload/` | POST | `upload_api()` | ✅ Fully used |
| `/api/reports/generate/` | POST | `generate_report()` | 🟡 Called; `files` field ignored |
| `/reports/{name}/` | GET | `report_file()` | ✅ Fully used |

---

## 6. SUMMARY COUNTS

| Category | Count |
|----------|-------|
| Database models | 2 |
| Database tables | 2 (+Django system tables) |
| Database rows (SensorReading) | 12,003 |
| Database rows (Sensor) | 6 |
| Sensor model fields | 5 |
| SensorReading model fields | 9 |
| Total database fields | 14 |
| API endpoints | 14 |
| 🔴 Dead API endpoints (no frontend consumer) | 8 |
| 🟡 Partially used API endpoints | 4 |
| ✅ Fully used API endpoints | 2 |
| Backend functions (active pipeline) | 5 |
| Backend functions (UNUSED / orphaned) | 5 |
| Total unique backend data fields (across all APIs) | 34 |
| Fields actually displayed in frontend | 16 |
| Fields returned by APIs but hidden | 18 |
| Hardcoded values that should be dynamic | 23+ |
| Templates | 14 (12 active + 2 legacy fallback) |
| Templates using SSR only | 7 |
| Templates using API fetch | 4 |
| Templates using neither context nor API | 2 |
