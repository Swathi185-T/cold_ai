# COLDCHAIN-AI Dataset Provenance & Transformation Audit

**Scientific Audit Document**: Preserves explicit lineage from raw downloaded public files to clean research-grade datasets.

## Provenance Tracking Matrix

### 1. `02_iot_temperature / iot_temperature_readings.csv`
- **Original Source**: Kaggle - "Temperature Readings | IOT Devices" (Manikanta Kumar)
- **Original File**: `archive/IOT-temp.csv` (inside `archive.zip`)
- **Downloaded Date**: 2026-10-01
- **SHA-256 (Raw)**: `2bf965701db96cd5788403d395a25d2dd7282bea24e317b7f7b157b7a02063d4`
- **Clean Target File**: `Datasets/02_iot_temperature/iot_temperature_readings.csv`
- **Processed Target File**: `Datasets/_processed/iot_temperature_cleaned.csv`
- **Cleaning Operations Required**: 
  1. Parse timestamp column `noted_date` with format `%d-%m-%Y %H:%M`.
  2. Invert reverse-chronological ordering to ascending time order (`df.sort_values("noted_date")`).
  3. Separate `In` (indoor room telemetry) and `Out` (outdoor weather) into distinct sensor streams.
  4. Drop exact duplicate row (1 row removed, 97,605 remaining).
  5. Generate regularized temporal intervals for sequence modeling.

### 2. `03_energy_consumption / energy_consumption_prediction.csv`
- **Original Source**: Kaggle - "Energy Consumption Prediction"
- **Original File**: `archive (1)/Energy_consumption.csv` (inside `archive (1).zip`)
- **Downloaded Date**: 2026-10-01
- **SHA-256 (Raw)**: `ff35741a8891ed888608a2b551ffd0330e8b25b5126bbc6178f5a8c6e8329654`
- **Clean Target File**: `Datasets/03_energy_consumption/energy_consumption_prediction.csv`
- **Processed Target File**: `Datasets/_processed/energy_consumption_processed.csv`
- **Cleaning Operations Required**: 
  1. Parse hourly `Timestamp`.
  2. Encode categorical variables (`HVACUsage`: Yes/No -> 1/0, `LightingUsage`: Yes/No -> 1/0, `Holiday`: Yes/No -> 1/0).
  3. Retain complete 1,000 records (0 missing, 0 duplicates removed).

### 3. `04_predictive_maintenance / eviot_predictive_maintenance.csv`
- **Original Source**: Kaggle - "EV Predictive Maintenance Dataset (15-min Telemetry)"
- **Original File**: `archive (2)/EV_Predictive_Maintenance_Dataset_15min.csv` (inside `archive (2).zip`)
- **Downloaded Date**: 2026-10-01
- **SHA-256 (Raw)**: `fbd6ba9635a98c72eba37970033bf2528760d7548eacd5eaefc73c6d24341daf`
- **Clean Target File**: `Datasets/04_predictive_maintenance/eviot_predictive_maintenance.csv`
- **Processed Target File**: `Datasets/_processed/eviot_scalability_benchmark.csv`
- **Cleaning Operations Required**: 
  1. Verify strict 15-minute continuous timestamp indexing.
  2. 0 rows removed (100% data integrity).
  3. Normalize multi-sensor electrical and thermal channels for Big Data scalability stress testing.

### 4. `05_electricity_forecasting / journey_to_zero_electricity_train.csv`
- **Original Source**: Kaggle - "Journey to Zero - Predict Electricity Consumption"
- **Original File**: `predict-electricity-consumption/train.csv` (inside `predict-electricity-consumption.zip`)
- **Downloaded Date**: 2026-10-01
- **SHA-256 (Raw)**: `2e494fd40e6c6446de26d24387e0c24018f38120e558074e5cb56d840fe19deb`
- **Clean Target File**: `Datasets/05_electricity_forecasting/journey_to_zero_electricity_train.csv`
- **Processed Target File**: `Datasets/_processed/electricity_forecasting_processed.csv`
- **Cleaning Operations Required**: 
  1. Parse ISO timezone-aware timestamps.
  2. Impute sparse atmospheric features (`snow`, `prcp`, `wpgt`) using forward-fill and median replacement.
  3. Align weather temperatures with consumption target for thermal-electrical load modeling.

### 5. `data/raw/simulated_cold_chain.csv` (Research Baseline Ground Truth)
- **Source**: COLDCHAIN-AI Domain Simulation Engine
- **File**: `data/raw/simulated_cold_chain.csv`
- **Status**: Preserved 100% intact as reference cold-chain benchmark (12,000 rows, 3 sensors CC-01, CC-02, CC-03).
- **Role**: Primary ground truth for multi-objective prediction-guided NSGA-II refrigeration optimization.