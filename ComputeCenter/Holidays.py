from scipy.optimize import minimize

from data import series
from data import dates
from data import holidays

def series_filter(series, dates, holidays):
    formatDates = []
    resultSeries = []
    resultHolidaysSeries = []
    for d in dates:
        formatDates.append(d[:5])
    for i in range(len(series)):
        if len(set([formatDates[i]]) & set(holidays)) != 0:
            resultHolidaysSeries.append(series[i])
        else:
            resultSeries.append(series[i])
    return resultSeries,resultHolidaysSeries
def series_filter_with_replace(series, dates, holidays):
    formatDates = []
    resultSeries = []
    for d in dates:
        formatDates.append(d[:5])
    for i in range(len(series)):
        if len(set([formatDates[i]]) & set(holidays)) == 0:
            resultSeries.append(series[i])
        else:
            if i != 0 & i != len(series):
                resultSeries.append((series[i-1]+series[i+1])/2)
            else:
                resultSeries.append(series[i])
    return resultSeries