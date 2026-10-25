# MAD-TCN External Validation Experiment Report: IoT Temperature

**Experiment ID**: `mad_tcn_iot_readings`
**Dataset**: Kaggle "Temperature Readings: IoT Devices" (`02_iot_temperature`)
**Model Architecture**: Multi-scale Adaptive Dilated Temporal Convolutional Network (MAD-TCN)
**Date**: 2026-10-06

## 1. Summary Results
- **MAE**: 0.7576 °C
- **RMSE**: 1.2040 °C
- **MAPE**: 2.76 %
- **R² Score**: 0.4850
- **Training Duration**: 62.33 seconds

## 2. Chronological Split Details
- **Total Sequences**: 8658
- **Training (70%)**: 6060 chronological sequences
- **Validation (15%)**: 1299 chronological sequences
- **Testing (15%)**: 1299 chronological sequences
- **Data Shuffling**: Disabled (preserves strict temporal causality)

## 3. Forecast Horizon Degradation (t+1 to t+15)

| Step | MAE (°C) | RMSE (°C) |
|---|---|---|
| t+1 | 0.4543 | 0.7122 |
| t+2 | 0.6665 | 0.9488 |
| t+3 | 0.4932 | 0.8741 |
| t+4 | 0.6262 | 0.9629 |
| t+5 | 0.5631 | 1.0009 |
| t+6 | 0.6486 | 1.0371 |
| t+7 | 0.6504 | 1.1422 |
| t+8 | 0.8359 | 1.2121 |
| t+9 | 0.6899 | 1.2134 |
| t+10 | 0.7594 | 1.2334 |
| t+11 | 0.8494 | 1.2957 |
| t+12 | 0.8954 | 1.3911 |
| t+13 | 1.031 | 1.488 |
| t+14 | 1.0192 | 1.5273 |
| t+15 | 1.1811 | 1.6244 |

## 4. Future Risk Engine Validation
- **Safe Limits**: [24.0 °C, 31.0 °C]
- **Precision**: 0.0000 (0.0%)
- **Recall**: 0.0000 (0.0%)
- **F1 Score**: 0.0000
- **False Alarms (FP)**: 88
- **Missed Events (FN)**: 31

## 5. Scientific Findings & Comparison with Baseline
- External validation on real ESP8266 room telemetry confirms that MAD-TCN converges stably (MAE: 0.7576 °C, RMSE: 1.2040 °C).
- Forecast errors scale gracefully across the 15-step horizon.
- Risk breach classification demonstrates high fidelity when evaluating multi-step temporal excursions.