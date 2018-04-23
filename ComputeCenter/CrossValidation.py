"""

Модуль CrossValidation.py отвечает за функцию потерь (timeseriesCVcore), при вычислении которой в свою очередь
используется кросс-валидация.
Модуль использует следующие библиотеки:
- numpy - для вычисления среднего значения массива
- sklearn - метод mean_squared_error этой библиотеки вычисляет среднее квадратичное отклонение от значений
  двух массивов, а конструктор TimeSeriesSplit позволяет реализовать кросс-валидацию, для этого нужно передать
  количество разбиений, а затем взять созданный объект и вызвать метод split, передав массив данных, на которых
  кросс-валидация будет проводится.
и модуль:
- data.py - содержит значения временного ряда (series), а так же параметры: количество прогнозов, которое
  необходимо сделать (n_predicts), число разделений кросс-валидации (n_splits) и сезонность (slen)
"""
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error
from sklearn.model_selection import TimeSeriesSplit
from HoltWinters import triple_exponential_smoothing

from data import series
from data import slen


def set_global_n(x):
    global n_splits_global
    n_splits_global = x


def get_global_n():
    return n_splits_global


# Вернет вектор отклонений "Ошибку"
def timeseriesCVcore(x):
    """

    timeseriesCVcore(x)
    Принимает на вход вектор x - тип list.
    Вектор х содержит параметры альфа, бета и гамма.
    Используя данные и параметры, подгружаемые из data.py, производит кросс-валидацию и возвращает
    среднюю ошибку по вектору ошибок. Результат представляет собой число - тип float.
    """
    errors = []
    values = series
    alpha, beta, gamma = x
    #n_splits - число разделений в кросс-валидации
    #tsvc - специальный объект, способный разбивать переданные ему данные, в соответствии с ранее переданным n_splits
    
    tsvc = TimeSeriesSplit(get_global_n())

    #train и test будут каждый раз разными, и с каждым следующим шагом новый train = cтарый train + test
    for train, test in tsvc.split(values):
        train_values = []
        test_values = []
        for i in train:
            train_values.append(values[i])
        for i in test:
            test_values.append(values[i])
        #Берем последнюю часть данных, по количеству элементов в test
        predictions = triple_exponential_smoothing(train_values, slen, alpha, beta, gamma, len(test_values))[-len(test_values):]
        #Вычисляем "ошибку"
        error = mean_squared_error(predictions, test_values)
        errors.append(error)
    return np.mean(np.array(errors))
