import math

import numpy as np
from geneticalgorithm import geneticalgorithm as ga

# 16. На языке Python разработайте скрипт, который с помощью генетического алгоритма
# и полного перебора решает следующую задачу. Дано N наименований продуктов, для каждого
# из которых известно m характеристик. Необходимо получить самый дешевый рацион из k наименований,
# удовлетворяющий заданным медицинским нормам для каждой из m характеристик.

products = [
    {
        "name": "Авокадо",
        "proteins": 1.9,
        "fats": 23.5,
        "carbohydrates": 6.8,
        "kcal": 223,
        "price": 52.25
    },
    {
        "name": "Баклажан",
        "proteins": 0.6,
        "fats": 0.1,
        "carbohydrates": 5.5,
        "kcal": 24,
        "price": 35.5
    },
    {
        "name": "Кабачок",
        "proteins": 0.6,
        "fats": 0.3,
        "carbohydrates": 33,
        "kcal": 27,
        "price": 35.375
    },
    {
        "name": "Картофель",
        "proteins": 2,
        "fats": 0.3,
        "carbohydrates": 19.7,
        "kcal": 83,
        "price": 15.25
    },
    {
        "name": "Йогурт",
        "proteins": 4,
        "fats": 2.7,
        "carbohydrates": 6.8,
        "kcal": 75,
        "price": 35
    },
    {
        "name": "Капуста брюссельская",
        "proteins": 12,
        "fats": 0.1,
        "carbohydrates": 7,
        "kcal": 12,
        "price": 92
    }
]

dim = len(products)

maxprice = 130

norm = {
    "proteins": 34,
    "fats": 25,
    "carbohydrates": 60,
    "kcal": 600,
}
kmax = 3


def f(X):
    price = 0
    proteins = 0
    fats = 0
    carbohydrates = 0
    kcal = 0
    k = 0

    for i in range(0, dim):
        if (X[i]):
            fooddata = products[i]
            price += fooddata.get("price")
            proteins += fooddata.get("proteins")
            fats += fooddata.get("fats")
            carbohydrates += fooddata.get("carbohydrates")
            kcal += fooddata.get("kcal")
            k = k + 1

    # находим квадрат разности между параметрами
    psqr = (proteins - norm.get("proteins")) ** 2
    fsqr = (fats - norm.get("fats")) ** 2
    csqr = (carbohydrates - norm.get("carbohydrates")) ** 2
    ksqr = (kcal - norm.get("kcal")) ** 2

    # находим корень суммы квадратов разницы - расстояние
    diff = np.sqrt(psqr + fsqr + csqr + ksqr)

    if (price > maxprice):
        diff += 100000

    if (k != kmax):
        diff += 100000

    return diff


def ppx(X):
  price = 0
  proteins = 0
  fats = 0
  carbohydrates = 0
  kcal = 0
  k = 0

  for i in range(0, dim):
    if (str(X[i]) == '1'):
      fooddata = products[i]
      price += fooddata.get("price")
      proteins += fooddata.get("proteins")
      fats += fooddata.get("fats")
      carbohydrates += fooddata.get("carbohydrates")
      kcal += fooddata.get("kcal")
      k = k + 1

  # находим квадрат разности между параметрами
  psqr = (proteins - norm.get("proteins")) ** 2
  fsqr = (fats - norm.get("fats")) ** 2
  csqr = (carbohydrates - norm.get("carbohydrates")) ** 2
  ksqr = (kcal - norm.get("kcal")) ** 2

  # находим корень суммы квадратов разницы - расстояние
  diff = np.sqrt(psqr + fsqr + csqr + ksqr)

  if (price > maxprice):
    diff += 100000

  if (k != kmax):
    diff += 100000

  return diff


algorithm_param = {
    'max_num_iteration': 100, \
    'population_size': 100, \
    'mutation_probability': 0.1, \
    'elit_ratio': 0.2, \
    'crossover_probability': 0.5, \
    'parents_portion': 0.3, \
    'crossover_type': 'uniform', \
    'max_iteration_without_improv': 20
}

model = ga(function=f, dimension=dim, variable_type='bool', algorithm_parameters=algorithm_param)

model.run()

price = 0
proteins = 0
fats = 0
carbohydrates = 0
kcal = 0
print("\nЛучший рацион за цену менее " + str(maxprice))
for i in range(0, dim):
    if (model.best_variable[i]):
        fooddata = products[i]
        print(fooddata.get("name"))
        price += fooddata.get("price")
        proteins += fooddata.get("proteins")
        fats += fooddata.get("fats")
        carbohydrates += fooddata.get("carbohydrates")
        kcal += fooddata.get("kcal")

print("По цене: " + str(price) + "; Макс. цена: " + str(maxprice))
print("Белки: " + str(proteins) + "; Норма: " + str(norm.get("proteins")))
print("Жиры: " + str(fats) + "; Норма: " + str(norm.get("fats")))
print("Углеводы: " + str(carbohydrates) + "; Норма: " + str(norm.get("carbohydrates")))
print("Калории: " + str(kcal) + "; Норма: " + str(norm.get("kcal")))

print('ПОЛНЫЙ ПЕРЕБОР:')

chroms = list()
for chrom in range(0, 2 ** len(products) - 1):
    chrBin = str(bin(chrom))
    chrBin = chrBin[2:]
    if (chrBin.count('1') == 3):
      while len(chrBin) < len(products):
          chrBin = '0' + chrBin
      chroms.append(chrBin)

dist = {}

for chrom in chroms:
  dist[chrom] = ppx(chrom)

min_ch = 'none'
min_diff = 10000000

for chrom in dist:
  if dist[chrom] < min_diff:
    min_ch = chrom
    min_diff = dist[chrom]

price = 0
proteins = 0
fats = 0
carbohydrates = 0
kcal = 0

print("\nЛучший рацион за цену менее " + str(maxprice))
for i in range(0, dim):
  if (min_ch[i] == '1'):
    fooddata = products[i]
    print(fooddata.get("name"))
    price += fooddata.get("price")
    proteins += fooddata.get("proteins")
    fats += fooddata.get("fats")
    carbohydrates += fooddata.get("carbohydrates")
    kcal += fooddata.get("kcal")

print("По цене: " + str(price) + "; Макс. цена: " + str(maxprice))
print("Белки: " + str(proteins) + "; Норма: " + str(norm.get("proteins")))
print("Жиры: " + str(fats) + "; Норма: " + str(norm.get("fats")))
print("Углеводы: " + str(carbohydrates) + "; Норма: " + str(norm.get("carbohydrates")))
print("Калории: " + str(kcal) + "; Норма: " + str(norm.get("kcal")))
