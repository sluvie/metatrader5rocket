import numpy as np
import pandas as pd
from scipy.signal import lfilter, lfilter_zi
from numba import jit


# SMA on Array
@jit
def SMAonArray(x, ma_period):
    x[np.isnan(x)] = 0
    y = np.empty_like(x)
    y[:ma_period-1] = np.nan
    y[ma_period-1] = np.sum(x[:ma_period])
    for i in range(ma_period, len(x)):
        y[i] = y[i-1] + x[i] - x[i-ma_period]
    return y/ma_period
    

# EMA on Array
@jit
def EMAonArray(x, alpha):
    x[np.isnan(x)] = 0
    y = np.empty_like(x)
    y[0] = x[0]
    for i in range(1,len(x)):
        y[i] = alpha*x[i] + (1-alpha)*y[i-1]
    return y


def MAonArray(a, ma_period, ma_method):
    if ma_method == 'SMA':
        y = SMAonArray(a, ma_period)
    elif ma_method == 'EMA':
        y = EMAonArray(a, 2/(ma_period+1))
    elif ma_method == 'SMMA':
        y = EMAonArray(a, 1/ma_period)
    elif ma_method == 'LWMA':
        h = np.arange(ma_period, 0, -1)*2/ma_period/(ma_period+1)
        y = lfilter(h, 1, a)
        y[:ma_period-1] = np.nan
    return y


def MAonSeries(s, ma_period, ma_method):
    return pd.Series(MAonArray(s.values, ma_period, ma_method), index=s.index)


# iMA
def iMA(df, ma_period, ma_shift=0, ma_method='SMA', applied_price='Close'):
    return MAonSeries(df[applied_price], ma_period, ma_method).shift(ma_shift)

# iRSI
def iRSI(df, ma_period, applied_price='Close'):
    diff = df[applied_price].diff()
    positive = MAonSeries(diff.clip(lower=0), ma_period, 'SMMA')
    negative = MAonSeries(diff.clip(upper=0), ma_period, 'SMMA')
    return 100-100/(1-positive/negative)