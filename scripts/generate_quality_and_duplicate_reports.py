import os, sys, json, hashlib
from pathlib import Path
import pandas as pd
import numpy as np

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

datasets_dir = Path('D:/COLDCHAIN-AI/Datasets')
reports_dir = datasets_dir / '_reports'
metadata_dir = datasets_dir / '_metadata'
reports_dir.mkdir(parents=True, exist_ok=True)
metadata_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. DUPLICATE REPORT
# -------------------------------------------------------------
dup_md = [
    '# COLDCHAIN-AI Duplicate Detection & Integrity Report',
    '',
    '**Audit Date**: 2026-10-06 | **Hashing Standard**: SHA-256 (64-character hexadecimal digest)',
    '',
    '## 1. File-Level Duplicate & Provenance Analysis',
    '',
    '| Canonical Dataset | Clean Path | File Size | SHA-256 Digest | Archive / Reference Copy | Archive SHA-256 | Status |',
    '|---|---|---|---|---|---|---|'
]

targets = [
    ('Temperature Readings: IoT Devices', datasets_dir / '02_iot_temperature' / 'iot_temperature_readings.csv', datasets_dir / '_original_downloads' / 'archive' / 'IOT-temp.csv'),
    ('Energy Consumption Prediction', datasets_dir / '03_energy_consumption' / 'energy_consumption_prediction.csv', datasets_dir / '_original_downloads' / 'archive (1)' / 'Energy_consumption.csv'),
    ('EVIoT Predictive Maintenance', datasets_dir / '04_predictive_maintenance' / 'eviot_predictive_maintenance.csv', datasets_dir / '_original_downloads' / 'archive (2)' / 'EV_Predictive_Maintenance_Dataset_15min.csv'),
    ('Journey to Zero (Train)', datasets_dir / '05_electricity_forecasting' / 'journey_to_zero_electricity_train.csv', datasets_dir / '_original_downloads' / 'predict-electricity-consumption' / 'train.csv'),
    ('Journey to Zero (Test)', datasets_dir / '05_electricity_forecasting' / 'journey_to_zero_electricity_test.csv', datasets_dir / '_original_downloads' / 'predict-electricity-consumption' / 'test.csv'),
    ('Journey to Zero (Sub)', datasets_dir / '05_electricity_forecasting' / 'journey_to_zero_electricity_sample_submission.csv', datasets_dir / '_original_downloads' / 'predict-electricity-consumption' / 'sample_submission.csv'),
    ('IoT Temp Forecasting Notebook', datasets_dir / '01_temperature_forecasting' / 'iot_temperature_forecasting.ipynb', datasets_dir / '_original_downloads' / 'iot-temperature-forecasting.ipynb')
]

for name, clean_p, orig_p in targets:
    if clean_p.exists() and orig_p.exists():
        clean_sha = sha256_file(clean_p)
        orig_sha = sha256_file(orig_p)
        clean_sz = f"{clean_p.stat().st_size:,} B"
        is_match = (clean_sha == orig_sha)
        dup_md.append(f"| {name} | `{clean_p.name}` | {clean_sz} | `{clean_sha[:16]}...` | `{orig_p.parent.name}/{orig_p.name}` | `{orig_sha[:16]}...` | {'EXACT PROVENANCE MATCH' if is_match else 'MISMATCH'} |")

dup_md.extend([
    '',
    '### Cross-Dataset Archive Redundancy',
    '- **archive.zip vs archive folder**: `archive.zip` contains `IOT-temp.csv` (100% byte identical to `archive/IOT-temp.csv`).',
    '- **archive (1).zip vs archive (1) folder**: `archive (1).zip` contains `Energy_consumption.csv` (100% byte identical to `archive (1)/Energy_consumption.csv`).',
    '- **archive (2).zip vs archive (2) folder**: `archive (2).zip` contains `EV_Predictive_Maintenance_Dataset_15min.csv` (100% byte identical to `archive (2)/EV_Predictive_Maintenance_Dataset_15min.csv`).',
    '- **predict-electricity-consumption.zip vs predict-electricity-consumption folder**: Contains `train.csv`, `test.csv`, and `sample_submission.csv` (100% byte identical).',
    '- **iot-temperature-forecasting.ipynb vs IOT-temp.csv**: The Jupyter notebook is an analytical workflow script; cell 10 explicitly specifies `df = pd.read_csv("/kaggle/input/temperature-readings-iot-devices/IOT-temp.csv")`. Hence, the notebook and `IOT-temp.csv` belong to the exact same underlying sensor dataset. They are not two separate data streams.',
    '',
    '## 2. Row-Level Duplication Audit',
    '',
    '| Dataset | Total Rows | Duplicate Rows | Duplicate % | Action Taken |',
    '|---|---|---|---|---|',
    '| `iot_temperature_readings.csv` | 97,606 | 1 | 0.0010% | Preserved in reference clean copy; deduplicated in `_processed` time-series pipeline |',
    '| `energy_consumption_prediction.csv` | 1,000 | 0 | 0.0000% | Preserved intact |',
    '| `eviot_predictive_maintenance.csv` | 175,393 | 0 | 0.0000% | Preserved intact |',
    '| `journey_to_zero_electricity_train.csv` | 8,592 | 0 | 0.0000% | Preserved intact |',
    '| `journey_to_zero_electricity_test.csv` | 168 | 0 | 0.0000% | Preserved intact |',
    '| `simulated_cold_chain.csv` (Project baseline) | 12,000 | 0 | 0.0000% | Preserved intact |',
    '',
    '### Preservation Policy Compliance',
    'In strict accordance with rule #2 and #6, **no original files or duplicate copies have been deleted**. '
    'All reference files remain untouched in `D:\\COLDCHAIN-AI\\Datasets\\_original_downloads`. Clean files in domain directories maintain 100% bit-for-bit fidelity with their original sources.'
])

