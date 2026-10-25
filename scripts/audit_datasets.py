import os, sys, json, hashlib, zipfile
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

# 1. Full file scan
inventory_records = []
all_files = []
for root, dirs, files in os.walk(datasets_dir):
    for f in files:
        full_p = Path(root) / f
        all_files.append(full_p)

for p in sorted(all_files):
    rel_p = str(p.relative_to(datasets_dir)).replace('\\', '/')
    size = p.stat().st_size
    ext = p.suffix.lower()
    sha = sha256_file(p)
    
    rows = 'N/A'
    cols = 'N/A'
    col_names = 'N/A'
    identity = 'Unknown'
    source = 'Public / Local'
    archive_src = 'N/A'
    purpose = 'General'
    
    if 'IOT-temp.csv' in p.name or 'iot_temperature_readings.csv' in p.name:
        identity = 'Temperature Readings: IoT Devices'
        source = 'Kaggle (temperature-readings-iot-devices)'
        archive_src = 'archive.zip'
        purpose = 'IoT sensor temperature telemetry benchmarking'
        try:
            df = pd.read_csv(p, nrows=2)
            cols = len(df.columns)
            col_names = '; '.join(df.columns)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                rows = sum(1 for _ in fp) - 1
        except Exception: pass
    elif 'Energy_consumption.csv' in p.name or 'energy_consumption_prediction.csv' in p.name:
        identity = 'Energy Consumption Prediction'
        source = 'Kaggle (energy-consumption-prediction)'
        archive_src = 'archive (1).zip'
        purpose = 'Building HVAC and thermal load energy modeling'
        try:
            df = pd.read_csv(p, nrows=2)
            cols = len(df.columns)
            col_names = '; '.join(df.columns)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                rows = sum(1 for _ in fp) - 1
        except Exception: pass
    elif 'EV_Predictive_Maintenance_Dataset_15min.csv' in p.name or 'eviot_predictive_maintenance.csv' in p.name:
        identity = 'EVIoT Predictive Maintenance Dataset'
        source = 'Kaggle (ev-predictive-maintenance-dataset-15min)'
        archive_src = 'archive (2).zip'
        purpose = 'High-frequency telemetry & Big Data scalability benchmarking'
        try:
            df = pd.read_csv(p, nrows=2)
            cols = len(df.columns)
            col_names = '; '.join(df.columns)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                rows = sum(1 for _ in fp) - 1
        except Exception: pass
    elif 'train.csv' in p.name or 'journey_to_zero_electricity_train.csv' in p.name:
        identity = 'Journey to Zero - Electricity Consumption (Train)'
        source = 'Kaggle (predict-electricity-consumption)'
        archive_src = 'predict-electricity-consumption.zip'
        purpose = 'Weather-dependent electricity demand forecasting'
        try:
            df = pd.read_csv(p, nrows=2)
            cols = len(df.columns)
            col_names = '; '.join(df.columns)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                rows = sum(1 for _ in fp) - 1
        except Exception: pass
    elif 'test.csv' in p.name or 'journey_to_zero_electricity_test.csv' in p.name:
        identity = 'Journey to Zero - Electricity Consumption (Test)'
        source = 'Kaggle (predict-electricity-consumption)'
        archive_src = 'predict-electricity-consumption.zip'
        purpose = 'Out-of-sample test split for electricity demand'
        try:
            df = pd.read_csv(p, nrows=2)
            cols = len(df.columns)
            col_names = '; '.join(df.columns)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                rows = sum(1 for _ in fp) - 1
        except Exception: pass
    elif 'sample_submission.csv' in p.name or 'journey_to_zero_electricity_sample_submission.csv' in p.name:
        identity = 'Journey to Zero - Sample Submission'
        source = 'Kaggle (predict-electricity-consumption)'
        archive_src = 'predict-electricity-consumption.zip'
        purpose = 'Competition submission template'
        try:
            df = pd.read_csv(p, nrows=2)
            cols = len(df.columns)
            col_names = '; '.join(df.columns)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                rows = sum(1 for _ in fp) - 1
        except Exception: pass
    elif ext == '.ipynb':
        identity = 'IoT Temperature Forecasting'
        source = 'Kaggle Notebook (iot-temperature-forecasting)'
        archive_src = 'Direct download'
        purpose = 'Exploratory data analysis & reference forecasting models'
        try:
            with open(p, 'r', encoding='utf-8') as fp:
                nb = json.load(fp)
                rows = len(nb.get('cells', []))
                cols = 0
                col_names = 'Jupyter Notebook cells'
        except Exception: pass
    elif ext == '.zip':
        identity = 'Raw Download Archive'
        source = 'Kaggle'
        archive_src = p.name
        purpose = 'Compressed download provenance preservation'
        try:
            with zipfile.ZipFile(p, 'r') as zf:
                col_names = '; '.join(zf.namelist())
                rows = len(zf.namelist())
        except Exception: pass
    elif ext == '.json':
        identity = 'Dataset Metadata'
        source = 'COLDCHAIN-AI Pipeline'
        archive_src = 'N/A'
        purpose = 'Dataset schema & provenance metadata'
    elif ext == '.md':
        identity = 'Documentation / Report'
        source = 'COLDCHAIN-AI Pipeline'
        archive_src = 'N/A'
        purpose = 'Dataset documentation & audit report'

    inventory_records.append({
        'original_path': rel_p,
        'filename': p.name,
        'extension': ext,
        'size_bytes': size,
        'row_count': rows,
        'col_count': cols,
        'columns': col_names,
        'dataset_identity': identity,
        'source': source,
        'archive_source': archive_src,
        'likely_purpose': purpose,
        'sha256': sha
    })

