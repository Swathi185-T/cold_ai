# COLDCHAIN-AI Dataset Inventory Audit Report

**Audit Timestamp**: 2026-10-06 | **Workspace Root**: `D:\COLDCHAIN-AI\Datasets`

## Executive Summary

This report catalogs all data files, notebooks, and compressed archives present in the COLDCHAIN-AI dataset directory. All original downloads are preserved strictly unmodified in `_original_downloads`, and clean organized copies reside in numbered domain directories.

### File Catalog Table

| Relative Path | Filename | Size (KB) | Rows | Cols | Identity | Source | Likely Purpose |
|---|---|---|---|---|---|---|---|
| `01_temperature_forecasting/iot_temperature_forecasting.ipynb` | `iot_temperature_forecasting.ipynb` | 12365.64 | 112 | 0 | IoT Temperature Forecasting | Kaggle Notebook (iot-temperature-forecasting) | Exploratory data analysis & reference forecasting models |
| `01_temperature_forecasting/metadata.json` | `metadata.json` | 1.36 | N/A | N/A | Dataset Metadata | COLDCHAIN-AI Pipeline | Dataset schema & provenance metadata |
| `02_iot_temperature/iot_temperature_readings.csv` | `iot_temperature_readings.csv` | 6785.28 | 97606 | 5 | Temperature Readings: IoT Devices | Kaggle (temperature-readings-iot-devices) | IoT sensor temperature telemetry benchmarking |
| `02_iot_temperature/metadata.json` | `metadata.json` | 1.33 | N/A | N/A | Dataset Metadata | COLDCHAIN-AI Pipeline | Dataset schema & provenance metadata |
| `03_energy_consumption/energy_consumption_prediction.csv` | `energy_consumption_prediction.csv` | 129.6 | 1000 | 11 | Energy Consumption Prediction | Kaggle (energy-consumption-prediction) | Building HVAC and thermal load energy modeling |
| `03_energy_consumption/metadata.json` | `metadata.json` | 1.3 | N/A | N/A | Dataset Metadata | COLDCHAIN-AI Pipeline | Dataset schema & provenance metadata |
| `04_predictive_maintenance/eviot_predictive_maintenance.csv` | `eviot_predictive_maintenance.csv` | 90720.54 | 175393 | 30 | EVIoT Predictive Maintenance Dataset | Kaggle (ev-predictive-maintenance-dataset-15min) | High-frequency telemetry & Big Data scalability benchmarking |
| `04_predictive_maintenance/metadata.json` | `metadata.json` | 1.64 | N/A | N/A | Dataset Metadata | COLDCHAIN-AI Pipeline | Dataset schema & provenance metadata |
| `05_electricity_forecasting/journey_to_zero_electricity_sample_submission.csv` | `journey_to_zero_electricity_sample_submission.csv` | 5.24 | 168 | 2 | Journey to Zero - Sample Submission | Kaggle (predict-electricity-consumption) | Competition submission template |
| `05_electricity_forecasting/journey_to_zero_electricity_test.csv` | `journey_to_zero_electricity_test.csv` | 13.63 | 168 | 12 | Journey to Zero - Electricity Consumption (Test) | Kaggle (predict-electricity-consumption) | Out-of-sample test split for electricity demand |
| `05_electricity_forecasting/journey_to_zero_electricity_train.csv` | `journey_to_zero_electricity_train.csv` | 719.71 | 8592 | 13 | Journey to Zero - Electricity Consumption (Train) | Kaggle (predict-electricity-consumption) | Weather-dependent electricity demand forecasting |
| `05_electricity_forecasting/metadata.json` | `metadata.json` | 1.28 | N/A | N/A | Dataset Metadata | COLDCHAIN-AI Pipeline | Dataset schema & provenance metadata |
| `06_cold_chain/README.md` | `README.md` | 0.4 | N/A | N/A | Documentation / Report | COLDCHAIN-AI Pipeline | Dataset documentation & audit report |
| `_original_downloads/archive/IOT-temp.csv` | `IOT-temp.csv` | 6785.28 | 97606 | 5 | Temperature Readings: IoT Devices | Kaggle (temperature-readings-iot-devices) | IoT sensor temperature telemetry benchmarking |
| `_original_downloads/archive (1)/Energy_consumption.csv` | `Energy_consumption.csv` | 129.6 | 1000 | 11 | Energy Consumption Prediction | Kaggle (energy-consumption-prediction) | Building HVAC and thermal load energy modeling |
| `_original_downloads/archive (2)/EV_Predictive_Maintenance_Dataset_15min.csv` | `EV_Predictive_Maintenance_Dataset_15min.csv` | 90720.54 | 175393 | 30 | EVIoT Predictive Maintenance Dataset | Kaggle (ev-predictive-maintenance-dataset-15min) | High-frequency telemetry & Big Data scalability benchmarking |
| `_original_downloads/iot-temperature-forecasting.ipynb` | `iot-temperature-forecasting.ipynb` | 12365.64 | 112 | 0 | IoT Temperature Forecasting | Kaggle Notebook (iot-temperature-forecasting) | Exploratory data analysis & reference forecasting models |
| `_original_downloads/predict-electricity-consumption/sample_submission.csv` | `sample_submission.csv` | 5.24 | 168 | 2 | Journey to Zero - Sample Submission | Kaggle (predict-electricity-consumption) | Competition submission template |
| `_original_downloads/predict-electricity-consumption/test.csv` | `test.csv` | 13.63 | 168 | 12 | Journey to Zero - Electricity Consumption (Test) | Kaggle (predict-electricity-consumption) | Out-of-sample test split for electricity demand |
| `_original_downloads/predict-electricity-consumption/train.csv` | `train.csv` | 719.71 | 8592 | 13 | Journey to Zero - Electricity Consumption (Train) | Kaggle (predict-electricity-consumption) | Weather-dependent electricity demand forecasting |
| `_original_downloads/source_zips/archive (1).zip` | `archive (1).zip` | 53.57 | 1 | N/A | Raw Download Archive | Kaggle | Compressed download provenance preservation |
| `_original_downloads/source_zips/archive (2).zip` | `archive (2).zip` | 43184.13 | 1 | N/A | Raw Download Archive | Kaggle | Compressed download provenance preservation |
| `_original_downloads/source_zips/archive.zip` | `archive.zip` | 1044.93 | 1 | N/A | Raw Download Archive | Kaggle | Compressed download provenance preservation |
| `_original_downloads/source_zips/predict-electricity-consumption.zip` | `predict-electricity-consumption.zip` | 173.88 | 3 | N/A | Raw Download Archive | Kaggle | Compressed download provenance preservation |
| `archive/IOT-temp.csv` | `IOT-temp.csv` | 6785.28 | 97606 | 5 | Temperature Readings: IoT Devices | Kaggle (temperature-readings-iot-devices) | IoT sensor temperature telemetry benchmarking |
| `archive (1)/Energy_consumption.csv` | `Energy_consumption.csv` | 129.6 | 1000 | 11 | Energy Consumption Prediction | Kaggle (energy-consumption-prediction) | Building HVAC and thermal load energy modeling |
| `archive (2)/EV_Predictive_Maintenance_Dataset_15min.csv` | `EV_Predictive_Maintenance_Dataset_15min.csv` | 90720.54 | 175393 | 30 | EVIoT Predictive Maintenance Dataset | Kaggle (ev-predictive-maintenance-dataset-15min) | High-frequency telemetry & Big Data scalability benchmarking |
| `iot-temperature-forecasting.ipynb` | `iot-temperature-forecasting.ipynb` | 12365.64 | 112 | 0 | IoT Temperature Forecasting | Kaggle Notebook (iot-temperature-forecasting) | Exploratory data analysis & reference forecasting models |
| `predict-electricity-consumption/sample_submission.csv` | `sample_submission.csv` | 5.24 | 168 | 2 | Journey to Zero - Sample Submission | Kaggle (predict-electricity-consumption) | Competition submission template |
| `predict-electricity-consumption/test.csv` | `test.csv` | 13.63 | 168 | 12 | Journey to Zero - Electricity Consumption (Test) | Kaggle (predict-electricity-consumption) | Out-of-sample test split for electricity demand |
| `predict-electricity-consumption/train.csv` | `train.csv` | 719.71 | 8592 | 13 | Journey to Zero - Electricity Consumption (Train) | Kaggle (predict-electricity-consumption) | Weather-dependent electricity demand forecasting |

