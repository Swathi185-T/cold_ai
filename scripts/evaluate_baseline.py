import json
from pathlib import Path
import pandas as pd
import numpy as np
import torch

from core_preprocessing import prepare, sequences, FEATURES
from ml.mad_tcn import MADTCN
from core import risk
from optimization.nsga2_optimizer import run_nsga2

def evaluate_baseline():
    print("Evaluating baseline simulation model...")
    df = pd.read_csv('data/raw/simulated_cold_chain.csv')
    df_prep = prepare(df)
    df_cc01 = df_prep[df_prep.sensor_id == 'CC-01']
    
    x, y = sequences(df_cc01, window=60, horizon=15)
    n_train = int(len(x) * 0.70)
    n_val = int(len(x) * 0.85)
    
    x_test = x[n_val:]
    y_test = y[n_val:]
    
    model = MADTCN(len(FEATURES))
    model.load_state_dict(torch.load('models/mad_tcn_best.pt', map_location='cpu', weights_only=True))
    model.eval()
    
    with torch.no_grad():
        preds = model(torch.tensor(x_test, dtype=torch.float32)).numpy()
        
    mae = float(np.mean(np.abs(preds - y_test)))
    rmse = float(np.sqrt(np.mean((preds - y_test) ** 2)))
    
    # Avoid zero division in MAPE
    non_zero = (np.abs(y_test) > 1e-4)
    mape = float(np.mean(np.abs((preds[non_zero] - y_test[non_zero]) / y_test[non_zero])) * 100)
    
    ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
    ss_res = np.sum((y_test - preds) ** 2)
    r2 = float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0
    
    horizon_metrics = []
    for h in range(15):
        h_mae = float(np.mean(np.abs(preds[:, h] - y_test[:, h])))
        h_rmse = float(np.sqrt(np.mean((preds[:, h] - y_test[:, h]) ** 2)))
        horizon_metrics.append({'step': f't+{h+1}', 'mae': round(h_mae, 4), 'rmse': round(h_rmse, 4)})
        
    results = {
        'experiment_id': 'baseline_simulation_cc01',
        'dataset': 'SIMULATION',
        'dataset_path': 'data/raw/simulated_cold_chain.csv',
        'features_count': len(FEATURES),
        'window_size': 60,
        'horizon': 15,
        'train_samples': n_train,
        'val_samples': n_val - n_train,
        'test_samples': len(x_test),
        'mae': round(mae, 4),
        'rmse': round(rmse, 4),
        'mape': round(mape, 4),
        'r2': round(r2, 4),
        'horizon_metrics': horizon_metrics
    }
    
    out_dir = Path('reports/baseline_validation')
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'baseline_metrics.json').write_text(json.dumps(results, indent=2))
    
    print(f"Baseline evaluated: MAE={mae:.4f}, RMSE={rmse:.4f}, R2={r2:.4f}, MAPE={mape:.2f}%")
    return results

if __name__ == '__main__':
    evaluate_baseline()
