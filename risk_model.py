"""Python reference for FloodLens browser formulas; illustrative, not trained/validated."""
import argparse
import json
import math

FIELDS = ('rainfall', 'river', 'soil', 'forecast', 'elevation', 'drainage')
BOUNDS = ((0, 300), (0, 10), (5, 100), (0, 350), (1, 60), (0, 100))
PRESETS = {
    'flood': (178, 6.4, 82, 210, 18, 45),
    'drought': (12, .6, 19, 18, 34, 25),
    'baseline': (60, .7, 80, 80, 35, 20),
}

def score(values):
    """Return scenario scores and exact additive logit contributions."""
    v = dict(zip(FIELDS, values))
    if len(values) != 6 or any(not math.isfinite(x) or not lo <= x <= hi
                               for x, (lo, hi) in zip(values, BOUNDS)):
        raise ValueError('Expected six finite inputs within browser slider bounds')
    flood = dict(zip(FIELDS, (
        v['rainfall']/300*2.25, v['river']/10*2.65, v['soil']/100*1.35,
        v['forecast']/350*1.75, (1-min(v['elevation'], 60)/60)*1.15,
        v['drainage']/100*1.05)))
    drought = {'soil': (1-v['soil']/100)*2.3,
               'rainfall': (1-v['rainfall']/300)*1.25,
               'forecast': (1-v['forecast']/350)*1.4,
               'elevation': v['elevation']/60*.35}
    def scaled(intercept, terms):
        # Match JavaScript Math.round for these nonnegative scores.
        return math.floor(100/(1+math.exp(-(intercept+sum(terms.values()))))+.5)
    f, d = scaled(-3.1, flood), scaled(-3, drought)
    kind = 'drought' if d > f else 'flood'
    maximum = max(f, d)
    return {'flood': f, 'drought': d, 'displayed_type': kind,
            'band': 'HIGH' if maximum >= 75 else 'MODERATE' if maximum >= 45 else 'LOW',
            'validation': 'Not validated',
            'contributions': drought if kind == 'drought' else flood}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preset', choices=PRESETS, default='drought')
    parser.add_argument('--values', type=float, nargs=6, metavar=FIELDS)
    args = parser.parse_args()
    print(json.dumps(score(args.values or PRESETS[args.preset]), indent=2))
