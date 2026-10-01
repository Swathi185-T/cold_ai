# COLDCHAIN AI — System Architecture & Design

## Overview

COLDCHAIN AI is a prediction-guided, multi-objective decision support platform for cold chain refrigeration operations. It couples deep temporal convolution forecasting (MAD-TCN) with evolutionary multi-objective optimization (NSGA-II) to deliver energy-aware temperature stabilization.

```
┌────────────────────────────────────────────────────────┐
│                   IoT SENSOR LAYER                     │
│  Temperature · Humidity · Power · Compressor · Door    │
└───────────────────────────┬────────────────────────────┘
                            │ Telemetry Stream
                            ▼
┌────────────────────────────────────────────────────────┐
│               DATA ENGINEERING PIPELINE                │
│  Cleaning · Rolling Means · Drift · 12-Feature Vector  │
└───────────────────────────┬────────────────────────────┘
                            │ Sliding Window (60 × 12)
                            ▼
┌────────────────────────────────────────────────────────┐
│                 AI FORECASTING ENGINE                  │
│       MAD-TCN (Multi-scale Adaptive Dilated TCN)       │
└───────────────────────────┬────────────────────────────┘
                            │ 15-Step Forecast Trajectory
                            ▼
┌────────────────────────────────────────────────────────┐
│                  FUTURE RISK ENGINE                    │
│     Boundary Penalty · Slope Velocity · Breach Horizon  │
└───────────────────────────┬────────────────────────────┘
                            │ Calculated Risk Score
                            ▼
┌────────────────────────────────────────────────────────┐
│         PREDICTION-GUIDED NSGA-II OPTIMIZER            │
│    Minimizes: Residual Safety Risk & Simulated Energy   │
└───────────────────────────┬────────────────────────────┘
                            │ Non-Dominated Pareto Set
                            ▼
┌────────────────────────────────────────────────────────┐
│             DECISION SUPPORT & WEB PLATFORM            │
│   Landing Page (/) · Control Center (/dashboard/)      │
│   Live IoT (/live-monitoring/) · Alerts (/alerts/)     │
└────────────────────────────────────────────────────────┘
```

---

## Component Layers

### 1. Data & Preprocessing Layer (`core_preprocessing.py`, `core.py`)
- **Ingestion:** Validates incoming CSV rows with timestamp parse and missing value check.
- **Feature Engineering:** Extracts 12 continuous and categorical signals:
  1. `temperature`: Primary thermal reading (°C)
  2. `humidity`: Chamber relative humidity (%)
  3. `ambient_temperature`: Exterior climate temperature (°C)
  4. `power_kw`: Instantaneous compressor electrical power (kW)
  5. `compressor_state`: Binary operating status (0: Idle, 1: Active)
  6. `door_open`: Binary door status (0: Closed, 1: Open)
  7. `temperature_delta`: First-order thermal difference
  8. `rolling_mean`: 5-timestep rolling moving average
  9. `rolling_std`: 5-timestep rolling standard deviation (jitter)
  10. `temperature_slope`: Multi-step velocity trend
  11. `ambient_difference`: Thermal differential ($T_{\text{ambient}} - T$)
  12. `power_delta`: First-order power difference
- **Windowing:** Slices continuous streams into sliding input windows of shape `(60, 12)`.

### 2. Deep Learning Forecasting Layer (`ml/mad_tcn.py`, `ml/inference.py`)
- **Model:** Multi-scale Adaptive Dilated Temporal Convolutional Network.
- **Causality:** Strictly causal 1D dilated convolutions with dilations $d \in \{1, 2, 4, 8\}$ preventing lookahead bias.
- **Adaptive Weighting:** Combines multi-scale temporal convolutions to simultaneously track short-term spikes (door opening) and diurnal curves.
- **Input/Output:** Ingests tensor of shape `(1, 60, 12)` and outputs vector of length 15 representing the future temperature trajectory.

### 3. Future Risk Assessment Layer (`core.py:risk`)
- **Penalty Function:**
  $$V(p_i) = \max(p_i - T_{\max}, 0) + \max(T_{\min} - p_i, 0)$$
- **Composite Risk Score:**
  $$S_{\text{risk}} = \text{clip}\left(100 \cdot \left(\frac{\bar{V}}{T_{\max} - T_{\min} + \epsilon} + 0.08 \cdot \max(0, \overline{\Delta p})\right), 0, 100\right)$$
- **Classification:** Severity mapped to `LOW` (<15), `MEDIUM` (15–40), `HIGH` (40–70), or `CRITICAL` (≥70).
- **Breach Horizon:** First future timestep $t+k$ where predicted temperature leaves safe bounds.

### 4. Prediction-Guided Optimization Layer (`optimization/nsga2_optimizer.py`)
- **Framework:** `pymoo` implementation of NSGA-II.
- **Decision Variables:**
  - $x_0$: Cooling intensity $I \in [0.1, 1.0]$
  - $x_1$: Compressor duty cycle $D \in [0.2, 1.0]$
  - $x_2$: Target temperature offset $O \in [0.0, 1.0]$
- **Objectives:**
  - $f_1 = \max(0, S_{\text{risk}} - 18 \cdot \Delta T_{\text{cool}}) + \max(0, T_{\text{curr}} - \Delta T_{\text{cool}} - 5.0) \cdot 5$
  - $f_2 = (0.25 + 0.035 \cdot \max(T_{\text{amb}} - T_{\text{curr}}, 0)) \cdot (0.35 + 0.65 \cdot I) \cdot D$
- **Selection:** Picks the Pareto point minimizing normalized weighted cost $0.65 \cdot f_1^* + 0.35 \cdot f_2^*$.

### 5. Web Application Layer (`apps/monitoring/views.py`, Django 5.x)
- **Home Route (`/`):** Full-screen product storytelling landing page with 16 sections, SVG data flow particles, and real backend metrics.
- **Operations Dashboard (`/dashboard/`):** KPI cards, Canvas forecast graph with safe/warning/critical bands, animated risk meter, and Pareto front display.
- **Live IoT Simulation (`/live-monitoring/`):** Multi-sensor telemetry cards with START/PAUSE/RESET controls stepping through database records.
- **Forecast Dashboard (`/predictions/`):** Deep dive into 15-step MAD-TCN predictions.
- **Pareto Dashboard (`/optimization/`):** Visual explanation of NSGA-II multi-objective balance.
- **Alert Management (`/alerts/`):** Active alerts, cache-persisted resolution, and nominal status tracking.
- **Sensor Fleet (`/sensors/`):** Fleet overview table with click-to-view historical temperature graph.
- **Model Performance (`/model/`):** Architecture breakdown, parameter shapes, and receptive field visualization.
- **Upload Center (`/upload/`):** Drag-and-drop CSV validation, preview, and persistence.
- **Report Center (`/reports/`):** Multi-format export in JSON, Markdown, and CSV.
- **Methodology (`/methodology/`):** Complete research architecture, mathematical formulations, and comparative evaluation.
