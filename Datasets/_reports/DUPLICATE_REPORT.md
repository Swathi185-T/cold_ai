# COLDCHAIN-AI Duplicate Detection & Integrity Report

**Audit Date**: 2026-10-06 | **Hashing Standard**: SHA-256 (64-character hexadecimal digest)

## 1. File-Level Duplicate & Provenance Analysis

| Canonical Dataset | Clean Path | File Size | SHA-256 Digest | Archive / Reference Copy | Archive SHA-256 | Status |
|---|---|---|---|---|---|---|
| Temperature Readings: IoT Devices | `iot_temperature_readings.csv` | 6,948,127 B | `2bf965701db96cd5...` | `archive/IOT-temp.csv` | `2bf965701db96cd5...` | EXACT PROVENANCE MATCH |
| Energy Consumption Prediction | `energy_consumption_prediction.csv` | 132,713 B | `ff35741a8891ed88...` | `archive (1)/Energy_consumption.csv` | `ff35741a8891ed88...` | EXACT PROVENANCE MATCH |
| EVIoT Predictive Maintenance | `eviot_predictive_maintenance.csv` | 92,897,837 B | `fbd6ba9635a98c72...` | `archive (2)/EV_Predictive_Maintenance_Dataset_15min.csv` | `fbd6ba9635a98c72...` | EXACT PROVENANCE MATCH |
| Journey to Zero (Train) | `journey_to_zero_electricity_train.csv` | 736,984 B | `2e494fd40e6c6446...` | `predict-electricity-consumption/train.csv` | `2e494fd40e6c6446...` | EXACT PROVENANCE MATCH |
| Journey to Zero (Test) | `journey_to_zero_electricity_test.csv` | 13,958 B | `913554a3865e9186...` | `predict-electricity-consumption/test.csv` | `913554a3865e9186...` | EXACT PROVENANCE MATCH |
| Journey to Zero (Sub) | `journey_to_zero_electricity_sample_submission.csv` | 5,368 B | `a2b3c239add5ca6c...` | `predict-electricity-consumption/sample_submission.csv` | `a2b3c239add5ca6c...` | EXACT PROVENANCE MATCH |
| IoT Temp Forecasting Notebook | `iot_temperature_forecasting.ipynb` | 12,662,414 B | `b602cdce55200cf0...` | `_original_downloads/iot-temperature-forecasting.ipynb` | `b602cdce55200cf0...` | EXACT PROVENANCE MATCH |

### Cross-Dataset Archive Redundancy
- **archive.zip vs archive folder**: `archive.zip` contains `IOT-temp.csv` (100% byte identical to `archive/IOT-temp.csv`).
- **archive (1).zip vs archive (1) folder**: `archive (1).zip` contains `Energy_consumption.csv` (100% byte identical to `archive (1)/Energy_consumption.csv`).
- **archive (2).zip vs archive (2) folder**: `archive (2).zip` contains `EV_Predictive_Maintenance_Dataset_15min.csv` (100% byte identical to `archive (2)/EV_Predictive_Maintenance_Dataset_15min.csv`).
- **predict-electricity-consumption.zip vs predict-electricity-consumption folder**: Contains `train.csv`, `test.csv`, and `sample_submission.csv` (100% byte identical).
- **iot-temperature-forecasting.ipynb vs IOT-temp.csv**: The Jupyter notebook is an analytical workflow script; cell 10 explicitly specifies `df = pd.read_csv("/kaggle/input/temperature-readings-iot-devices/IOT-temp.csv")`. Hence, the notebook and `IOT-temp.csv` belong to the exact same underlying sensor dataset. They are not two separate data streams.

## 2. Row-Level Duplication Audit

| Dataset | Total Rows | Duplicate Rows | Duplicate % | Action Taken |
|---|---|---|---|---|
| `iot_temperature_readings.csv` | 97,606 | 1 | 0.0010% | Preserved in reference clean copy; deduplicated in `_processed` time-series pipeline |
| `energy_consumption_prediction.csv` | 1,000 | 0 | 0.0000% | Preserved intact |
| `eviot_predictive_maintenance.csv` | 175,393 | 0 | 0.0000% | Preserved intact |
| `journey_to_zero_electricity_train.csv` | 8,592 | 0 | 0.0000% | Preserved intact |
| `journey_to_zero_electricity_test.csv` | 168 | 0 | 0.0000% | Preserved intact |
| `simulated_cold_chain.csv` (Project baseline) | 12,000 | 0 | 0.0000% | Preserved intact |

### Preservation Policy Compliance
In strict accordance with rule #2 and #6, **no original files or duplicate copies have been deleted**. All reference files remain untouched in `D:\COLDCHAIN-AI\Datasets\_original_downloads`. Clean files in domain directories maintain 100% bit-for-bit fidelity with their original sources.