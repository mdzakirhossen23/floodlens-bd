import unittest
from risk_model import score, PRESETS
from evaluate import metrics

class ModelChecks(unittest.TestCase):
    def test_known_browser_scenarios(self):
        self.assertEqual(score(PRESETS['flood'])['flood'], 97)
        self.assertEqual(score(PRESETS['drought'])['drought'], 83)
        self.assertEqual(score(PRESETS['baseline'])['band'], 'LOW')

    def test_drought_explanation_excludes_flood_only_inputs(self):
        result = score(PRESETS['drought'])
        self.assertEqual(result['displayed_type'], 'drought')
        self.assertEqual(set(result['contributions']), {'soil', 'rainfall', 'forecast', 'elevation'})

    def test_expected_direction(self):
        dry = list(PRESETS['drought'])
        wetter = dry.copy()
        wetter[2] += 20
        self.assertLess(score(wetter)['drought'], score(dry)['drought'])
        flood = list(PRESETS['flood'])
        flood[1] -= 3
        self.assertLess(score(flood)['flood'], score(PRESETS['flood'])['flood'])

    def test_baseline_and_validation(self):
        self.assertAlmostEqual(metrics()['always_positive_accuracy'], .8185)
        self.assertLess(metrics()['specificity'], .21)
        self.assertEqual(score(PRESETS['baseline'])['validation'], 'Not validated')

    def test_invalid_values(self):
        for values in [(0,)*5, (0,0,0,0,0,0), (float('nan'),0,50,0,1,0)]:
            with self.assertRaises(ValueError):
                score(values)

if __name__ == '__main__':
    unittest.main()
