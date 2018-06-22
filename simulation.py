import numpy as np
from tivlib.preprocess import get_jan_may_sep
from tivlib.stats import slow_stochastic
from tivlib.utils import show_pnl
import matplotlib.pyplot as plt

def slow_stochastic_strategy(window=5, out_sample_start=None):
	ioe159 = get_jan_may_sep()
	ss = slow_stochastic(close = ioe159['Close'], 
	                     high = ioe159['High'], 
	                     low = ioe159['Low'], 
	                     window = window)
	direction = []
	position = 0
	ss_below = False
	ss_above = False
	for value in ss:
	    if value > 0.2 and ss_below:
	        position = 1
	        ss_below = False
	    elif value < 0.8 and ss_above:
	        position = -1
	        ss_above = False
	    elif value < 0.2:
	        ss_below = True
	    elif value > 0.8:
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
	ioe159 = get_jan_may_sep()
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