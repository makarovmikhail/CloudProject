"""

Модуль HoltWinters.py отвечает за реализацию метода Хольта-Винтерса.
"""

#Вычисление начального значения тренда
def initial_trend(series, slen):
    """

    initial_trend(series, slen)
    Вспомогательная функция.
    Принимает на вход параметры:
        - series - значения временного ряда
        - slen - сезонность
    Возвращает начальное значение тренда - число - тип float.
    """
    sum = 0.0
    for i in range(slen):
        sum+= float(series[i+slen] - series[i]) / slen
    return sum / slen

#Вычисление начальных сезонных компонент
def initial_seasonal_components(series, slen):
    """

    initial_seasonal_components(series, slen)
    Вспомогательная функция.
    Принимает на вход параметры:
        - series - значения временного ряда
        - slen - сезонность
    Возвращает начальные значения сезонных компонент - тип dict.
    """
    seasonals = {}
    season_averages = []
    n_seasons = int(len(series)/slen)
    for j in range(n_seasons):
        season_averages.append(sum(series[slen*j:slen*j+slen])/float(slen))
    for i in range(slen):
        sum_of_vals_over_avg = 0.0
        for j in range(n_seasons):
            sum_of_vals_over_avg += series[slen*j+i]-season_averages[j]
        seasonals[i] = sum_of_vals_over_avg/n_seasons
    return seasonals

#Непосредственно метод Хольта-Винтерса (тройное экспоненциальное сглаживание)
def triple_exponential_smoothing(series, slen, alpha, beta, gamma, n_preds):
    """

    triple_exponential_smoothing(series, slen, alpha, beta, gamma, n_preds)
    Реализует метод Хольта-Винтерса.
    Принимает на вход параметры:
        - series - значения временного ряда
        - slen - сезонность
        - alpha - параметр метода
        - beta - параметр метода
        - gamma - параметр метода
        - n_preds - количество прогнозов (сколько значений нужно предсказать)
    Возвращает массив элементов - в количестве длинны временного ряда + количество прогнозов - тип list.
    """
    result = []
    seasonals = initial_seasonal_components(series, slen)
    for i in range(len(series)+n_preds):
        if i == 0:
            smooth = series[0]
            trend = initial_trend(series, slen)
            result.append(series[0])
            continue
        if i >= len(series):
            m = i - len(series)+1
            result.append((smooth+m*trend)+seasonals[i%slen])
        else:
            val = series[i]
            last_smooth, smooth = smooth, alpha*(val-seasonals[i%slen])+(1-alpha)*(smooth+trend)
            trend = beta * (smooth-last_smooth) + (1-beta)*trend
            seasonals[i%slen] = gamma*(val-smooth)+(1-gamma)*seasonals[i%slen]
            result.append(smooth+trend+seasonals[i%slen])
    return result
