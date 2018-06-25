import numpy as np
from tivlib.preprocess import get_ioe0, get_rb0
from tivlib.stats import slow_stochastic
from tivlib.utils import show_pnl
import matplotlib.pyplot as plt
from scipy import stats 

def select_security(security):
	if security == 'iron':
		return get_ioe0()
	elif security == 'rebar':
		return get_rb0()

def slow_stochastic_strategy(security,
						     window=5, 
							 lower=0.2,
							 upper=0.8,
							 out_sample_start=None, 
							 return_directions=False):
	df = select_security(security)
	ss = slow_stochastic(close = df['Close'], 
	                     high = df['High'], 
	                     low = df['Low'], 
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
	if return_directions:
		return direction
	if out_sample_start is None:
		show_pnl(direction, df["Settle"])
	else:
		os_data = df["Settle"][out_sample_start:]
		os_direction = direction[-len(os_data):]
		show_pnl(os_direction, os_data)

def moving_average_crossover_strategy(security, window=5, opp_direction = False, 
									  out_sample_start=None, 
									  return_directions=False):
	df = select_security(security)
	mva = df["Settle"].rolling(center=False, window=window).mean()
	direction = []
	position = 0
	mva_below = False
	mva_above = False
	for i, value in enumerate(mva):
	    if value > df["Settle"][i] and mva_below:
	        position = 1
	        mva_below = False
	    elif value < df["Settle"][i] and mva_above:
	        position = -1
	        mva_above = False
	    elif value < df["Settle"][i]:
	        mva_below = True
	    elif value > df["Settle"][i]:
	        mva_above = True
	    direction.append(position)

	direction = np.array(direction)
	if return_directions:
		return direction
	if opp_direction:
		direction = -direction
	if out_sample_start is None:
		show_pnl(direction, df["Settle"])
	else:
		os_data = df["Settle"][out_sample_start:]
		os_direction = direction[-len(os_data):]
		show_pnl(os_direction, os_data)

def macd_strategy(security, long=26, mid=12, short=9,
				  use_divergence=False,
				  out_sample_start=None, 
				  return_directions=False):
	"""
	default MACD(26, 12, 9) is used
	"""
	df = select_security(security)
	ema_long = df['Settle'].ewm(span=long, adjust=False).mean()
	ema_mid = df['Settle'].ewm(span=mid, adjust=False).mean()
	macd = ema_mid - ema_long
	macd_ema_short = macd.ewm(span=short, adjust=False).mean()
	divergence = macd - macd_ema_short
	direction = []
	position = 0
	if use_divergence:
		div_prev = 0
		for i in range(df.shape[0]):
			if divergence[i] > div_prev:
				position = 1
			else:
				position = -1
			direction.append(position)
			div_prev = divergence[i]

	else:
		for i in range(df.shape[0]):
		    if macd[i] > macd_ema_short[i]:
		        position = 1
		    else:
		    	position = -1
		    direction.append(position)

	direction = np.array(direction)
	if return_directions:
		return direction
	if out_sample_start is None:
		show_pnl(direction, df["Settle"])
	else:
		os_data = df["Settle"][out_sample_start:]
		os_direction = direction[-len(os_data):]
		show_pnl(os_direction, os_data)

def rsi_strategy(security, window=14, out_sample_start=None, 
				 upper=70, lower=30, return_directions=False):
	"""
	default RSI(14) is used
	"""
	df = select_security(security)
	pnl = df['Settle']- df['Settle'].shift(1)
	profit = pnl.clip(lower=0, upper=None)
	loss = pnl.clip(lower=None, upper=0)
	avg_profit = profit.rolling(window=window).mean()
	avg_loss = loss.rolling(window=window).mean()
	rsi = 100 -100/(1 + avg_profit/abs(avg_loss))
	direction = []
	position = 0
	for i in range(df.shape[0]):
	    if rsi[i] > upper:
	    	position = 1
	    if rsi[i] < lower:
	   		position = -1
	    direction.append(position)
	direction = np.array(direction)
	if return_directions:
		return direction

	if out_sample_start is None:
		show_pnl(direction, df["Settle"])
	else:
		os_data = df["Settle"][out_sample_start:]
		os_direction = direction[-len(os_data):]
		show_pnl(os_direction, os_data)

def bollinger_bands_strategy(security, window=14, out_sample_start=None, 
				 			 upper=70, lower=30, return_directions=False):
	"""
	default RSI(14) is used
	"""
	df = select_security(security)
	pnl = df['Settle']- df['Settle'].shift(1)
	profit = pnl.clip(lower=0, upper=None)
	loss = pnl.clip(lower=None, upper=0)
	avg_profit = profit.rolling(window=window).mean()
	avg_loss = loss.rolling(window=window).mean()
	rsi = 100 -100/(1 + avg_profit/abs(avg_loss))
	direction = []
	position = 0
	for i in range(df.shape[0]):
	    if rsi[i] > upper:
	    	position = 1
	    if rsi[i] < lower:
	   		position = -1
	    direction.append(position)
	direction = np.array(direction)
	if return_directions:
		return direction

	if out_sample_start is None:
		show_pnl(direction, df["Settle"])
	else:
		os_data = df["Settle"][out_sample_start:]
		os_direction = direction[-len(os_data):]
		show_pnl(os_direction, os_data)

def master_strategy(security, out_sample_start=None, return_directions=False):
	df = select_security(security)
	direction = None
	if security == 'iron':
		dir1 = slow_stochastic_strategy(security=security,
										window=3, 
										lower=0.35,
										upper=0.65,
										out_sample_start=out_sample_start, 
										return_directions=True)
		dir2 = moving_average_crossover_strategy(security=security, 
												 window=20, 
												 opp_direction=True, 
												 out_sample_start=out_sample_start, 
												 return_directions=True)
		dir3 = macd_strategy(security=security, 
							 long=25, 
							 mid=12, 
							 short=2, 
							 use_divergence=True, 
							 out_sample_start=out_sample_start, 
							 return_directions=True)
		directions = np.stack((dir1, dir2, dir3), axis=1)
		direction = stats.mode(directions, axis=1)[0]
		direction = direction.reshape((direction.shape[0]))
		direction = np.array(direction)

	elif security == 'rebar':
		dir1 = slow_stochastic_strategy(security=security,
										window=7, 
										lower=0.4,
										upper=0.6,
										out_sample_start=out_sample_start, 
										return_directions=True)
		dir2 = moving_average_crossover_strategy(security=security, 
												 window=5, 
												 opp_direction=True, 
												 out_sample_start=out_sample_start, 
												 return_directions=True)
		dir3 = macd_strategy(security=security, 
							 long=26, 
							 mid=12, 
							 short=2, 
							 use_divergence=True, 
							 out_sample_start=out_sample_start, 
							 return_directions=True)
		directions = np.stack((dir1, dir2, dir3), axis=1)
		direction = stats.mode(directions, axis=1)[0]
		direction = direction.reshape((direction.shape[0]))
		direction = np.array(direction)

	if return_directions:
		return direction

	if out_sample_start is None:
		show_pnl(direction, df["Settle"])
	else:
		os_data = df["Settle"][out_sample_start:]
		os_direction = direction[-len(os_data):]
		show_pnl(os_direction, os_data)