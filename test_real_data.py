import json
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from train_real_data import build_examples

ROOT = Path(__file__).resolve().parent

class RealDataChecks(unittest.TestCase):
    def test_gaps_are_not_bridged(self):
        df = pd.read_csv(ROOT/'data/bangladesh_water_level.csv',parse_dates=['date'])
        examples, missing = build_examples(df)
        self.assertEqual((len(df),len(examples),missing),(80,67,11))
        dates = set(df.date)
        for date in examples.index:
            self.assertTrue(all(date+pd.Timedelta(days=offset) in dates for offset in [-2,-1,0,1]))

    def test_chronological_split(self):
        d = json.loads((ROOT/'real-data.json').read_text())
        self.assertLess(d['split']['train']['last_target'],d['split']['validation']['first_target'])
        self.assertLess(d['split']['validation']['last_target'],d['split']['test']['first_target'])
        self.assertEqual(d['split']['test']['samples'],14)

    def test_exported_model_and_metrics(self):
        d = json.loads((ROOT/'real-data.json').read_text())
        errors = []
        for row in d['test_predictions']:
            pred = d['model']['intercept']+sum(c*row[k] for c,k in zip(d['model']['coefficients'],d['feature_order']))
            self.assertAlmostEqual(pred,row['predicted_m'],places=10)
            self.assertEqual(pd.Timestamp(row['target_date'])-pd.Timestamp(row['input_date']),pd.Timedelta(days=1))
            errors.append(abs(pred-row['actual_m']))
        self.assertAlmostEqual(float(np.mean(errors)),d['metrics']['ridge']['mae_m'],places=10)
        self.assertGreater(d['metrics']['ridge']['mae_m'],d['metrics']['persistence']['mae_m'])

if __name__ == '__main__':
    unittest.main()
