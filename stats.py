import numpy as np
import pandas as pd
from datetime import datetime
import datetime

def correlation(series_x, series_ys, 
				start_date = None, end_date = None, 
				length = None, 
				rolling_mean = None, 
				delay_x = None, 
				method = 'pearson'):
	"""
	Computes the correlation coefficient between series_x 
	and series_y filtered by dates or length in years
	If an integer is passed into rolling_mean, data will be
	denoised using a simple moving average with window length
	rolling_mean

	Method can be pearson (default), kendall or spearman
	IMPORTANT: 
	1) series_x and series_y must have datetime index
	2) series_x and series_y must have the same length
	"""
	correlation_data = pd.DataFrame()
	if length is None:
		if start_date is None:
				start_date = series_x.index[0]
		if end_date is None:
			end_date = series_x.index[-1]
	elif length is not None:
		start_date = series_x.index[-1] - datetime.timedelta(days=length*365)
		end_date = series_x.index[-1]
	correlation_data[series_x.name] = series_x.loc[start_date:end_date]
	for i, series_y in enumerate(series_ys):
		correlation_data[series_y.name + ' ' +str(i)] = series_y.loc[start_date:end_date]
	if rolling_mean is not None:
		correlation_data = correlation_data.rolling(center=False, window = rolling_mean).mean()
	if delay_x is not None:
		correlation_data[series_x.name] = correlation_data[series_x.name].shift(delay_x)
	return correlation_data.corr(method=method)

def slow_stochastic(close, high, low, window=14):
	"""
	Computes the slow stochastic indicator for the past (window)
	Default window is 14
	"""
	l = low.rolling(center=False, window=window).min()
	h = high.rolling(center=False, window=window).max()
	return (close - l) / (h - l)