## Identified Target Datasets vs Downloaded Files

The user specified an intention to download 5 datasets. Detailed inspection reveals the exact distribution below:

### 1. IoT Temperature Forecasting
- **Status**: PRESENT AS JUPYTER NOTEBOOK (Not an independent CSV file)
- **Original Source**: Kaggle (`iot-temperature-forecasting.ipynb`)
- **Original Folder**: `Datasets/` & `_original_downloads/`
- **Actual Data Files**: `01_temperature_forecasting/iot_temperature_forecasting.ipynb`
- **Rows**: 112 cells
- **Columns**: NOT PRESENT (Notebook format)
- **Important Columns**: References underlying `IOT-temp.csv` columns (`noted_date`, `temp`, `out/in`)
- **Time column**: NOT PRESENT in notebook directly (uses `noted_date` in referenced dataset)
- **Temperature**: NOT PRESENT in notebook directly (uses `temp` in referenced dataset)
- **Humidity**: NOT PRESENT
- **Energy**: NOT PRESENT
- **Power**: NOT PRESENT
- **Voltage**: NOT PRESENT
- **Current**: NOT PRESENT
- **Sensor/device ID**: NOT PRESENT
- **Location**: NOT PRESENT
- **Failure/anomaly**: NOT PRESENT
- **Other relevant fields**: Contains exploratory data analysis, HoloViews visual charts, and forecasting models trained on `IOT-temp.csv`.

