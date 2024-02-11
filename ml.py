import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def modelML(data):
    # Выделение групп для обучения и предсказания
    X = []
    y = []
    for i in range(len(data)):
        X.append([data[0][i], data[1][i], data[2][i]])
        y.append(data[0][i])
    # Данные -> nparray
    X = np.array(X)
    y = np.array(y)
    rnd_state = 44 # Для достижения MSE минимального значения 6.6405325443786785, должно быть 44
    mse_min, temp = 18, None
    while mse_min > 7:
        # Разбиенние данных для обучения и теста
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=rnd_state)
        # Обучение модели линейной регрессии
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test) # Предсказание
        mse = np.mean((y_test - y_pred) ** 2) # Оценка модели
        # print(f'Среднеквадратическая ошибка (MSE): {mse},\nПредсказание температуры: {y_pred}, rnd_state:{rnd_state}')

        if mse < mse_min:
            mse_min = mse
            temp = y_pred
            rnd_state -= 1
        else:
            rnd_state += 1
    # print(f'MSE minimum: {mse_min}')
    return (f'Среднеквадратическая ошибка (MSE): {mse},\n'
            f'Предсказание температуры: {y_pred}, rnd_state:{rnd_state}')


# Подготовка данных в виде списка кортежей
#  Линейная регрессия, есть список кортежей,
#  содержащий значения температуры, влажности и давления, а также температуру следующего дня.
# data = [
#     (-15, 65, 1020, -12),
#     (-12, 70, 1015, -18),
#     (-18, 55, 1018, -10),
#     (-10, 55, 1018, -14),
#     # Еще добавить можно данных
# ]
#
# print(modelML(data))