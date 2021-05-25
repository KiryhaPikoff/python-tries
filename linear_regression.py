import pandas as pd
from sklearn.linear_model import LinearRegression

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option("display.precision", 2)

import numpy as np

played_race_s = 'played_race'
games_s = 'games'
winrate_s = 'winrate'
mmr_s = 'mmr'

table = pd.read_csv('sc2-norm')

x = np.array(table[games_s]).reshape((-1, 1))
y = np.array(table[winrate_s])

model = LinearRegression()
model.fit(x, y)
r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)