# Save inventory CSV
inv_df = pd.DataFrame(inventory_records)
inv_csv_path = reports_dir / 'DATASET_INVENTORY.csv'
inv_df.to_csv(inv_csv_path, index=False)
print('Wrote DATASET_INVENTORY.csv')

# Build DATASET_INVENTORY.md
md_lines = [
    '# COLDCHAIN-AI Dataset Inventory Audit Report',
    '',
    '**Audit Timestamp**: 2026-10-06 | **Workspace Root**: `D:\\COLDCHAIN-AI\\Datasets`',
    '',
    '## Executive Summary',
    '',
    'This report catalogs all data files, notebooks, and compressed archives present in the COLDCHAIN-AI dataset directory. '
    'All original downloads are preserved strictly unmodified in `_original_downloads`, and clean organized copies reside in numbered domain directories.',
    '',
    '### File Catalog Table',
    '',
    '| Relative Path | Filename | Size (KB) | Rows | Cols | Identity | Source | Likely Purpose |',
    '|---|---|---|---|---|---|---|---|'
]

for r in inventory_records:
    size_kb = round(r['size_bytes'] / 1024, 2)
    md_lines.append(f"| `{r['original_path']}` | `{r['filename']}` | {size_kb} | {r['row_count']} | {r['col_count']} | {r['dataset_identity']} | {r['source']} | {r['likely_purpose']} |")

