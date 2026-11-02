# Observed Bangladesh gauge data

Source: https://reproducibility.worldbank.org/catalog/374
DOI: https://doi.org/10.60572/4vhs-y802
Archive: RR_BGD_2025_385v2.zip, downloaded November 3, 2026 (Bangladesh time).

Original archive path: `Replication package/data/bangladesh/round3/DataSets/Raw/water_level.dta`.
The source catalog identifies these observations as FFWC/BWDB data, publicly included in the package. The source's `r 01 graph water level.do` identifies the Bangladesh series as "Bahurabad station measured water level." This integration preserves that spelling rather than inferring an unverified gauge identifier. The file contains only `date` and `water_level` (label: Water level meters). Gauge datum and official danger levels are not supplied, so this project does not infer flood-depth or danger-level classes from these values.

`water_level.dta` is retained unchanged. `bangladesh_water_level.csv` is a direct conversion using `pandas.read_stata`, followed by `to_csv(index=False)`. The archive's analysis script is preserved as `source_analysis.do` and its license as `WORLD_BANK_LICENSE.txt`. The original household survey datasets are not used or redistributed here.

There are 80 observations over June 15–September 13, 2024. Eleven calendar dates are missing. No readings have been generated or interpolated. The model requires t−2, t−1, t and t+1 to be present, yielding 67 one-step forecasting examples. It uses gauge level and historical changes only, not six-input scenario features or future observed rainfall. The final 14 chronological examples are held out. A frozen fitted model consumes each test day's actually available past readings, making this a rolling one-step evaluation, not an unobserved multi-day rollout.

The ridge model is slightly worse than persistence in MAE on this specific test block. Do not market it as an accuracy improvement. The test contains the late-season recession and is not a held-out set of flood events. Other gauges, flood peaks, seasons, rainfall and drought outcomes remain unvalidated.

FFWC direct API access returned "Access Denied: Invalid Security Header" during integration. No security restriction was bypassed; the publicly downloadable World Bank archive was used instead.
