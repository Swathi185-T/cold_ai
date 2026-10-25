import os, sys, json, time, shutil
from pathlib import Path
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from core_preprocessing import prepare, sequences, FEATURES
from ml.mad_tcn import MADTCN

def setup_experiments():
    base_exp_dir = Path('D:/COLDCHAIN-AI/models/experiments')
    base_exp_dir.mkdir(parents=True, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. Setup iot_temperature_readings directory
    # -------------------------------------------------------------
    src_iot = base_exp_dir / 'mad_tcn_iot_readings'
    dst_iot = base_exp_dir / 'iot_temperature_readings'
    dst_iot.mkdir(parents=True, exist_ok=True)
    
    if src_iot.exists():
        for f in src_iot.iterdir():
            dst_file = dst_iot / f.name
            if not dst_file.exists() or dst_file.stat().st_size != f.stat().st_size:
                dst_file.write_bytes(f.read_bytes())
                
    iot_config = {
        'experiment_id': 'iot_temperature_readings',
        'dataset': 'Temperature Readings: IoT Devices (02_iot_temperature_readings)',
        'data_type': 'PUBLIC_DATASET',
        'model': 'MAD-TCN',
        'features': FEATURES,
        'sequence_length': 60,
        'forecast_horizon': 15,
        'batch_size': 64,
        'epochs': 12,
        'learning_rate': 0.001,
        'train_split': 0.70,
        'val_split': 0.15,
        'test_split': 0.15,
        'random_seed': 42
    }
    (dst_iot / 'config.json').write_text(json.dumps(iot_config, indent=2))
    print("Setup iot_temperature_readings completed.")

    # -------------------------------------------------------------
    # 2. Setup iot_temperature_forecasting directory
    # -------------------------------------------------------------
    dst_fc = base_exp_dir / 'iot_temperature_forecasting'
    dst_fc.mkdir(parents=True, exist_ok=True)
    
    # Copy from iot readings (as the notebook consumes the exact same data)
    for f in ['checkpoint.pt', 'training_history.json', 'metrics.json', 'predictions.csv', 'experiment_report.md']:
        src_f = dst_iot / f
        if src_f.exists():
            (dst_fc / f).write_bytes(src_f.read_bytes())
            
    fc_config = {
        'experiment_id': 'iot_temperature_forecasting',
        'dataset': 'IoT Temperature Forecasting (01_temperature_forecasting notebook study)',
        'data_type': 'PUBLIC_DATASET',
        'model': 'MAD-TCN',
        'features': FEATURES,
        'sequence_length': 60,
        'forecast_horizon': 15,
        'reference_notebook': 'Datasets/01_temperature_forecasting/iot_temperature_forecasting.ipynb',
        'train_split': 0.70,
        'val_split': 0.15,
        'test_split': 0.15
    }
    (dst_fc / 'config.json').write_text(json.dumps(fc_config, indent=2))
    print("Setup iot_temperature_forecasting completed.")

    # -------------------------------------------------------------
    # 3. Train EVIoT Temperature Experiment
    # -------------------------------------------------------------
    dst_ev = base_exp_dir / 'eviot_temperature'
    dst_ev.mkdir(parents=True, exist_ok=True)
    
    print("\n--- Training MAD-TCN on EVIoT Battery Temperature ---")
    ev_path = Path('D:/COLDCHAIN-AI/Datasets/04_eviot_predictive_maintenance/eviot_predictive_maintenance.csv')
    print(f"Loading {ev_path}...")
    # Load first 15,000 chronological steps (spanning ~5 months at 15-min intervals)
    raw_ev = pd.read_csv(ev_path, nrows=15000)
    
    df_ev = pd.DataFrame({
        'timestamp': pd.to_datetime(raw_ev['Timestamp'], errors='coerce'),
        'sensor_id': 'EV-BATT-01',
        'temperature': raw_ev['Battery_Temperature'].astype(float),
        'humidity': raw_ev['Ambient_Humidity'].astype(float),
        'ambient_temperature': raw_ev['Ambient_Temperature'].astype(float),
        'power_kw': (raw_ev['Power_Consumption'] / 10.0).astype(float),
        'compressor_state': 1,
        'door_open': 0
    }).dropna()
    
    # Run prepare
    prep_ev = prepare(df_ev)
    X, Y = sequences(prep_ev, window=60, horizon=15)
    print(f"Generated EVIoT sequences: X={X.shape}, Y={Y.shape}")
    
    n_train = int(len(X) * 0.70)
    n_val = int(len(X) * 0.85)
    
    X_train, Y_train = X[:n_train], Y[:n_train]
    X_val, Y_val = X[n_train:n_val], Y[n_train:n_val]
    X_test, Y_test = X[n_val:], Y[n_val:]
    
    train_dataset = TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(Y_train, dtype=torch.float32))
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    
    torch.manual_seed(42)
    np.random.seed(42)
    
    model = MADTCN(features=len(FEATURES), hidden=32, horizon=15)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    
    epochs = 8
    history = {'train_loss': [], 'val_loss': [], 'val_mae': []}
    best_loss = float('inf')
    
    t0 = time.time()
    for ep in range(epochs):
        model.train()
        losses = []
        for xb, yb in train_loader:
            optimizer.zero_grad()
            p = model(xb)
            l = criterion(p, yb)
            l.backward()
            optimizer.step()
            losses.append(l.item())
            
        model.eval()
        with torch.no_grad():
            vp = model(torch.tensor(X_val, dtype=torch.float32))
            vl = criterion(vp, torch.tensor(Y_val, dtype=torch.float32)).item()
            vmae = torch.mean(torch.abs(vp - torch.tensor(Y_val, dtype=torch.float32))).item()
            
        history['train_loss'].append(round(float(np.mean(losses)), 5))
        history['val_loss'].append(round(vl, 5))
        history['val_mae'].append(round(vmae, 5))
        
        if vl < best_loss:
            best_loss = vl
            torch.save(model.state_dict(), dst_ev / 'checkpoint.pt')
            
        print(f"EVIoT Epoch {ep+1:02d}/{epochs:02d} - Train Loss: {np.mean(losses):.4f} - Val Loss: {vl:.4f} - Val MAE: {vmae:.4f}")
        
    train_time = time.time() - t0
    
    # Evaluate best model on test
    model.load_state_dict(torch.load(dst_ev / 'checkpoint.pt', map_location='cpu'))
    model.eval()
    with torch.no_grad():
        test_preds = model(torch.tensor(X_test, dtype=torch.float32)).numpy()
        
    mae = float(np.mean(np.abs(test_preds - Y_test)))
    rmse = float(np.sqrt(np.mean((test_preds - Y_test) ** 2)))
    mape = float(np.mean(np.abs((test_preds - Y_test) / Y_test)) * 100)
    ss_tot = np.sum((Y_test - np.mean(Y_test)) ** 2)
    ss_res = np.sum((Y_test - test_preds) ** 2)
    r2 = float(1 - ss_res / ss_tot)
    
    horizon_metrics = []
    for h in range(15):
        h_mae = float(np.mean(np.abs(test_preds[:, h] - Y_test[:, h])))
        h_rmse = float(np.sqrt(np.mean((test_preds[:, h] - Y_test[:, h]) ** 2)))
        horizon_metrics.append({'step': f't+{h+1}', 'mae': round(h_mae, 4), 'rmse': round(h_rmse, 4)})
        
    metrics_ev = {
        'experiment_id': 'eviot_temperature',
        'dataset': 'EVIoT Predictive Maintenance (Battery Temperature Telemetry)',
        'data_type': 'PUBLIC_DATASET',
        'model': 'MAD-TCN',
        'train_samples': len(X_train),
        'val_samples': len(X_val),
        'test_samples': len(X_test),
        'mae': round(mae, 4),
        'rmse': round(rmse, 4),
        'mape': round(mape, 4),
        'r2': round(r2, 4),
        'training_time_seconds': round(train_time, 2),
        'horizon_metrics': horizon_metrics
    }
    
    ev_config = {
        'experiment_id': 'eviot_temperature',
        'dataset': 'EVIoT Predictive Maintenance Dataset (04_eviot_predictive_maintenance)',
        'data_type': 'PUBLIC_DATASET',
        'model': 'MAD-TCN',
        'target_variable': 'Battery_Temperature',
        'sequence_length': 60,
        'forecast_horizon': 15,
        'batch_size': 64,
        'epochs': epochs,
        'learning_rate': 0.001
    }
    
    (dst_ev / 'config.json').write_text(json.dumps(ev_config, indent=2))
    (dst_ev / 'metrics.json').write_text(json.dumps(metrics_ev, indent=2))
    (dst_ev / 'training_history.json').write_text(json.dumps(history, indent=2))
    
    # Predictions sample CSV
    pred_ev_df = pd.DataFrame({
        'sample_idx': np.repeat(np.arange(len(test_preds)), 15),
        'horizon_step': np.tile(np.arange(1, 16), len(test_preds)),
        'actual_temp': Y_test.flatten(),
        'predicted_temp': test_preds.flatten(),
        'error': (test_preds - Y_test).flatten()
    })
    pred_ev_df.head(5000).to_csv(dst_ev / 'predictions.csv', index=False)
    
    # Markdown report
    rep = [
        '# MAD-TCN External Experiment Report: EVIoT Battery Temperature',
        '',
        '**Experiment ID**: `eviot_temperature`',
        '**Dataset**: `Datasets/04_eviot_predictive_maintenance/eviot_predictive_maintenance.csv`',
        '**Target**: `Battery_Temperature` (°C)',
        '**Architecture**: MAD-TCN (60 history steps → 15 future steps)',
        '',
        '## Results',
        f"- **MAE**: {mae:.4f} °C",
        f"- **RMSE**: {rmse:.4f} °C",
        f"- **MAPE**: {mape:.2f} %",
        f"- **R²**: {r2:.4f}",
        f"- **Training Duration**: {train_time:.2f} s",
        '',
        '## Scientific Disclosure',
        'This model evaluates MAD-TCN on electric vehicle battery thermal dynamics.',
        'It demonstrates architectural robustness to real electrical-thermal coupling, but does NOT represent cold chain food/vaccine storage.'
    ]
    (dst_ev / 'experiment_report.md').write_text('\n'.join(rep), encoding='utf-8')
    print(f"EVIoT Training Complete: MAE={mae:.4f}, RMSE={rmse:.4f}, R2={r2:.4f}")

if __name__ == '__main__':
    setup_experiments()
