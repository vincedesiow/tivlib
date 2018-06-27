import numpy as np
import pandas as pd

# months and years data (need to be updated in the long run)
months = {'F': 1, 'G': 2, 'H': 3, 'J': 4, 'K': 5, 'M': 6, 
          'N': 7, 'Q': 8, 'U': 9, 'V': 10, 'X': 11, 'Z': 12}
years = ['2015', '2016', '2017', '2018', '2019']


def compute_returns(data, delta = 1):
	"""
	compute the percentage change in delta number of 
	periods

	data in numpy array format as of now
	default delta = 1 (one period change)
	"""
	return (data[delta:] - data[:-delta])/data[:-1]

def get_ioe1(path = "data/store.h5"):
	"""
	make ioe1 by rolling over quandl's spot month futures contract
	"""
	f = pd.HDFStore(path)
	ioe1 = pd.DataFrame()
	rb_contracts = [i for i in f.keys() if i[1] is 'I']
	for contract in rb_contracts:
	    contract_month = months[contract[2]]  - 1
	    contract_year = int(contract[3:])
	    contract_year = contract_year - 1 if contract_month <= 0 else contract_year
	    contract_month = contract_month if contract_month > 0 else contract_month + 12
	    timestamp_start = str(contract_year) + '-' + str(contract_month)
	    timestamp_end = contract[3:] + '-' + str(months[contract[2]])
	    try:
	        # rollover is done on the 11th trading day to compute ioe1
	        start_date = f[contract][timestamp_start].head(10).index[-1] + pd.DateOffset(1)
	        end_date = f[contract][timestamp_end].head(10).index[-1]
	        ioe1 = pd.concat([ioe1, f[contract].loc[start_date:end_date]])
	    except:
	        try:
	            start_date = f[contract][timestamp_start].head(10).index[-1] + pd.DateOffset(1)
	            ioe1 = pd.concat([ioe1, f[contract].loc[start_date:]])
	        except:
	            print('Data not available yet for %s to %s'%(timestamp_start, timestamp_end))
	ioe1 = ioe1.sort_index()
	return ioe1

def get_ioe0(path = "data/store.h5"):
	"""
	make modified continuous iron futures using Jan, May and Sep contracts
	rollovered 2 months prior to expiration
	"""
	f = pd.HDFStore(path)
	ioe2 = pd.DataFrame()
	rb_contracts = [i for i in f.keys() if i[1:3]  in ['IF', 'IK', 'IU']]
	for contract in rb_contracts:
	    start_month = months[contract[2]] - 6
	    start_year = int(contract[3:])
	    start_year = start_year - 1 if start_month <= 0 else start_year
	    start_month = start_month if start_month > 0 else start_month + 12
	    end_month = months[contract[2]] - 2
	    end_year = int(contract[3:])
	    end_year = end_year - 1 if end_month <= 0 else end_year
	    end_month = end_month if end_month > 0 else end_month + 12
	    timestamp_start = str(start_year) + '-' + str(start_month)
	    timestamp_end = str(end_year) + '-' + str(end_month)
	    try:
	        # rollover is done on the 11th trading day to compute ioe1
	        start_date = f[contract][timestamp_start].head(10).index[-1] + pd.DateOffset(1)
	        end_date = f[contract][timestamp_end].head(10).index[-1]
	        ioe2 = pd.concat([ioe2, f[contract].loc[start_date:end_date]])
	    except:
	        try:
	            start_date = f[contract][timestamp_start].head(10).index[-1] + pd.DateOffset(1)
	            ioe2 = pd.concat([ioe2, f[contract].loc[start_date:]])
	        except:
	            print('Data not available yet for %s to %s'%(timestamp_start, timestamp_end))
	ioe2 = ioe2.sort_index()
	return ioe2

def get_rb0(path = "data/store.h5"):
	"""
	make modified continuous rebar futures using Jan, May and Oct contracts
	rollovered 2 months prior to expiration 
	"""
	f = pd.HDFStore(path)
	rb0 = pd.DataFrame()
	rb_contracts = [i for i in f.keys() if i[1:4]  in ['RBF', 'RBK', 'RBV']]
	for contract in rb_contracts:
		# hard code start_month, end_month, start_year and end_year
		if months[contract[3]] == 1:
			start_month = 8
			end_month = 11
			start_year = int(contract[4:]) - 1
			end_year = int(contract[4:]) - 1
		elif months[contract[3]] == 5:
			start_month = 11
			end_month = 3
			start_year = int(contract[4:]) - 1
			end_year = int(contract[4:])
		elif months[contract[3]] == 10:
			start_month = 3
			end_month = 8
			start_year = int(contract[4:])
			end_year = int(contract[4:])
		timestamp_start = str(start_year) + '-' + str(start_month)
		timestamp_end = str(end_year) + '-' + str(end_month)
		raw_df = f[contract][['Open', 'Close', 'High', 'Low', 'Volume', 'Settle']]
		try:
			# rollover is done on the 15 of each month or the first day after 15
			start_date = raw_df[timestamp_start + '-15':].index[0] + pd.DateOffset(1)
			end_date = raw_df[:timestamp_end + '-15'].index[-1]
			rb0 = pd.concat([rb0, raw_df.loc[start_date:end_date]])
		except:
		    try:
		        start_date = raw_df[timestamp_start + '-15':].index[0] + pd.DateOffset(1)
		        rb0 = pd.concat([rb0, raw_df.loc[start_date:]])
		    except:
		        print('Data not available yet for %s to %s'%(timestamp_start, timestamp_end))
	rb0 = rb0.sort_index()
	return rb0

