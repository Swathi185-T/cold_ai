"""Prediction-guided cold-chain analytical pipeline."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

PROFILES = {
    'Food': (0.0, 5.0),
    'Vaccine': (2.0, 8.0),
    'Medicine': (2.0, 8.0),
    'Generic': (0.0, 5.0)
}

def clean_frame(frame):
    import pandas as pd
    required = {'timestamp', 'sensor_id', 'temperature'}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')
    df = frame.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
    df = df.dropna(subset=['timestamp', 'sensor_id', 'temperature']).sort_values(['sensor_id', 'timestamp']).drop_duplicates(['sensor_id', 'timestamp'])
    for col in ['humidity', 'ambient_temperature', 'power_kw', 'compressor_state', 'door_open']:
        if col not in df:
            df[col] = 0.0
    df['temperature_delta'] = df.groupby('sensor_id').temperature.diff().fillna(0)
    df['temperature_slope'] = df.groupby('sensor_id').temperature.transform(lambda x: x.rolling(5, min_periods=2).mean().diff()).fillna(0)
    return df

def predict_future(temperatures, horizon=15):
    x = np.asarray(temperatures, dtype=float)
    slope = float(np.mean(np.diff(x[-min(len(x), 10):]))) if len(x) > 1 else 0.0
    return (x[-1] + slope * np.arange(1, horizon + 1)).round(3).tolist()

def risk(prediction, profile='Food'):
    lo, hi = PROFILES.get(profile, PROFILES['Generic'])
    p = np.asarray(prediction, dtype=float)
    if len(p) == 0:
        return {
            'risk_score': 0.0,
            'risk_level': 'LOW',
            'risk_reason': f'No forecast points available. Safe profile limits: {lo:.1f} to {hi:.1f} °C.',
            'predicted_breach_time': None
        }
    violation = np.maximum(p - hi, 0) + np.maximum(lo - p, 0)
    diff_mean = float(np.diff(p).mean()) if len(p) > 1 else 0.0
    score = float(np.clip(100 * (violation.mean() / (hi - lo + 1e-6) + max(0.0, diff_mean) * 0.08), 0, 100))
    level = 'CRITICAL' if score >= 70 else 'HIGH' if score >= 40 else 'MEDIUM' if score >= 15 else 'LOW'
    breach = next((i + 1 for i, v in enumerate(p) if v < lo or v > hi), None)
    return {
        'risk_score': round(score, 2),
        'risk_level': level,
        'risk_reason': f'Predicted temperature range {p.min():.1f} to {p.max():.1f} °C against {lo:.1f} to {hi:.1f} °C profile limits.',
        'predicted_breach_time': breach
    }

def energy(current, ambient, intensity, duty):
    return round(max(0.05, 0.25 + 0.035 * max(ambient - current, 0)) * (0.35 + 0.65 * intensity) * duty, 3)

def optimize(current, ambient, future_risk):
    candidates = []
    for intensity in np.linspace(0.2, 1.0, 17):
        for duty in np.linspace(0.3, 1.0, 15):
            cooling = 3.2 * intensity * duty
            residual = max(0.0, future_risk - cooling * 18)
            e = energy(current, ambient, intensity, duty)
            candidates.append({
                'cooling_intensity': round(float(intensity), 2),
                'compressor_duty_cycle': round(float(duty), 2),
                'safety_risk': round(residual, 2),
                'estimated_energy_kwh': e,
                'expected_temperature': round(current - cooling, 2)
            })
    pareto = [
        a for a in candidates
        if not any(
            b['safety_risk'] <= a['safety_risk'] and
            b['estimated_energy_kwh'] <= a['estimated_energy_kwh'] and
            (b['safety_risk'] < a['safety_risk'] or b['estimated_energy_kwh'] < a['estimated_energy_kwh'])
            for b in candidates
        )
    ]
    max_e = max(y['estimated_energy_kwh'] for y in pareto) if pareto else 1.0
    rec = min(pareto, key=lambda x: 0.65 * x['safety_risk'] / 100 + 0.35 * x['estimated_energy_kwh'] / max_e)
    rec['explanation'] = 'Selected from a non-dominated energy/safety trade-off using predicted future risk, not current temperature alone.'
    return pareto, rec

def prediction_guided_optimization(state, profile='Food'):
    forecast = predict_future(state['temperatures'])
    assessment = risk(forecast, profile)
    pareto, recommendation = optimize(state['temperatures'][-1], state.get('ambient_temperature', 20), assessment['risk_score'])
    return {
        'forecast': forecast,
        'risk': assessment,
        'pareto_solutions': pareto,
        'recommended_solution': recommendation
    }
