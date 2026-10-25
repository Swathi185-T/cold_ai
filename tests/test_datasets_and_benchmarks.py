import json
from pathlib import Path
from django.test import TestCase
import pandas as pd
import torch

from ml.mad_tcn import MADTCN
from ml.inference import forecast
from core_preprocessing import FEATURES, prepare, sequences
from core import risk
from optimization.nsga2_optimizer import run_nsga2

class DatasetAndBenchmarkTests(TestCase):
    def test_01_dataset_directories_and_metadata_exist(self):
        datasets_dir = Path('D:/COLDCHAIN-AI/Datasets')
        required_dirs = [
            '01_temperature_forecasting',
            '02_iot_temperature_readings',
            '03_energy_consumption',
            '04_eviot_predictive_maintenance',
            '05_electricity_forecasting'
        ]
        for d in required_dirs:
            dp = datasets_dir / d
            self.assertTrue(dp.exists(), f"Missing directory {d}")
            meta_p = dp / 'metadata.json'
            self.assertTrue(meta_p.exists(), f"Missing metadata.json in {d}")
            meta = json.loads(meta_p.read_text(encoding='utf-8'))
            self.assertIn('dataset_name', meta)
            self.assertIn('source', meta)
            self.assertIn('data_type', meta)

    def test_02_original_downloads_preserved(self):
        orig_dir = Path('D:/COLDCHAIN-AI/Datasets/_original_downloads')
        self.assertTrue(orig_dir.exists())
        self.assertTrue((orig_dir / 'archive').exists())
        self.assertTrue((orig_dir / 'archive (1)').exists())
        self.assertTrue((orig_dir / 'archive (2)').exists())
        self.assertTrue((orig_dir / 'predict-electricity-consumption').exists())
        self.assertTrue((orig_dir / 'iot-temperature-forecasting.ipynb').exists())

    def test_03_experiment_registry_integrity(self):
        reg_p = Path('experiments/registry.json')
        self.assertTrue(reg_p.exists())
        reg = json.loads(reg_p.read_text(encoding='utf-8'))
        self.assertIn('experiments', reg)
        self.assertGreaterEqual(len(reg['experiments']), 3)
        for exp in reg['experiments']:
            self.assertIn('experiment_id', exp)
            self.assertIn('model', exp)
            self.assertIn('MAE', exp)
            self.assertIn('RMSE', exp)

    def test_04_baseline_model_inference_compatibility(self):
        # Verify baseline model checkpoint loads and produces 15-step forecast
        model = MADTCN(len(FEATURES))
        model.load_state_dict(torch.load('models/mad_tcn_best.pt', map_location='cpu', weights_only=True))
        model.eval()
        dummy_seq = torch.randn(1, 60, len(FEATURES))
        with torch.no_grad():
            out = model(dummy_seq).squeeze().tolist()
        self.assertEqual(len(out), 15)

    def test_05_external_iot_model_checkpoint(self):
        ckpt_p = Path('models/experiments/iot_temperature_readings/checkpoint.pt')
        self.assertTrue(ckpt_p.exists())
        model = MADTCN(len(FEATURES))
        model.load_state_dict(torch.load(ckpt_p, map_location='cpu', weights_only=True))
        model.eval()
        dummy_seq = torch.randn(1, 60, len(FEATURES))
        with torch.no_grad():
            out = model(dummy_seq).squeeze().tolist()
        self.assertEqual(len(out), 15)

    def test_06_datasets_page_and_api_http_200(self):
        res_page = self.client.get('/datasets/')
        self.assertEqual(res_page.status_code, 200)
        self.assertContains(res_page, "Dataset Catalog")

        res_api = self.client.get('/api/datasets/')
        self.assertEqual(res_api.status_code, 200)
        data = res_api.json()
        self.assertEqual(data.get('status'), 'OK')

        res_exp = self.client.get('/api/experiments/')
        self.assertEqual(res_exp.status_code, 200)

    def test_07_optimization_comparison_artifact_integrity(self):
        comp_summary = Path('reports/nsga2_comparison/comparison_summary.json')
        self.assertTrue(comp_summary.exists())
        summary = json.loads(comp_summary.read_text(encoding='utf-8'))
        self.assertIn('method_a_current_state', summary)
        self.assertIn('method_b_prediction_guided', summary)
        self.assertIn('relative_comparison', summary)
        self.assertGreater(summary['total_scenarios_evaluated'], 0)

    def test_08_scalability_benchmark_artifact_integrity(self):
        scal_csv = Path('reports/scalability/scalability_results.csv')
        self.assertTrue(scal_csv.exists())
        df = pd.read_csv(scal_csv)
        self.assertGreaterEqual(len(df), 6)
        self.assertIn(1000000, df['row_count'].values)
