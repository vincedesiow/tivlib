import numpy as np
from tivlib.preprocess import get_ioe0
from tivlib.stats import slow_stochastic
from tivlib.utils import show_pnl
import matplotlib.pyplot as plt

def slow_stochastic_strategy(window=5, 
							 lower=0.2,
							 upper=0.8,
							 out_sample_start=None):
	ioe159 = get_ioe0()
	ss = slow_stochastic(close = ioe159['Close'], 
	                     high = ioe159['High'], 
	                     low = ioe159['Low'], 
	                     window = window)
	direction = []
	position = 0
	ss_below = False
	ss_above = False
	for value in ss:
	    if value > lower and ss_below:
	        position = 1
	        ss_below = False
	    elif value < upper and ss_above:
	        position = -1
	        ss_above = False
	    elif value < lower:
	        ss_below = True
	    elif value > upper:
	        ss_above = True
	    direction.append(position)

	direction = np.array(direction)
	if out_sample_start is None:
		show_pnl(direction, ioe159["Settle"])
	else:
		os_data = ioe159["Settle"][out_sample_start:]
		os_direction = direction[-len(os_data):]
		show_pnl(os_direction, os_data)

def moving_average_crossover_strategy(window=5, opp_direction = False, 
									  out_sample_start=None):
	ioe159 = get_ioe0()
	mva = ioe159["Settle"].rolling(center=False, window=window).mean()
	direction = []
	position = 0
	mva_below = False
	mva_above = False
	for i, value in enumerate(mva):
	    if value > ioe159["Settle"][i] and mva_below:
	        position = 1
	        mva_below = False
	    elif value < ioe159["Settle"][i] and mva_above:
	        position = -1
	        mva_above = False
	    elif value < ioe159["Settle"][i]:
	        mva_below = True
	    elif value > ioe159["Settle"][i]:
	        mva_above = True
	    direction.append(position)

	direction = np.array(direction)
	if opp_direction:
		direction = -direction
	if out_sample_start is None:
		show_pnl(direction, ioe159["Settle"])
	else:
		os_data = ioe159["Settle"][out_sample_start:]
		os_direction = direction[-len(os_data):]
		show_pnl(os_direction, os_data)

def macd_strategy(long=26, mid=12, short=9,
				  use_divergence=False,
				  out_sample_start=None):
	"""
	default MACD(26, 12, 9) is used
	"""
	ioe159 = get_ioe0()
	ema_long = ioe159['Settle'].ewm(span=long, adjust=False).mean()
	ema_mid = ioe159['Settle'].ewm(span=mid, adjust=False).mean()
	macd = ema_mid - ema_long
	macd_ema_short = macd.ewm(span=short, adjust=False).mean()
	divergence = macd - macd_ema_short
	direction = []
	position = 0
	if use_divergence:
		div_prev = 0
		for i in range(ioe159.shape[0]):
			if divergence[i] > div_prev:
				position = 1
			else:
				position = -1
			direction.append(position)
			div_prev = divergence[i]

	else:
		for i in range(ioe159.shape[0]):
		    if macd[i] > macd_ema_short[i]:
		        position = 1
		    else:
		    	position = -1
		    direction.append(position)

	direction = np.array(direction)

	if out_sample_start is None:
		show_pnl(direction, ioe159["Settle"])
	else:
		os_data = ioe159["Settle"][out_sample_start:]
		os_direction = direction[-len(os_data):]
		show_pnl(os_direction, os_data)

def rsi_strategy(window=14, out_sample_start=None, 
				 upper=70, lower=30):
	"""
	default RSI(14) is used
	"""
	ioe159 = get_ioe0()
	pnl = ioe159['Settle']- ioe159['Settle'].shift(1)
	profit = pnl.clip(lower=0, upper=None)
	loss = pnl.clip(lower=None, upper=0)
	avg_profit = profit.rolling(window=window).mean()
	avg_loss = loss.rolling(window=window).mean()
	rsi = 100 -100/(1 + avg_profit/abs(avg_loss))
	direction = []
	position = 0
	for i in range(ioe159.shape[0]):
	    if rsi[i] > upper:
	    	position = 1
	    if rsi[i] < lower:
	   		position = -1
	    direction.append(position)
	direction = np.array(direction)

	if out_sample_start is None:
		show_pnl(direction, ioe159["Settle"])
	else:
		os_data = ioe159["Settle"][out_sample_start:]
		os_direction = direction[-len(os_data):]
		show_pnl(os_direction, os_data)

def bollinger_bands_strategy(window=14, out_sample_start=None, 
				 			 upper=70, lower=30):
	"""
	default RSI(14) is used
	"""
	ioe159 = get_ioe0()
	pnl = ioe159['Settle']- ioe159['Settle'].shift(1)
	profit = pnl.clip(lower=0, upper=None)
	loss = pnl.clip(lower=None, upper=0)
	avg_profit = profit.rolling(window=window).mean()
	avg_loss = loss.rolling(window=window).mean()
	rsi = 100 -100/(1 + avg_profit/abs(avg_loss))
	direction = []
	position = 0
	for i in range(ioe159.shape[0]):
	    if rsi[i] > upper:
	    	position = 1
	    if rsi[i] < lower:
	   		position = -1
	    direction.append(position)
	direction = np.array(direction)

	if out_sample_start is None:
		show_pnl(direction, ioe159["Settle"])
	else:
		os_data = ioe159["Settle"][out_sample_start:]
		os_direction = direction[-len(os_data):]
		show_pnl(os_direction, os_data)