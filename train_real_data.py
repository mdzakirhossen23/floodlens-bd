"""Reproduce a small, chronological 24h river-level backtest from public observations."""
from pathlib import Path
import hashlib
import json
import platform
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent

def build_examples(df):
    df = df.sort_values('date').set_index('date')
    if df.index.has_duplicates:
        raise ValueError('Duplicate dates')
    if not np.isfinite(df.water_level).all():
        raise ValueError('Missing or non-finite readings')
    # Reindex exposes missing calendar days. Never interpolate through gaps.
    daily = df.reindex(pd.date_range(df.index.min(), df.index.max(), freq='D')).water_level
    frame = pd.DataFrame({'level_t': daily, 'change_1d': daily.diff(),
                          'change_2d': daily-daily.shift(2),
                          'target': daily.shift(-1)})
    frame['target_date'] = frame.index + pd.Timedelta(days=1)
    return frame.dropna(), int(daily.isna().sum())

def evaluate(actual, predicted):
    return {'mae_m': float(mean_absolute_error(actual, predicted)),
            'rmse_m': float(mean_squared_error(actual, predicted)**.5)}

def main():
    csv = ROOT/'data/bangladesh_water_level.csv'
    df = pd.read_csv(csv, parse_dates=['date'])
    examples, missing = build_examples(df)
    n = len(examples)
    a, b = int(n*.6), int(n*.8)
    train, valid, test = examples.iloc[:a], examples.iloc[a:b], examples.iloc[b:]
    features = ['level_t','change_1d','change_2d']
    trials = []
    for alpha in [.01,.1,1.,10.,100.]:
        candidate = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
        candidate.fit(train[features],train.target)
        trials.append((evaluate(valid.target,candidate.predict(valid[features]))['mae_m'],alpha))
    _, alpha = min(trials)
    # Refit on train+validation only; the test targets never enter training.
    fit = examples.iloc[:b]
    model = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
    model.fit(fit[features],fit.target)
    pred = model.predict(test[features])
    results = {'ridge': evaluate(test.target,pred),
               'persistence': evaluate(test.target,test.level_t),
               'linear_trend': evaluate(test.target,test.level_t+test.change_1d)}
    scaler, reg = model.steps[0][1], model.steps[1][1]
    coef = reg.coef_/scaler.scale_
    intercept = float(reg.intercept_-np.dot(coef,scaler.mean_))
    def period(part):
        return {'samples':len(part),'first_target':str(part.target_date.iloc[0].date()),
                'last_target':str(part.target_date.iloc[-1].date())}
    payload = {
        'source':'FFWC/BWDB observations redistributed in World Bank RR_BGD_2025_385v2',
        'source_url':'https://reproducibility.worldbank.org/catalog/374',
        'station':'Bahurabad (station name as written in source analysis script)',
        'observation_count':len(df),'first_date':str(df.date.min().date()),
        'last_date':str(df.date.max().date()),'missing_calendar_days':missing,
        'valid_examples':n,'forecast_horizon_hours':24,
        'task':'Next-day gauge-level regression, not flood/drought classification',
        'split':{'train':period(train),'validation':period(valid),'test':period(test)},
        'alpha':alpha,'metrics':results,'feature_order':features,
        'model':{'type':'Ridge regression','intercept':intercept,'coefficients':coef.tolist()},
        'sha256_csv':hashlib.sha256(csv.read_bytes()).hexdigest(),
        'versions':{'python':platform.python_version(),'numpy':np.__version__,
                    'pandas':pd.__version__,'scikit_learn':sklearn.__version__},
        'observations':[{'date':str(r.date.date()),'water_level_m':float(r.water_level)} for r in df.itertuples()],
        'test_predictions':[{'input_date':str(date.date()),'target_date':str(row.target_date.date()),
                             'level_t':float(row.level_t),'change_1d':float(row.change_1d),
                             'change_2d':float(row.change_2d),'actual_m':float(row.target),
                             'predicted_m':float(p),'persistence_m':float(row.level_t),
                             'trend_m':float(row.level_t+row.change_1d)}
                            for (date,row),p in zip(test.iterrows(),pred)]}
    target = ROOT/'real-data.json'
    target.write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in payload.items() if k not in ['observations','test_predictions']},indent=2))

if __name__ == '__main__':
    main()
