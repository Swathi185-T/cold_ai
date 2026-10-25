# ColdChain AI Report

```json
{
  "data_provenance": "DEMONSTRATION / SIMULATION DATA",
  "energy_notice": "ENERGY VALUES ARE ESTIMATED/SIMULATED",
  "sensor": "TEST-01",
  "timestamp": "2026-10-06T17:57:43.025113+00:00",
  "current_temperature": 3.4942607593108406,
  "forecast": [
    4.14397668838501,
    5.086888313293457,
    4.576793193817139,
    5.118535041809082,
    4.339173793792725,
    3.7038826942443848,
    4.01222038269043,
    4.277037143707275,
    4.027024269104004,
    3.5367329120635986,
    3.996645212173462,
    4.207477569580078,
    4.231035232543945,
    3.8762645721435547,
    4.125854969024658
  ],
  "risk": {
    "risk_score": 0.27,
    "risk_level": "LOW",
    "risk_reason": "Predicted temperature range 3.5 to 5.1 \u00b0C against 0.0 to 5.0 \u00b0C profile limits.",
    "predicted_breach_time": 2
  },
  "pareto_solutions": [
    {
      "cooling_intensity": 0.10000000051690049,
      "compressor_duty_cycle": 0.20000000123273104,
      "target_temperature_offset": 0.2048291293748863,
      "safety_risk": 0.0,
      "estimated_energy_kwh": 0.06869917297325909
    }
  ],
  "recommendation": {
    "cooling_intensity": 0.10000000051690049,
    "compressor_duty_cycle": 0.20000000123273104,
    "target_temperature_offset": 0.2048291293748863,
    "safety_risk": 0.0,
    "estimated_energy_kwh": 0.06869917297325909,
    "expected_temperature": 3.4302607585855505,
    "explanation": "Selected from pymoo NSGA-II using future risk calculated from the MAD-TCN forecast."
  },
  "metrics": {
    "mae": 1.2500958442687988,
    "rmse": 1.467206597328186,
    "dataset": "SIMULATION"
  },
  "limitations": [
    "Simulated data",
    "CPU model",
    "No physical actuator validation"
  ]
}
```