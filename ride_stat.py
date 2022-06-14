#!/usr/bin/env python
from pathlib import Path
import pandas as pd
from parse_fit import parse

data_dir = Path.home() / Path('gdrive/Recreation/bike/fit-data/')

parse(data_dir)

pd.set_option('display.precision', 2)

results = []
files = list(data_dir.glob('*.csv'))
files.sort()

for fp in files:
    rec = {}    
    df = pd.read_csv(fp)
    dfp = df.query('power > 0').mean()
    rec['file'] = fp.stem
    rec['miles'] = df.distance.max() * 0.6214 / 1000
    rec['bat_Wh'] = df.batCurrCap1.max() - df.batCurrCap1.min()
    rec['me_Wh'] = df.power.sum() / 3600.0
    rec['mi/kWh'] = rec['miles'] / (rec['bat_Wh']/1000)
    rec['power'] = dfp.power
    rec['motor_power'] = dfp.motor_power
    rec['support'] = df.motor_power.sum() / df.power.sum()
    rec['cadence'] =df.query('cadence >=60').mean()['cadence']

    # calc elevation gained, and elevation gained per mile.
    alt_chg = df.altitude.diff()
    rec['elev_gained'] = alt_chg[alt_chg > 0].sum() * 3.28
    rec['elev_per_mi'] = rec['elev_gained'] / rec['miles']

    # hours moving
    rec['hours'] = len(df.query('speed > 0')) / 3600.0
    results.append(rec)

df_results = pd.DataFrame(results)
print(df_results)
print('\nAverage Results:')
print(df_results.mean())
df_results.to_pickle('rides.pkl')