### 2. Temperature Readings: IoT Devices
- **Status**: PRESENT
- **Original Source**: Kaggle (`temperature-readings-iot-devices` by Manikanta Kumar)
- **Original Folder**: `Datasets/archive/` (from `archive.zip`)
- **Actual Data Files**: `02_iot_temperature/iot_temperature_readings.csv`
- **Rows**: 97,606
- **Columns**: 5
- **Important Columns**: `noted_date`, `temp`, `out/in`
- **Time column**: `noted_date` (DD-MM-YYYY HH:MM format)
- **Temperature**: `temp` (Integer °C, range 21 to 51 °C)
- **Humidity**: NOT PRESENT
- **Energy**: NOT PRESENT
- **Power**: NOT PRESENT
- **Voltage**: NOT PRESENT
- **Current**: NOT PRESENT
- **Sensor/device ID**: `room_id/id` (constant `Room Admin`), row ID `id`
- **Location**: `out/in` (`In`: 20,345 records, `Out`: 77,261 records)
- **Failure/anomaly**: NOT PRESENT
- **Other relevant fields**: `id` (__export__.temp_log_...)

### 3. Energy Consumption Prediction
- **Status**: PRESENT
- **Original Source**: Kaggle (`energy-consumption-prediction`)
- **Original Folder**: `Datasets/archive (1)/` (from `archive (1).zip`)
- **Actual Data Files**: `03_energy_consumption/energy_consumption_prediction.csv`
- **Rows**: 1,000
- **Columns**: 11
- **Important Columns**: `Timestamp`, `Temperature`, `Humidity`, `SquareFootage`, `Occupancy`, `HVACUsage`, `LightingUsage`, `RenewableEnergy`, `EnergyConsumption`
- **Time column**: `Timestamp` (YYYY-MM-DD HH:MM:SS format, hourly)
- **Temperature**: `Temperature` (Ambient building temperature °C)
- **Humidity**: `Humidity` (%)
- **Energy**: `EnergyConsumption` (Total kWh), `RenewableEnergy` (kWh)
- **Power**: NOT PRESENT (Energy per hour in kWh)
- **Voltage**: NOT PRESENT
- **Current**: NOT PRESENT
- **Sensor/device ID**: NOT PRESENT
- **Location**: NOT PRESENT (`SquareFootage` characterizes the facility)
- **Failure/anomaly**: NOT PRESENT
- **Other relevant fields**: `Occupancy`, `HVACUsage` (On/Off), `LightingUsage` (On/Off), `DayOfWeek`, `Holiday` (Yes/No)

