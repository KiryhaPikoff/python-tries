# import mkl
# mkl.verbose(1)

from pandas import *

import numpy as np

count = 500
noise_level = 3
max_noise_level=100
very_big_noise=100_000_000

def mask(size):
    digits = abs(np.random.random_integers(low=0, high=max_noise_level, size=size))
    return list(map(lambda x: 0 if x < noise_level else 1, digits))

sex = abs(
    np.random.random_integers(low=1, high=2, size=count)
) * mask(count)
sex = map(lambda x: np.nan if x == 0 else x, sex)
sex = map(lambda x,y:x*y,sex,mask(count))
sex = list(map(lambda x: int((np.random.random(1) * max_noise_level) * very_big_noise) if x == 0 else x, sex))

salary = abs(
    np.random.normal(loc=30_000, scale=10_000, size=(count))
) * mask(count)
salary = map(lambda x: np.nan if x == 0 else x, salary)
salary = map(lambda x,y:x*y,salary,mask(count))
salary = list(map(lambda x: int((np.random.random(1) * max_noise_level) * very_big_noise) if x == 0 else x, salary))

order = abs(
    np.random.gamma(shape=10, scale=300, size=(count))
) * mask(count)
order = map(lambda x: np.nan if x == 0 else x, order)
order = map(lambda x,y:x*y,order,mask(count))
order = list(map(lambda x: int((np.random.random(1) * max_noise_level) * very_big_noise) if x == 0 else x, order))

month = abs(
    np.random.random_integers(low=0, high=11, size=count)
) * mask(count)
month = map(lambda x: np.nan if x == 0 else x, month)
month = map(lambda x,y:x*y,month,mask(count))
month = list(map(lambda x: int((np.random.random(1) * max_noise_level) * very_big_noise) if x == 0 else x, month))


table = DataFrame({"sex": sex, "salary": salary, "order": order, "month": month})
print(table)

table.to_csv('pikoff_table', index=False)