def get_hc0(path = "data/store.h5"):
	"""
	make modified continuous hot rolled coil futures using Jan, May and Oct contracts
	rollovered 2 months prior to expiration 
	"""
	f = pd.HDFStore(path)
	hc0 = pd.DataFrame()
	hc_contracts = [i for i in f.keys() if i[1:4]  in ['HCF', 'HCK', 'HCV']]
	for contract in hc_contracts:
		# hard code start_month, end_month, start_year and end_year
		if months[contract[3]] == 1:
			start_month = 8
			end_month = 11
			start_year = int(contract[4:]) - 1
			end_year = int(contract[4:]) - 1
		elif months[contract[3]] == 5:
			start_month = 11
			end_month = 3
			start_year = int(contract[4:]) - 1
			end_year = int(contract[4:])
		elif months[contract[3]] == 10:
			start_month = 3
			end_month = 8
			start_year = int(contract[4:])
			end_year = int(contract[4:])
		timestamp_start = str(start_year) + '-' + str(start_month)
		timestamp_end = str(end_year) + '-' + str(end_month)
		raw_df = f[contract][['Open', 'Close', 'High', 'Low', 'Volume', 'Settle']]
		try:
			# rollover is done on the 15 of each month or the first day after 15
			start_date = raw_df[timestamp_start + '-15':].index[0] + pd.DateOffset(1)
			end_date = raw_df[:timestamp_end + '-15'].index[-1]
			hc0 = pd.concat([hc0, raw_df.loc[start_date:end_date]])
		except:
		    try:
		        start_date = raw_df[timestamp_start + '-15':].index[0] + pd.DateOffset(1)
		        hc0 = pd.concat([hc0, raw_df.loc[start_date:]])
		    except:
		        print('Data not available yet for %s to %s'%(timestamp_start, timestamp_end))
	hc0 = hc0.sort_index()
	return hc0

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def window_stack(data, stepsize=1, width=5):
	"""
	stack data based on width
	"""
	n = data.shape[0]
	return np.hstack( data[i:1+n+i-width:stepsize] for i in range(0,width) )

def normalize_columns(data, return_mean_and_std=False):
	"""
	standard normalization of all columns
	"""
	if not return_mean_and_std:
		return (data - data.mean())/data.std()
	return data.mean(), data.std()

def denormalize_columns(data, mean, std):
	return data * std + mean

def normalize(data):
	return (data - data.mean()) / (data.max() - data.min())

def add_past_data(df, feature, window):
	"""
	add data with lags into existing dataframes as new columns
	"""
	for i in range(window):
		df[feature + ' -' + str(i+1)] = df[feature].shift(i+1)
	return df

def get_last_trading_day_of_month(data):
	"""# ======== CODE TO RETIRE =========
	return the filtered dataframe with last trading data of the month only
	"""
	dateRange = []  
	tempYear = None  
	dictYears = data.index.groupby(data.index.year)
	for yr in dictYears.keys():
	    tempYear = pd.DatetimeIndex(dictYears[yr]).groupby(pd.DatetimeIndex(dictYears[yr]).month)
	    for m in tempYear.keys():
	        dateRange.append(max(tempYear[m]))
	dateRange = pd.DatetimeIndex(dateRange)
	return data.loc[dateRange].sort_index()

def get_last_trading_day_of_quarter(data):
	"""
	return the filtered dataframe with last trading data of the month only
	"""
	dateRange = []  
	tempYear = None  
	dictYears = data.index.groupby(data.index.year)
	for yr in dictYears.keys():
		tempYear = pd.DatetimeIndex(dictYears[yr]).groupby(pd.DatetimeIndex(dictYears[yr]).month)
		for m in tempYear.keys():
			if m in [3, 6, 9, 12]:
				dateRange.append(max(tempYear[m]))
			else:
				pass
	dateRange = pd.DatetimeIndex(dateRange)
	return data.loc[dateRange].sort_index()



# ======== CODE TO RETIRE =========
def clean_bloomberg(excel_file, sheet_name, target):
	"""
	clean bloomberg data based on target created
	"""
	df = pd.read_excel(excel_file, sheet_name, header=5)
	df.index = df.Dates
	df.PX_LAST = df.PX_LAST.astype(float)
	df = df.loc[[i for i in df.loc[target.index[0]:target.index[-1]].index if i in target.index]]
	# check if last date is the same
	df = df.fillna(method ='ffill')
	return df

def get_fx_daily(pairs, start_date, end_date, path = "data/store.h5"):
	f = pd.HDFStore(path)
	fx = pd.DataFrame()
	for pair in pairs:
		fx[pair] = f[pair]['Value'].loc[start_date:end_date]
	return fx