### 4. EVIoT Predictive Maintenance Dataset
- **Status**: PRESENT
- **Original Source**: Kaggle (`ev-predictive-maintenance-dataset-15min`)
- **Original Folder**: `Datasets/archive (2)/` (from `archive (2).zip`)
- **Actual Data Files**: `04_predictive_maintenance/eviot_predictive_maintenance.csv`
- **Rows**: 175,393
- **Columns**: 30
- **Important Columns**: `Timestamp`, `Battery_Voltage`, `Battery_Current`, `Battery_Temperature`, `Motor_Temperature`, `Power_Consumption`, `Ambient_Temperature`, `Ambient_Humidity`, `Failure_Probability`, `Maintenance_Type`
- **Time column**: `Timestamp` (15-minute interval, 2020-01-01 to 2025-01-01)
- **Temperature**: `Battery_Temperature`, `Motor_Temperature`, `Tire_Temperature`, `Ambient_Temperature`
- **Humidity**: `Ambient_Humidity`
- **Energy**: NOT PRESENT
- **Power**: `Power_Consumption` (kW)
- **Voltage**: `Battery_Voltage` (V)
- **Current**: `Battery_Current` (A)
- **Sensor/device ID**: NOT PRESENT (Continuous vehicle powertrain telemetry)
- **Location**: NOT PRESENT (`Route_Roughness`, `Distance_Traveled` describe terrain)
- **Failure/anomaly**: `Failure_Probability`, `Maintenance_Type`, `RUL`, `TTF`, `Component_Health_Score`
- **Other relevant fields**: `SoC`, `SoH`, `Charge_Cycles`, `Motor_Vibration`, `Motor_Torque`, `Motor_RPM`, `Brake_Pad_Wear`, `Brake_Pressure`, `Reg_Brake_Efficiency`, `Tire_Pressure`, `Suspension_Load`, `Load_Weight`, `Driving_Speed`, `Idle_Time`

### 5. Journey to Zero / Predict Electricity Consumption
- **Status**: PRESENT
- **Original Source**: Kaggle (`predict-electricity-consumption`)
- **Original Folder**: `Datasets/predict-electricity-consumption/` (from `predict-electricity-consumption.zip`)
- **Actual Data Files**: `05_electricity_forecasting/journey_to_zero_electricity_train.csv` (8,592 rows), `..._test.csv` (168 rows), `..._sample_submission.csv` (168 rows)
- **Rows**: 8,592 (train), 168 (test)
- **Columns**: 13 (train), 12 (test)
- **Important Columns**: `time`, `temp`, `dwpt`, `rhum`, `el_price`, `consumption`
- **Time column**: `time` (Hourly ISO timestamp with offset)
- **Temperature**: `temp` (Ambient outdoor temperature °C), `dwpt` (Dew point temperature °C)
- **Humidity**: `rhum` (Relative humidity %)
- **Energy**: `consumption` (Hourly electricity consumption)
- **Power**: NOT PRESENT
- **Voltage**: NOT PRESENT
- **Current**: NOT PRESENT
- **Sensor/device ID**: NOT PRESENT
- **Location**: NOT PRESENT
- **Failure/anomaly**: NOT PRESENT
- **Other relevant fields**: `prcp` (precipitation), `snow`, `wdir` (wind direction), `wspd` (wind speed), `wpgt` (gust), `pres` (air pressure), `coco` (weather condition code), `el_price` (electricity spot price)

### Genuine Cold-Chain Logistics Data
- **Status**: NOT PRESENT IN PUBLIC DOWNLOADS
- **Cold Chain Baseline**: The only cold chain refrigerated transport dataset in the project is `D:/COLDCHAIN-AI/data/raw/simulated_cold_chain.csv` (12,000 rows across 3 cold chain sensors CC-01, CC-02, CC-03).
- **Scientific Disclosure**: Public datasets represent ambient room IoT, building HVAC, EV powertrains, and regional electricity grids. They provide external algorithmic stress-testing and transfer-learning validation, but are NOT cold-chain logistics telemetry.