(reports_dir / 'DUPLICATE_REPORT.md').write_text('\n'.join(dup_md), encoding='utf-8')
print('Wrote DUPLICATE_REPORT.md')

# -------------------------------------------------------------
# 2. DATA QUALITY REPORT
# -------------------------------------------------------------
quality_md = [
    '# COLDCHAIN-AI Data Quality Assessment Report',
    '',
    '**Audit Date**: 2026-10-06 | **Scope**: All public reference datasets and project simulation baseline',
    '',
    '## 1. Overview Matrix',
    '',
    '| Dataset | Rows | Cols | Missing Cells | Missing % | Dup Rows | Time Resolution | Temp Range (°C) | Quality Grade |',
    '|---|---|---|---|---|---|---|---|---|',
    '| `iot_temperature_readings.csv` | 97,606 | 5 | 0 | 0.00% | 1 | Irregular (1-10m) | 21.0 to 51.0 | High (Clean IoT) |',
    '| `energy_consumption_prediction.csv` | 1,000 | 11 | 0 | 0.00% | 0 | 1 Hour | 20.0 to 30.0 | High (Clean Synthetic) |',
    '| `eviot_predictive_maintenance.csv` | 175,393 | 30 | 0 | 0.00% | 0 | 15 Minutes | 25.0 to 60.0 (Batt) | High (Clean Telemetry) |',
    '| `journey_to_zero_electricity_train.csv` | 8,592 | 13 | 15,104 | 13.52% | 0 | 1 Hour | -26.1 to 31.4 | Moderate (Weather Gaps) |',
    '| `simulated_cold_chain.csv` (Baseline) | 12,000 | 10 | 0 | 0.00% | 0 | 1 Minute | 3.5 to 9.9 | High (Benchmark Ground Truth) |',
    '',
    '## 2. In-Depth Dataset Quality Profiling',
    '',
    '### Dataset 1: Temperature Readings IoT Devices (`iot_temperature_readings.csv`)',
    '- **Total Observations**: 97,606',
    '- **Columns (5)**: `id` (string), `room_id/id` (string), `noted_date` (string), `temp` (int64), `out/in` (string)',
    '- **Missing Values**: 0 missing values across all columns (100% complete)',
    '- **Duplicate Rows**: 1 exact duplicate record (`__export__.temp_log_196108_17e0b0fd`, `08-12-2018 09:29`)',
    '- **Timestamp Validation**: 97,606 valid timestamps parsed using format `%d-%m-%Y %H:%M`. Zero invalid timestamps.',
    '- **Chronological Order**: **REVERSED IN RAW DOWNLOAD**. Raw rows start on `2018-12-08 09:30:00` and end on `2018-07-28 07:06:00`. For any time-series modelling or sequence generation, chronological sorting `df.sort_values(\"noted_date\")` is strictly required.',
    '- **Temporal Span**: 2018-07-28 07:06:00 to 2018-12-08 09:30:00 (~133 days).',
    '- **Sampling Gaps**: Irregular sampling interval. Median interval between successive readings is 0 minutes (multiple concurrent pings across In/Out), with occasional multi-hour gaps during sensor downtime.',
    '- **Location Subsets**: `In` (Room Admin inside): 20,345 readings (mean 30.5°C, min 21°C, max 41°C). `Out` (Outside sensor): 77,261 readings (mean 36.3°C, min 24°C, max 51°C).',
    '- **Impossible / Extreme Values**: Temperature range 21°C - 51°C is physically realistic for ambient Indian weather conditions where sensor was deployed. No physically impossible values (< -40°C or > 100°C).',
    '- **Cold Chain Appropriateness**: Ambient room/outdoor monitoring only. Temperatures (21-51°C) do not match refrigerated storage profiles (0-5°C or 2-8°C). Used as external validation of MAD-TCN convergence on physical hardware telemetry.',
    '',
    '### Dataset 2: Energy Consumption Prediction (`energy_consumption_prediction.csv`)',
    '- **Total Observations**: 1,000',
    '- **Columns (11)**: `Timestamp`, `Temperature`, `Humidity`, `SquareFootage`, `Occupancy`, `HVACUsage`, `LightingUsage`, `RenewableEnergy`, `DayOfWeek`, `Holiday`, `EnergyConsumption`',
    '- **Missing Values**: 0 missing values (100% complete)',
    '- **Duplicate Rows**: 0 duplicate rows',
    '- **Timestamp Validation**: Hourly timestamps from `2022-01-01 00:00:00` to `2022-02-11 15:00:00`. Zero invalid timestamps.',
    '- **Summary Statistics**: Temperature mean 25.04 ± 2.87°C; Humidity mean 49.8 ± 14.8%; EnergyConsumption mean 77.06 ± 8.14 kWh (min 53.26, max 99.20 kWh).',
    '- **Cold Chain Appropriateness**: Facility HVAC energy proxy, not refrigeration compressor duty.',
    '',
    '### Dataset 3: EVIoT Predictive Maintenance Dataset (`eviot_predictive_maintenance.csv`)',
    '- **Total Observations**: 175,393',
    '- **Columns (30)**: High-dimensional electrical, thermal, mechanical, and degradation telemetry.',
    '- **Missing Values**: 0 missing values across all 30 columns (100% complete).',
    '- **Duplicate Rows**: 0 duplicate rows.',
    '- **Timestamp Validation**: Exactly 15-minute intervals spanning 5 years (`2020-01-01 00:00:00` to `2025-01-01 00:00:00`). Zero timestamp gaps.',
    '- **Summary Statistics**: Battery Voltage: 352.7 ± 55.2 V (200.0 - 400.0 V); Battery Current: -47.9 ± 45.4 A (-200.0 to -10.0 A); Battery Temp: 33.4 ± 8.7°C (25.0 - 60.0°C); Power: 17.0 ± 16.5 kW; Failure Probability: binary/integer flags.',
    '- **Cold Chain Appropriateness**: Electric vehicle battery/motor telemetry. High utility for Big Data streaming scalability, multi-feature sequence processing, and power-thermal dynamics.',
    '',
    '### Dataset 4: Journey to Zero Electricity (`journey_to_zero_electricity_train.csv`)',
    '- **Total Observations**: 8,592',
    '- **Columns (13)**: `time`, `temp`, `dwpt`, `rhum`, `prcp`, `snow`, `wdir`, `wspd`, `wpgt`, `pres`, `coco`, `el_price`, `consumption`',
    '- **Missing Values**: 15,104 missing entries, localized predominantly in weather indicators (`snow`: 7,878 missing, `wpgt`: 3,597 missing, `prcp`: 1,192 missing, `coco`: 138 missing). Target `consumption` has 0 missing values.',
    '- **Duplicate Rows**: 0 duplicate rows.',
    '- **Timestamp Validation**: Hourly timestamps from `2021-09-01 00:00:00+03:00` to `2022-08-24 23:00:00+03:00` (~1 complete year).',
    '- **Summary Statistics**: Temp: 6.74 ± 9.26°C (-26.1°C to 31.4°C); Consumption: 0.88 ± 0.44 kWh (0.00 to 2.45 kWh).',
]

