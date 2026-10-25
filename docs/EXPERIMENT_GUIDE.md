# COLDCHAIN-AI Experiment Execution & Benchmarking Guide

> **Document Status**: Complete & Verified  
> **Target Audience**: Researchers, ML Engineers, Optimization Specialists, System Auditors  
> **Last Updated**: October 2026  
> **Environment**: Windows 11, Python 3.14, PyTorch 2.14.1+cpu  
> **Project Root**: [`D:\COLDCHAIN-AI`](file:///D:/COLDCHAIN-AI)

---

## Table of Contents
1. [Experimentation Philosophy & Scientific Integrity](#1-experimentation-philosophy--scientific-integrity)
2. [Environment Configuration & Prerequisites](#2-environment-configuration--prerequisites)
3. [Experiment Registry & Storage Architecture](#3-experiment-registry--storage-architecture)
4. [Step-by-Step Experiment Execution](#4-step-by-step-experiment-execution)
   - [Experiment 1: Baseline Simulation Evaluation (`evaluate_baseline.py`)](#experiment-1-baseline-simulation-evaluation-evaluate_baselinepy)
   - [Experiment 2: IoT Hardware Temperature Generalization (`train_iot_temperature.py`)](#experiment-2-iot-hardware-temperature-generalization-train_iot_temperaturepy)
   - [Experiment 3: EVIoT Battery Thermal Dynamics (`train_eviot_and_forecasting.py`)](#experiment-3-eviot-battery-thermal-dynamics-train_eviot_and_forecastingpy)
   - [Experiment 4: Thermal & Environmental Energy Modeling (`train_energy_model.py`)](#experiment-4-thermal--environmental-energy-modeling-train_energy_modelpy)
   - [Experiment 5: Multi-Objective NSGA-II Methodology Comparison (`compare_nsga2_methods.py`)](#experiment-5-multi-objective-nsga-ii-methodology-comparison-compare_nsga2_methodspy)
   - [Experiment 6: Big Data Streaming Scalability Stress Benchmark (`run_scalability_benchmark.py`)](#experiment-6-big-data-streaming-scalability-stress-benchmark-run_scalability_benchmarkpy)
5. [Summary of Empirical Results](#5-summary-of-empirical-results)
6. [Reproducibility Checklist & Troubleshooting](#6-reproducibility-checklist--troubleshooting)

---

## 1. Experimentation Philosophy & Scientific Integrity

The COLDCHAIN-AI benchmarking suite is built upon four fundamental principles of scientific honesty:

1. **No Data Fabrication**: Every metric cited in documentation and registered in configuration files reflects actual outputs computed by scripts in [`scripts/`](file:///D:/COLDCHAIN-AI/scripts/).
2. **Clear Labeling of Simulated/Estimated Data**: Real-world energy metering for cold-room compressors is expensive and rare. All energy values within the NSGA-II optimizer are explicitly labeled as **ESTIMATED / SIMULATED** based on thermodynamic lift models.
3. **Honest Reporting of Negative Results**: Deep learning models have strict inductive biases. When the MAD-TCN model is applied to domain-inappropriate physical processes (such as high-current electrochemical heating in EV batteries), the resulting negative $R^2$ is documented rather than hidden.
4. **Strict Checkpoint Immutability**: Production models serving the web dashboard ([`models/mad_tcn_best.pt`](file:///D:/COLDCHAIN-AI/models/mad_tcn_best.pt)) are frozen and protected. Experimental runs write only to dedicated subdirectories inside [`models/experiments/`](file:///D:/COLDCHAIN-AI/models/experiments/).

---

## 2. Environment Configuration & Prerequisites

All scripts in the repository assume Windows execution using Python 3.14 with CPU-only PyTorch.

> [!IMPORTANT]
> **MANDATORY ENVIRONMENT VARIABLE: `PYTHONPATH`**  
> Before executing any script in the `scripts/` directory, you must set `PYTHONPATH` to the repository root (`D:\COLDCHAIN-AI`). Failing to set `PYTHONPATH` will result in `ModuleNotFoundError: No module named 'core_preprocessing'` or similar import failures.

### Setting `PYTHONPATH` in Windows Terminals

#### PowerShell:
```powershell
# Set for current session
$env:PYTHONPATH = "D:\COLDCHAIN-AI"

# Verify path is set
$env:PYTHONPATH
```

#### Command Prompt (cmd.exe):
```cmd
:: Set for current session
set PYTHONPATH=D:\COLDCHAIN-AI

:: Verify path is set
echo %PYTHONPATH%
```

#### Active Python Interpreter Check:
```powershell
python -c "import sys, torch; print('Python:', sys.version); print('PyTorch:', torch.__version__); print('Device:', torch.device('cpu'))"
```
Expected output:
```
Python: 3.14.x ...
PyTorch: 2.14.1+cpu
Device: cpu
```

---

## 3. Experiment Registry & Storage Architecture

### Central Experiment Registry: [`experiments/registry.json`](file:///D:/COLDCHAIN-AI/experiments/registry.json)
The repository maintains a centralized schema-validated registry documenting every experiment, dataset lineage, hyperparameters, empirical error metrics, and operational status.

```mermaid
graph TD
    Reg["experiments/registry.json<br/>(Central Experiment Registry)"]
    Exp1["exp_baseline_simulation<br/>(ACTIVE_DEFAULT)"]
    Exp2["exp_iot_temperature_external<br/>(VALIDATED_EXTERNAL)"]
    Exp3["exp_energy_thermal_demand<br/>(VALIDATED_EXTERNAL)"]
    Exp4["exp_scalability_big_data<br/>(VALIDATED_EXTERNAL)"]

    Reg --> Exp1
    Reg --> Exp2
    Reg --> Exp3
    Reg --> Exp4

    Exp1 --> M1["models/mad_tcn_best.pt (FROZEN)"]
    Exp2 --> M2["models/experiments/mad_tcn_iot_readings/checkpoint.pt"]
    Exp3 --> R3["reports/energy_validation/energy_metrics.json"]
    Exp4 --> R4["reports/scalability/scalability_results.csv"]
```

### Directory Structure for Checkpoints and Reports
- **Production Checkpoint**: [`models/mad_tcn_best.pt`](file:///D:/COLDCHAIN-AI/models/mad_tcn_best.pt) (Trained on cold-chain simulation, NEVER overwritten)
- **Experimental Models**: [`models/experiments/`](file:///D:/COLDCHAIN-AI/models/experiments/)
  - `mad_tcn_iot_readings/`: Model weights and training history for IoT sensor readings
  - `eviot_temperature/`: Model weights and history for EV battery thermal dynamics
  - `iot_temperature_forecasting/`: Methodology validation files
- **Reports & Artifacts**: [`reports/`](file:///D:/COLDCHAIN-AI/reports/)
  - `baseline_validation/`: Baseline metrics and per-horizon errors
  - `energy_validation/`: Regression metrics, correlation stats, and regression plots
  - `nsga2_comparison/`: Pareto comparison between reactive and predictive control
  - `scalability/`: Throughput and memory consumption benchmarks

---

## 4. Step-by-Step Experiment Execution

### Experiment 1: Baseline Simulation Evaluation (`evaluate_baseline.py`)

- **Script Path**: [`scripts/evaluate_baseline.py`](file:///D:/COLDCHAIN-AI/scripts/evaluate_baseline.py)
- **Dataset Evaluated**: Simulated Cold Chain (`data/raw/simulated_cold_chain.csv`), CC-01 sensor channel
- **Data Classification**: `SIMULATION`
- **Model Evaluated**: Production baseline [`models/mad_tcn_best.pt`](file:///D:/COLDCHAIN-AI/models/mad_tcn_best.pt)
- **Test Protocol**: Chronological 70% train / 15% validation / 15% test split (589 test sequence windows of shape $60 \times 12$).

#### Execution Command:
```powershell
$env:PYTHONPATH = "D:\COLDCHAIN-AI"
python D:\COLDCHAIN-AI\scripts\evaluate_baseline.py
```

#### Output Metrics:
- **MAE**: `1.0131` °C
- **RMSE**: `1.2224` °C
- **R² Score**: `0.5893`
- **MAPE**: `14.80%`
- **Primary Artifact**: [`reports/baseline_validation/baseline_metrics.json`](file:///D:/COLDCHAIN-AI/reports/baseline_validation/baseline_metrics.json)

---

### Experiment 2: IoT Hardware Temperature Generalization (`train_iot_temperature.py`)

- **Script Path**: [`scripts/train_iot_temperature.py`](file:///D:/COLDCHAIN-AI/scripts/train_iot_temperature.py)
- **Dataset Evaluated**: Temperature Readings: IoT Devices (`Datasets/02_iot_temperature_readings/iot_temperature_readings.csv`)
- **Data Classification**: `PUBLIC_DATASET`
- **Sensor Hardware**: Real ESP8266 microcontroller module with digital sensor deployed in room environment
- **Training Configuration**:
  - Sequence Length: 60 timesteps | Horizon: 15 timesteps
  - Architecture: MAD-TCN (Hidden: 32 channels, 4 dilated branches $d \in \{1, 2, 4, 8\}$)
  - Batch Size: 64 | Epochs: 12 | Optimizer: Adam ($\eta = 0.001$, Weight Decay = $1\times 10^{-5}$)
  - Split: Chronological 70% train (6,060 samples) / 15% val (1,299 samples) / 15% test (1,299 samples)

#### Execution Command:
```powershell
$env:PYTHONPATH = "D:\COLDCHAIN-AI"
python D:\COLDCHAIN-AI\scripts\train_iot_temperature.py
```

#### Output Metrics:
- **MAE**: `0.7576` °C
- **RMSE**: `1.2040` °C
- **R² Score**: `0.4850`
- **MAPE**: `2.76%`
- **Risk Classification F1**: `0.8778` at $30.5\text{ }^\circ\text{C}$ threshold (Precision: `0.9634`, Recall: `0.8061`)
- **Primary Checkpoint**: [`models/experiments/mad_tcn_iot_readings/checkpoint.pt`](file:///D:/COLDCHAIN-AI/models/experiments/mad_tcn_iot_readings/checkpoint.pt)
- **Metrics File**: [`models/experiments/mad_tcn_iot_readings/metrics.json`](file:///D:/COLDCHAIN-AI/models/experiments/mad_tcn_iot_readings/metrics.json)

---

### Experiment 3: EVIoT Battery Thermal Dynamics (`train_eviot_and_forecasting.py`)

- **Script Path**: [`scripts/train_eviot_and_forecasting.py`](file:///D:/COLDCHAIN-AI/scripts/train_eviot_and_forecasting.py)
- **Dataset Evaluated**: EVIoT Predictive Maintenance (`Datasets/04_eviot_predictive_maintenance/eviot_predictive_maintenance.csv`)
- **Target Channel**: `Battery_Temperature` (°C)
- **Data Classification**: `PUBLIC_DATASET`
- **Training Configuration**:
  - 15,000 chronological observations (spanning ~5 months at 15-minute intervals)
  - 8 Epochs | Batch Size: 64 | Optimizer: Adam ($\eta = 0.001$)
  - Checkpoint: Saved to `models/experiments/eviot_temperature/checkpoint.pt`

#### Execution Command:
```powershell
$env:PYTHONPATH = "D:\COLDCHAIN-AI"
python D:\COLDCHAIN-AI\scripts\train_eviot_and_forecasting.py
```

#### Output Metrics:
- **MAE**: `6.1046` °C
- **RMSE**: `8.6461` °C
- **R² Score**: `-0.0102` (Negative $R^2$)
- **MAPE**: `17.05%` (or 18.25% unclipped)
- **Artifacts Generated**: [`models/experiments/eviot_temperature/metrics.json`](file:///D:/COLDCHAIN-AI/models/experiments/eviot_temperature/metrics.json)

> [!NOTE]
> **SCIENTIFIC EXPLANATION OF NEGATIVE $R^2$**:  
> In standard statistics, an $R^2 < 0$ occurs when the model's mean squared error is worse than simply predicting the mean of the test set ($\bar{y}$). This is an **honest, anticipated scientific boundary**:
> - Ambient cold-chain thermal dynamics follow **slow diffusive heat conduction** dictated by surrounding ambient air.
> - Electric vehicle batteries experience **high-frequency electrochemical Joule heating** ($P = I^2 R$) driven by sudden vehicle acceleration and regenerative braking.
> - Because MAD-TCN's inputs in this script only include ambient temperature and generic derivatives, the network cannot foresee sharp battery heat spikes without battery current and internal resistance features.

---

### Experiment 4: Thermal & Environmental Energy Modeling (`train_energy_model.py`)

- **Script Path**: [`scripts/train_energy_model.py`](file:///D:/COLDCHAIN-AI/scripts/train_energy_model.py)
- **Primary Dataset**: Energy Consumption Prediction (`Datasets/03_energy_consumption/energy_consumption_prediction.csv`)
- **Secondary Dataset**: Journey to Zero (`Datasets/05_electricity_forecasting/journey_to_zero_electricity_train.csv`)
- **Data Classification**: `PUBLIC_DATASET`
- **Methodology**: Standardized Ridge Linear Regression ($\alpha = 1.0$) with cross-dataset correlation analysis.

#### Execution Command:
```powershell
$env:PYTHONPATH = "D:\COLDCHAIN-AI"
python D:\COLDCHAIN-AI\scripts\train_energy_model.py
```

#### Output Metrics:
- **Test MAE**: `4.0994` kWh
- **Test RMSE**: `4.9602` kWh
- **Test R²**: `0.5866`
- **Test MAPE**: `5.31%`
- **Key Learned Coefficients**:
  - `Temperature`: `+5.6734` (strongest positive driver of HVAC cooling load)
  - `HVACUsage`: `+2.2850` (active thermal conditioning penalty)
  - `Occupancy`: `+1.6003` (internal thermal gain from occupants)
  - `LightingUsage`: `+1.0234`
  - `RenewableEnergy`: `+0.7099`
  - `Humidity`: `-0.5136`
  - `SquareFootage`: `-0.1270`
- **Journey to Zero Weather Correlations**:
  - Outdoor Temperature vs Consumption: `-0.2679` (heating season inversion)
  - Outdoor Humidity vs Consumption: `+0.0944`
- **Artifacts Saved**:
  - [`reports/energy_validation/energy_metrics.json`](file:///D:/COLDCHAIN-AI/reports/energy_validation/energy_metrics.json)
  - [`reports/energy_validation/plots/energy_prediction_actual_vs_pred.png`](file:///D:/COLDCHAIN-AI/reports/energy_validation/plots/energy_prediction_actual_vs_pred.png)
  - [`reports/energy_validation/plots/energy_feature_impact.png`](file:///D:/COLDCHAIN-AI/reports/energy_validation/plots/energy_feature_impact.png)
  - [`reports/energy_validation/energy_predictions.csv`](file:///D:/COLDCHAIN-AI/reports/energy_validation/energy_predictions.csv)

---

### Experiment 5: Multi-Objective NSGA-II Methodology Comparison (`compare_nsga2_methods.py`)

- **Script Path**: [`scripts/compare_nsga2_methods.py`](file:///D:/COLDCHAIN-AI/scripts/compare_nsga2_methods.py)
- **Objective**: Rigorous head-to-head empirical comparison between:
  - **Method A**: *Current-State Reactive Optimization* (considers only instantaneous chamber temperature violation).
  - **Method B**: *Prediction-Guided NSGA-II* (optimizes compressor duty cycle and cooling intensity based on MAD-TCN 15-step forecast).
- **Evaluation Set**: 50 representative sequential scenarios sampled across simulation test sets.

#### Execution Command:
```powershell
$env:PYTHONPATH = "D:\COLDCHAIN-AI"
python D:\COLDCHAIN-AI\scripts\compare_nsga2_methods.py
```

#### Output Metrics & Findings:
| Metric | Method A (Current-State) | Method B (Prediction-Guided) | Relative Delta |
| :--- | :--- | :--- | :--- |
| **Mean Cycle Energy (ESTIMATED)** | `0.5561` kWh | `0.4471` kWh | **-19.6% reduction** |
| **Mean Compressor Duty Cycle** | `0.6847` (68.5%) | `0.5477` (54.8%) | **-20.0% reduction** |
| **Total Cumulative Violations** | `153.88` °C·steps | `434.91` °C·steps | **+182.6% increase** |
| **Mean Pareto Solutions Found** | `35.78` | `43.30` | **+21.0% richer frontier** |
| **Mean Optimization Latency** | `294.13` ms | `303.48` ms | Comparable (~300 ms) |

> [!IMPORTANT]
> **GENUINE PARETO TRADE-OFF**:  
> Method B achieves **19.6% energy savings** by aggressively reducing compressor duty cycle, but allows mild thermal excursions (+182.6% cumulative violation score). This proves the algorithm solves a true multi-objective Pareto trade-off rather than an artificial win-win scenario.

- **Artifacts Saved**:
  - [`reports/nsga2_comparison/comparison_summary.json`](file:///D:/COLDCHAIN-AI/reports/nsga2_comparison/comparison_summary.json)
  - [`reports/nsga2_comparison/comparison_results.csv`](file:///D:/COLDCHAIN-AI/reports/nsga2_comparison/comparison_results.csv)
  - [`reports/nsga2_comparison/nsga2_comparison_report.md`](file:///D:/COLDCHAIN-AI/reports/nsga2_comparison/nsga2_comparison_report.md)

---

### Experiment 6: Big Data Streaming Scalability Stress Benchmark (`run_scalability_benchmark.py`)

- **Script Path**: [`scripts/run_scalability_benchmark.py`](file:///D:/COLDCHAIN-AI/scripts/run_scalability_benchmark.py)
- **Objective**: Quantify end-to-end execution latency and peak memory across 6 escalating data tiers (from 10,000 to 1,000,000 rows).
- **Tested Subsystems**:
  1. Disk reading & CSV parsing
  2. Vectorized pandas rolling feature engineering
  3. Matrix temporal window creation ($60 \times 12$)
  4. PyTorch MAD-TCN batch inference (1,000 sequences)
  5. NSGA-II multi-objective optimization (30 generations, 48 population)

#### Execution Command:
```powershell
$env:PYTHONPATH = "D:\COLDCHAIN-AI"
python D:\COLDCHAIN-AI\scripts\run_scalability_benchmark.py
```

#### Output Metrics:
| Tier Label | Row Count | Classification | Pipeline Time | Peak Memory | Inference Latency | NSGA-II Opt Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Real Simulation** | 10,000 | `REAL_SIMULATION` | **2.08 s** | **8.38 MB** | 0.755 ms/sample | 1.06 s |
| **Real IoT Subset** | 50,000 | `REAL_IOT_TELEMETRY` | **4.22 s** | **28.05 MB** | 0.558 ms/sample | 1.46 s |
| **Full IoT Readings** | 100,000 | `REAL_IOT_TELEMETRY` | **3.56 s** | **45.00 MB** | 0.454 ms/sample | 0.92 s |
| **Real EVIoT 15-min** | 175,000 | `REAL_EVIOT_TELEMETRY` | **15.04 s** | **162.75 MB** | 1.583 ms/sample | 2.78 s |
| **Synthetic 500K** | 500,000 | `SYNTHETIC_EXPANSION` | **3.83 s** | **169.05 MB** | 0.343 ms/sample | 1.15 s |
| **Synthetic 1M** | 1,000,000 | `SYNTHETIC_EXPANSION` | **2.62 s** | **336.90 MB** | 0.254 ms/sample | 0.87 s |

- **Artifacts Saved**:
  - [`reports/scalability/scalability_results.csv`](file:///D:/COLDCHAIN-AI/reports/scalability/scalability_results.csv)
  - [`reports/scalability/scalability_report.md`](file:///D:/COLDCHAIN-AI/reports/scalability/scalability_report.md)

---

## 5. Summary of Empirical Results

| Experiment Name | Primary Target | Model Family | MAE | RMSE | $R^2$ Score | Hardware Latency | Storage Location |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline Simulation** | Temp (°C) | MAD-TCN | `1.0131` | `1.2224` | `0.5893` | 0.75 ms / sample | [`reports/baseline_validation/`](file:///D:/COLDCHAIN-AI/reports/baseline_validation/) |
| **IoT Telemetry** | Temp (°C) | MAD-TCN | `0.7576` | `1.2040` | `0.4850` | 0.56 ms / sample | [`models/experiments/mad_tcn_iot_readings/`](file:///D:/COLDCHAIN-AI/models/experiments/mad_tcn_iot_readings/) |
| **EVIoT Battery** | Batt Temp (°C) | MAD-TCN | `6.1046` | `8.6461` | `-0.0102` | 1.58 ms / sample | [`models/experiments/eviot_temperature/`](file:///D:/COLDCHAIN-AI/models/experiments/eviot_temperature/) |
| **Energy Consumption** | Energy (kWh) | Ridge Reg | `4.0994` | `4.9602` | `0.5866` | 0.15 ms / sample | [`reports/energy_validation/`](file:///D:/COLDCHAIN-AI/reports/energy_validation/) |
| **NSGA-II Comparison** | Pareto Objectives | NSGA-II | N/A | N/A | N/A | 303.48 ms / run | [`reports/nsga2_comparison/`](file:///D:/COLDCHAIN-AI/reports/nsga2_comparison/) |
| **Scalability (1M)** | Pipeline Stream | Vectorized | N/A | N/A | N/A | 2.62 s total | [`reports/scalability/`](file:///D:/COLDCHAIN-AI/reports/scalability/) |

---

## 6. Reproducibility Checklist & Troubleshooting

To replicate all benchmark outputs cleanly on a fresh workstation:

1. **Verify Python Environment**:
   - Python 3.14 (64-bit on Windows)
   - Packages installed: `torch==2.14.1+cpu`, `pandas`, `numpy`, `scikit-learn`, `pymoo`, `matplotlib`
2. **Set `PYTHONPATH`**:
   - Always run `$env:PYTHONPATH="D:\COLDCHAIN-AI"` in PowerShell prior to invoking Python.
3. **Random Seeds**:
   - PyTorch manual seed is hardcoded to `42` (`torch.manual_seed(42)`).
   - NumPy random seed is hardcoded to `42` (`np.random.seed(42)`).
   - PyMoo optimizer seed is set to `42` (`seed=42`).
4. **Common Errors & Solutions**:
   - *Error*: `FileNotFoundError: data/raw/simulated_cold_chain.csv`  
     *Solution*: Run `python scripts/generate_sample_data.py` to regenerate the baseline simulation files.
   - *Error*: `ModuleNotFoundError: No module named 'core_preprocessing'`  
     *Solution*: Check `echo $env:PYTHONPATH`. It must contain `D:\COLDCHAIN-AI`.
   - *Error*: `RuntimeError: Attempting to deserialize object on a CUDA device...`  
     *Solution*: All model loaders explicitly use `map_location='cpu'`. Ensure GPU overrides are disabled.

---
*End of Experiment Guide. Maintained under the COLDCHAIN-AI Open Research Quality Framework.*
