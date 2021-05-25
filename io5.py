import decimal
import math
import random

begX: decimal
endX: decimal

def f(x: float):
    try:
        val = x**2 + 3*math.exp(-0.45*x)
    except OverflowError:
        val = float('inf')
    return val

def p1(x: float):
    decimal.getcontext().prec = 10
    v = math.exp(-0.45*x)
    return 2*x-1.35*v

def p2(x: float):
    decimal.getcontext().prec = 10
    return 0.6075*math.exp(-0.45*x)

def Swenn():
    print("Метод Свенна:")
    h = float(input("Введите величину шага h > 0 ->"))
    k = 0
    x0 = float(input("Введите начальное приближение ->"))
    print("Начальное приближение = " + str(x0))
    a = x0 - h
    b = x0 + h

    # максимум, ф-ия не унимодальна
    while (f(x0 - h) <= f(x0) and f(x0) >= f(x0 + h)):
        x0 = float(input("Введите новое начальное приближение ->"))
        print("Новое начальное приближение = " + str(x0))

    # минимум
    if not (f(x0 - h) >= f(x0) and f(x0) <= f(x0 + h)):

        if (f(x0 - h) >= f(x0) and f(x0) >= f(x0 + h)):
            print("Функция убывает, двигаемся вправо -> " + str(x0))
            delta = h
            a = x0
            x = x0 + h
            k = 1

        if (f(x0 - h)<= f(x0) and f(x0) <= f(x0 + h)):
            print("Функция возрастает, двигаемся влево <- " + str(x0))
            delta = -h
            b = x0
            x = x0 - h
            k = 1
        xnext = x + math.pow(2, k) * delta

        while (f(xnext) < f(x)):
            print("Значение меньше предыдущего " + str(xnext) + " " + str(f(xnext)))
            if (f(xnext) < f(x) and delta == h):
                a = xnext
            if (f(xnext) < f(x) and delta == -h):
                b = xnext
            k += 1
            x = xnext
            xnext = x + math.pow(2, k) * delta
        print("Значение не меньше предыдущего " + str(xnext) + " " + str(f(xnext)))

        if (delta == h):
            b = xnext
        if (delta == -h):
            a = xnext

    global begX
    begX = a
    global endX
    endX = b
    print("Начальное приближение методом Свенна: begX = " + str(begX) + ", endX =" + str(endX))

def RavnSearch():
    print("Метод равномерного поиска:")
    Xmin = begX
    Ymin = f(begX)
    N = int(input("Введите количество промежутков -> "))
    for i in range(N):
        i += 1
        x = begX + i * (abs(endX) - begX) / (N + 1)
        y = f(x)
        if y < Ymin:
            Ymin = y
            Xmin = x
        print(str(i) + ") x = " + str(x) + ", y = " + str(y))

    print("Решение методом равномерного поиска: x = " + str(Xmin) + " y =" + str(Ymin))
    return Xmin

def Newton():
    print("Метод Ньютона")
    i = 1
    x0 = begX
    print(str(i) + ") x = " + str(x0) + ", y = " + str(f(x0)))
    x1 = begX - p1(x0) / p2(x0)

    while (abs(x1 - x0) > eps):
        x0 = x1
        i += 1
        print(str(i) + ") x = " + str(x0) + ", y = " + str(f(x0)))
        x1 = x0 - p1(x0) / p2(x0)

    print("Решение методом Ньютона: x = " + str(x0) + ", y = " + str(f(x0)))
    return x0


eps = float(input("Введите точность: "))

Swenn()
#resultX = Newton()
resultX = RavnSearch()
#resultX = Gold()

print("Первая производная f'(x) = " + str(p1(resultX)))
print("Вторая производная f''(x) = " + str(p2(resultX)))