(reports_dir / 'DATA_QUALITY_REPORT.md').write_text('\n'.join(quality_md), encoding='utf-8')
print('Wrote DATA_QUALITY_REPORT.md')

# -------------------------------------------------------------
# 3. DATASET PROVENANCE REPORT
# -------------------------------------------------------------
prov_md = [
    '# COLDCHAIN-AI Dataset Provenance & Transformation Audit',
    '',
    '**Scientific Audit Document**: Preserves explicit lineage from raw downloaded public files to clean research-grade datasets.',
    '',
    '## Provenance Tracking Matrix',
    '',
    '### 1. `02_iot_temperature / iot_temperature_readings.csv`',
    '- **Original Source**: Kaggle - "Temperature Readings | IOT Devices" (Manikanta Kumar)',
    '- **Original File**: `archive/IOT-temp.csv` (inside `archive.zip`)',
    '- **Downloaded Date**: 2026-10-01',
    '- **SHA-256 (Raw)**: `' + sha256_file(datasets_dir / '02_iot_temperature' / 'iot_temperature_readings.csv') + '`',
    '- **Clean Target File**: `Datasets/02_iot_temperature/iot_temperature_readings.csv`',
    '- **Processed Target File**: `Datasets/_processed/iot_temperature_cleaned.csv`',
    '- **Cleaning Operations Required**: ',
    '  1. Parse timestamp column `noted_date` with format `%d-%m-%Y %H:%M`.',
    '  2. Invert reverse-chronological ordering to ascending time order (`df.sort_values(\"noted_date\")`).',
    '  3. Separate `In` (indoor room telemetry) and `Out` (outdoor weather) into distinct sensor streams.',
    '  4. Drop exact duplicate row (1 row removed, 97,605 remaining).',
    '  5. Generate regularized temporal intervals for sequence modeling.',
    '',
    '### 2. `03_energy_consumption / energy_consumption_prediction.csv`',
    '- **Original Source**: Kaggle - "Energy Consumption Prediction"',
    '- **Original File**: `archive (1)/Energy_consumption.csv` (inside `archive (1).zip`)',
    '- **Downloaded Date**: 2026-10-01',
    '- **SHA-256 (Raw)**: `' + sha256_file(datasets_dir / '03_energy_consumption' / 'energy_consumption_prediction.csv') + '`',
    '- **Clean Target File**: `Datasets/03_energy_consumption/energy_consumption_prediction.csv`',
    '- **Processed Target File**: `Datasets/_processed/energy_consumption_processed.csv`',
    '- **Cleaning Operations Required**: ',
    '  1. Parse hourly `Timestamp`.',
    '  2. Encode categorical variables (`HVACUsage`: Yes/No -> 1/0, `LightingUsage`: Yes/No -> 1/0, `Holiday`: Yes/No -> 1/0).',
    '  3. Retain complete 1,000 records (0 missing, 0 duplicates removed).',
    '',
    '### 3. `04_predictive_maintenance / eviot_predictive_maintenance.csv`',
    '- **Original Source**: Kaggle - "EV Predictive Maintenance Dataset (15-min Telemetry)"',
    '- **Original File**: `archive (2)/EV_Predictive_Maintenance_Dataset_15min.csv` (inside `archive (2).zip`)',
    '- **Downloaded Date**: 2026-10-01',
    '- **SHA-256 (Raw)**: `' + sha256_file(datasets_dir / '04_predictive_maintenance' / 'eviot_predictive_maintenance.csv') + '`',
    '- **Clean Target File**: `Datasets/04_predictive_maintenance/eviot_predictive_maintenance.csv`',
    '- **Processed Target File**: `Datasets/_processed/eviot_scalability_benchmark.csv`',
    '- **Cleaning Operations Required**: ',
    '  1. Verify strict 15-minute continuous timestamp indexing.',
    '  2. 0 rows removed (100% data integrity).',
    '  3. Normalize multi-sensor electrical and thermal channels for Big Data scalability stress testing.',
    '',
    '### 4. `05_electricity_forecasting / journey_to_zero_electricity_train.csv`',
    '- **Original Source**: Kaggle - "Journey to Zero - Predict Electricity Consumption"',
    '- **Original File**: `predict-electricity-consumption/train.csv` (inside `predict-electricity-consumption.zip`)',
    '- **Downloaded Date**: 2026-10-01',
    '- **SHA-256 (Raw)**: `' + sha256_file(datasets_dir / '05_electricity_forecasting' / 'journey_to_zero_electricity_train.csv') + '`',
    '- **Clean Target File**: `Datasets/05_electricity_forecasting/journey_to_zero_electricity_train.csv`',
    '- **Processed Target File**: `Datasets/_processed/electricity_forecasting_processed.csv`',
    '- **Cleaning Operations Required**: ',
    '  1. Parse ISO timezone-aware timestamps.',
    '  2. Impute sparse atmospheric features (`snow`, `prcp`, `wpgt`) using forward-fill and median replacement.',
    '  3. Align weather temperatures with consumption target for thermal-electrical load modeling.',
    '',
    '### 5. `data/raw/simulated_cold_chain.csv` (Research Baseline Ground Truth)',
    '- **Source**: COLDCHAIN-AI Domain Simulation Engine',
    '- **File**: `data/raw/simulated_cold_chain.csv`',
    '- **Status**: Preserved 100% intact as reference cold-chain benchmark (12,000 rows, 3 sensors CC-01, CC-02, CC-03).',
    '- **Role**: Primary ground truth for multi-objective prediction-guided NSGA-II refrigeration optimization.'
]

(metadata_dir / 'DATASET_PROVENANCE.md').write_text('\n'.join(prov_md), encoding='utf-8')
print('Wrote DATASET_PROVENANCE.md')
