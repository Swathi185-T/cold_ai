# COLDCHAIN-AI Data Quality Assessment Report

**Audit Date**: 2026-10-06 | **Scope**: All public reference datasets and project simulation baseline

## 1. Overview Matrix

| Dataset | Rows | Cols | Missing Cells | Missing % | Dup Rows | Time Resolution | Temp Range (°C) | Quality Grade |
|---|---|---|---|---|---|---|---|---|
| `iot_temperature_readings.csv` | 97,606 | 5 | 0 | 0.00% | 1 | Irregular (1-10m) | 21.0 to 51.0 | High (Clean IoT) |
| `energy_consumption_prediction.csv` | 1,000 | 11 | 0 | 0.00% | 0 | 1 Hour | 20.0 to 30.0 | High (Clean Synthetic) |
| `eviot_predictive_maintenance.csv` | 175,393 | 30 | 0 | 0.00% | 0 | 15 Minutes | 25.0 to 60.0 (Batt) | High (Clean Telemetry) |
| `journey_to_zero_electricity_train.csv` | 8,592 | 13 | 15,104 | 13.52% | 0 | 1 Hour | -26.1 to 31.4 | Moderate (Weather Gaps) |
| `simulated_cold_chain.csv` (Baseline) | 12,000 | 10 | 0 | 0.00% | 0 | 1 Minute | 3.5 to 9.9 | High (Benchmark Ground Truth) |

## 2. In-Depth Dataset Quality Profiling

### Dataset 1: Temperature Readings IoT Devices (`iot_temperature_readings.csv`)
- **Total Observations**: 97,606
- **Columns (5)**: `id` (string), `room_id/id` (string), `noted_date` (string), `temp` (int64), `out/in` (string)
- **Missing Values**: 0 missing values across all columns (100% complete)
- **Duplicate Rows**: 1 exact duplicate record (`__export__.temp_log_196108_17e0b0fd`, `08-12-2018 09:29`)
- **Timestamp Validation**: 97,606 valid timestamps parsed using format `%d-%m-%Y %H:%M`. Zero invalid timestamps.
- **Chronological Order**: **REVERSED IN RAW DOWNLOAD**. Raw rows start on `2018-12-08 09:30:00` and end on `2018-07-28 07:06:00`. For any time-series modelling or sequence generation, chronological sorting `df.sort_values("noted_date")` is strictly required.
- **Temporal Span**: 2018-07-28 07:06:00 to 2018-12-08 09:30:00 (~133 days).
- **Sampling Gaps**: Irregular sampling interval. Median interval between successive readings is 0 minutes (multiple concurrent pings across In/Out), with occasional multi-hour gaps during sensor downtime.
- **Location Subsets**: `In` (Room Admin inside): 20,345 readings (mean 30.5°C, min 21°C, max 41°C). `Out` (Outside sensor): 77,261 readings (mean 36.3°C, min 24°C, max 51°C).
- **Impossible / Extreme Values**: Temperature range 21°C - 51°C is physically realistic for ambient Indian weather conditions where sensor was deployed. No physically impossible values (< -40°C or > 100°C).
- **Cold Chain Appropriateness**: Ambient room/outdoor monitoring only. Temperatures (21-51°C) do not match refrigerated storage profiles (0-5°C or 2-8°C). Used as external validation of MAD-TCN convergence on physical hardware telemetry.

### Dataset 2: Energy Consumption Prediction (`energy_consumption_prediction.csv`)
- **Total Observations**: 1,000
- **Columns (11)**: `Timestamp`, `Temperature`, `Humidity`, `SquareFootage`, `Occupancy`, `HVACUsage`, `LightingUsage`, `RenewableEnergy`, `DayOfWeek`, `Holiday`, `EnergyConsumption`
- **Missing Values**: 0 missing values (100% complete)
- **Duplicate Rows**: 0 duplicate rows
- **Timestamp Validation**: Hourly timestamps from `2022-01-01 00:00:00` to `2022-02-11 15:00:00`. Zero invalid timestamps.
- **Summary Statistics**: Temperature mean 25.04 ± 2.87°C; Humidity mean 49.8 ± 14.8%; EnergyConsumption mean 77.06 ± 8.14 kWh (min 53.26, max 99.20 kWh).
- **Cold Chain Appropriateness**: Facility HVAC energy proxy, not refrigeration compressor duty.

### Dataset 3: EVIoT Predictive Maintenance Dataset (`eviot_predictive_maintenance.csv`)
- **Total Observations**: 175,393
- **Columns (30)**: High-dimensional electrical, thermal, mechanical, and degradation telemetry.
- **Missing Values**: 0 missing values across all 30 columns (100% complete).
- **Duplicate Rows**: 0 duplicate rows.
- **Timestamp Validation**: Exactly 15-minute intervals spanning 5 years (`2020-01-01 00:00:00` to `2025-01-01 00:00:00`). Zero timestamp gaps.
- **Summary Statistics**: Battery Voltage: 352.7 ± 55.2 V (200.0 - 400.0 V); Battery Current: -47.9 ± 45.4 A (-200.0 to -10.0 A); Battery Temp: 33.4 ± 8.7°C (25.0 - 60.0°C); Power: 17.0 ± 16.5 kW; Failure Probability: binary/integer flags.
- **Cold Chain Appropriateness**: Electric vehicle battery/motor telemetry. High utility for Big Data streaming scalability, multi-feature sequence processing, and power-thermal dynamics.

### Dataset 4: Journey to Zero Electricity (`journey_to_zero_electricity_train.csv`)
- **Total Observations**: 8,592
- **Columns (13)**: `time`, `temp`, `dwpt`, `rhum`, `prcp`, `snow`, `wdir`, `wspd`, `wpgt`, `pres`, `coco`, `el_price`, `consumption`
- **Missing Values**: 15,104 missing entries, localized predominantly in weather indicators (`snow`: 7,878 missing, `wpgt`: 3,597 missing, `prcp`: 1,192 missing, `coco`: 138 missing). Target `consumption` has 0 missing values.
- **Duplicate Rows**: 0 duplicate rows.
- **Timestamp Validation**: Hourly timestamps from `2021-09-01 00:00:00+03:00` to `2022-08-24 23:00:00+03:00` (~1 complete year).
- **Summary Statistics**: Temp: 6.74 ± 9.26°C (-26.1°C to 31.4°C); Consumption: 0.88 ± 0.44 kWh (0.00 to 2.45 kWh).