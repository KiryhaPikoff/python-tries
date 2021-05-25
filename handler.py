import pandas as pd
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option("display.precision", 2)

import numpy as np


played_race_s = 'played_race'
games_s = 'games'
winrate_s = 'winrate'
mmr_s = 'mmr'

table = pd.read_csv('sc2-gamer-table')

groups = table.groupby(played_race_s)\
    .agg({
        winrate_s: ['count', 'std', 'min', 'mean', 'median', 'max'],
        games_s: ['std', 'min', 'median', 'max'],
        mmr_s: ['std', 'min', 'median', 'mean']
    })

print(groups)

races_count=3
max_mmr = 10000
default_mmr = 5000
max_winrate = 100
min_games = 15


played_race = table[played_race_s]
games = table[games_s]
winrate = table[winrate_s]
mmr = table[mmr_s]

played_race.update(played_race.replace(np.nan, -1.0))
table.loc[(table[played_race_s] > races_count), played_race_s] = -1

games.update(games.replace(np.nan, games.median()))

mmr.update(mmr.replace(np.nan, mmr.median()))
table.loc[(table[mmr_s] > max_mmr), mmr_s] = default_mmr

table = table[winrate.notna()]
table = table[winrate <= max_winrate]

table = table[games >= min_games]

groups = table.groupby(played_race_s)\
    .agg({
        winrate_s: ['count', 'std', 'min', 'mean', 'median', 'max'],
        games_s: ['std', 'min', 'median', 'max'],
        mmr_s: ['std', 'min', 'median', 'mean']
    })

print(groups)

table.to_csv('sc2-norm', index=False)