md_lines.extend([
    '',
    '## Identified Target Datasets vs Downloaded Files',
    '',
    'The user specified an intention to download 5 datasets. Detailed inspection reveals the exact distribution below:',
    '',
    '### 1. IoT Temperature Forecasting',
    '- **Status**: PRESENT AS JUPYTER NOTEBOOK (Not an independent CSV file)',
    '- **Original Source**: Kaggle (`iot-temperature-forecasting.ipynb`)',
    '- **Original Folder**: `Datasets/` & `_original_downloads/`',
    '- **Actual Data Files**: `01_temperature_forecasting/iot_temperature_forecasting.ipynb`',
    '- **Rows**: 112 cells',
    '- **Columns**: NOT PRESENT (Notebook format)',
    '- **Important Columns**: References underlying `IOT-temp.csv` columns (`noted_date`, `temp`, `out/in`)',
    '- **Time column**: NOT PRESENT in notebook directly (uses `noted_date` in referenced dataset)',
    '- **Temperature**: NOT PRESENT in notebook directly (uses `temp` in referenced dataset)',
    '- **Humidity**: NOT PRESENT',
    '- **Energy**: NOT PRESENT',
    '- **Power**: NOT PRESENT',
    '- **Voltage**: NOT PRESENT',
    '- **Current**: NOT PRESENT',
    '- **Sensor/device ID**: NOT PRESENT',
    '- **Location**: NOT PRESENT',
    '- **Failure/anomaly**: NOT PRESENT',
    '- **Other relevant fields**: Contains exploratory data analysis, HoloViews visual charts, and forecasting models trained on `IOT-temp.csv`.',
    '',
    '### 2. Temperature Readings: IoT Devices',
    '- **Status**: PRESENT',
    '- **Original Source**: Kaggle (`temperature-readings-iot-devices` by Manikanta Kumar)',
    '- **Original Folder**: `Datasets/archive/` (from `archive.zip`)',
    '- **Actual Data Files**: `02_iot_temperature/iot_temperature_readings.csv`',
    '- **Rows**: 97,606',
    '- **Columns**: 5',
    '- **Important Columns**: `noted_date`, `temp`, `out/in`',
    '- **Time column**: `noted_date` (DD-MM-YYYY HH:MM format)',
    '- **Temperature**: `temp` (Integer °C, range 21 to 51 °C)',
    '- **Humidity**: NOT PRESENT',
    '- **Energy**: NOT PRESENT',
    '- **Power**: NOT PRESENT',
    '- **Voltage**: NOT PRESENT',
    '- **Current**: NOT PRESENT',
    '- **Sensor/device ID**: `room_id/id` (constant `Room Admin`), row ID `id`',
    '- **Location**: `out/in` (`In`: 20,345 records, `Out`: 77,261 records)',
    '- **Failure/anomaly**: NOT PRESENT',
    '- **Other relevant fields**: `id` (__export__.temp_log_...)',
    '',
    '### 3. Energy Consumption Prediction',
    '- **Status**: PRESENT',
    '- **Original Source**: Kaggle (`energy-consumption-prediction`)',
    '- **Original Folder**: `Datasets/archive (1)/` (from `archive (1).zip`)',
    '- **Actual Data Files**: `03_energy_consumption/energy_consumption_prediction.csv`',
    '- **Rows**: 1,000',
    '- **Columns**: 11',
    '- **Important Columns**: `Timestamp`, `Temperature`, `Humidity`, `SquareFootage`, `Occupancy`, `HVACUsage`, `LightingUsage`, `RenewableEnergy`, `EnergyConsumption`',
    '- **Time column**: `Timestamp` (YYYY-MM-DD HH:MM:SS format, hourly)',
    '- **Temperature**: `Temperature` (Ambient building temperature °C)',
    '- **Humidity**: `Humidity` (%)',
    '- **Energy**: `EnergyConsumption` (Total kWh), `RenewableEnergy` (kWh)',
    '- **Power**: NOT PRESENT (Energy per hour in kWh)',
    '- **Voltage**: NOT PRESENT',
    '- **Current**: NOT PRESENT',
    '- **Sensor/device ID**: NOT PRESENT',
    '- **Location**: NOT PRESENT (`SquareFootage` characterizes the facility)',
    '- **Failure/anomaly**: NOT PRESENT',
    '- **Other relevant fields**: `Occupancy`, `HVACUsage` (On/Off), `LightingUsage` (On/Off), `DayOfWeek`, `Holiday` (Yes/No)',
    '',
    '### 4. EVIoT Predictive Maintenance Dataset',
    '- **Status**: PRESENT',
    '- **Original Source**: Kaggle (`ev-predictive-maintenance-dataset-15min`)',
    '- **Original Folder**: `Datasets/archive (2)/` (from `archive (2).zip`)',
    '- **Actual Data Files**: `04_predictive_maintenance/eviot_predictive_maintenance.csv`',
    '- **Rows**: 175,393',
    '- **Columns**: 30',
    '- **Important Columns**: `Timestamp`, `Battery_Voltage`, `Battery_Current`, `Battery_Temperature`, `Motor_Temperature`, `Power_Consumption`, `Ambient_Temperature`, `Ambient_Humidity`, `Failure_Probability`, `Maintenance_Type`',
    '- **Time column**: `Timestamp` (15-minute interval, 2020-01-01 to 2025-01-01)',
    '- **Temperature**: `Battery_Temperature`, `Motor_Temperature`, `Tire_Temperature`, `Ambient_Temperature`',
    '- **Humidity**: `Ambient_Humidity`',
    '- **Energy**: NOT PRESENT',
    '- **Power**: `Power_Consumption` (kW)',
    '- **Voltage**: `Battery_Voltage` (V)',
    '- **Current**: `Battery_Current` (A)',
    '- **Sensor/device ID**: NOT PRESENT (Continuous vehicle powertrain telemetry)',
    '- **Location**: NOT PRESENT (`Route_Roughness`, `Distance_Traveled` describe terrain)',
    '- **Failure/anomaly**: `Failure_Probability`, `Maintenance_Type`, `RUL`, `TTF`, `Component_Health_Score`',
    '- **Other relevant fields**: `SoC`, `SoH`, `Charge_Cycles`, `Motor_Vibration`, `Motor_Torque`, `Motor_RPM`, `Brake_Pad_Wear`, `Brake_Pressure`, `Reg_Brake_Efficiency`, `Tire_Pressure`, `Suspension_Load`, `Load_Weight`, `Driving_Speed`, `Idle_Time`',
    '',
    '### 5. Journey to Zero / Predict Electricity Consumption',
    '- **Status**: PRESENT',
    '- **Original Source**: Kaggle (`predict-electricity-consumption`)',
    '- **Original Folder**: `Datasets/predict-electricity-consumption/` (from `predict-electricity-consumption.zip`)',
    '- **Actual Data Files**: `05_electricity_forecasting/journey_to_zero_electricity_train.csv` (8,592 rows), `..._test.csv` (168 rows), `..._sample_submission.csv` (168 rows)',
    '- **Rows**: 8,592 (train), 168 (test)',
    '- **Columns**: 13 (train), 12 (test)',
    '- **Important Columns**: `time`, `temp`, `dwpt`, `rhum`, `el_price`, `consumption`',
    '- **Time column**: `time` (Hourly ISO timestamp with offset)',
    '- **Temperature**: `temp` (Ambient outdoor temperature °C), `dwpt` (Dew point temperature °C)',
    '- **Humidity**: `rhum` (Relative humidity %)',
    '- **Energy**: `consumption` (Hourly electricity consumption)',
    '- **Power**: NOT PRESENT',
    '- **Voltage**: NOT PRESENT',
    '- **Current**: NOT PRESENT',
    '- **Sensor/device ID**: NOT PRESENT',
    '- **Location**: NOT PRESENT',
    '- **Failure/anomaly**: NOT PRESENT',
    '- **Other relevant fields**: `prcp` (precipitation), `snow`, `wdir` (wind direction), `wspd` (wind speed), `wpgt` (gust), `pres` (air pressure), `coco` (weather condition code), `el_price` (electricity spot price)',
    '',
    '### Genuine Cold-Chain Logistics Data',
    '- **Status**: NOT PRESENT IN PUBLIC DOWNLOADS',
    '- **Cold Chain Baseline**: The only cold chain refrigerated transport dataset in the project is `D:/COLDCHAIN-AI/data/raw/simulated_cold_chain.csv` (12,000 rows across 3 cold chain sensors CC-01, CC-02, CC-03).',
    '- **Scientific Disclosure**: Public datasets represent ambient room IoT, building HVAC, EV powertrains, and regional electricity grids. They provide external algorithmic stress-testing and transfer-learning validation, but are NOT cold-chain logistics telemetry.'
])

(reports_dir / 'DATASET_INVENTORY.md').write_text('\n'.join(md_lines), encoding='utf-8')
print('Wrote DATASET_INVENTORY.md')
