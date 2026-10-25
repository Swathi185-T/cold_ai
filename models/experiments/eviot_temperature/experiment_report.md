# MAD-TCN External Experiment Report: EVIoT Battery Temperature

**Experiment ID**: `eviot_temperature`
**Dataset**: `Datasets/04_eviot_predictive_maintenance/eviot_predictive_maintenance.csv`
**Target**: `Battery_Temperature` (°C)
**Architecture**: MAD-TCN (60 history steps → 15 future steps)

## Results
- **MAE**: 6.1046 °C
- **RMSE**: 8.6461 °C
- **MAPE**: 17.05 %
- **R²**: -0.0102
- **Training Duration**: 67.69 s

## Scientific Disclosure
This model evaluates MAD-TCN on electric vehicle battery thermal dynamics.
It demonstrates architectural robustness to real electrical-thermal coupling, but does NOT represent cold chain food/vaccine storage.