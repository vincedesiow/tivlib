"""
Script to import iron futures data from quandl
"""

import quandl
import pandas as pd

quandl.ApiConfig.api_key = 'LRxNLmnMssNZbDKnPZQh'
months = {'F': 1, 'G': 2, 'H': 3, 'J': 4, 'K': 5, 'M': 6, 
          'N': 7, 'Q': 8, 'U': 9, 'V': 10, 'X': 11, 'Z': 12}
years = ['2015', '2016', '2017', '2018', '2019']
f =  pd.HDFStore('../data/store.h5')

# iron futures
for year in years:
    for month in months.keys():
        try:
            f['I'+month+year] = quandl.get('DCE/I'+month+year)
            print('Iron futures ' + str(months[month]) + '-' + year + ' successfully obtained')
        except:
            print('Error: no data available yet for iron futures %s'
            	  %(str(months[month]) + '-' + year))

# Shanghai Steel Rebar Futures Individual Contracts
years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
for year in years:
    for month in months.keys():
        try:
            f['RB'+month+year] = quandl.get('SHFE/RB'+month+year)
            print('Rebar futures ' + str(months[month]) + '-' + year + ' successfully obtained')
        except:
            print('Error: no data available yet for rebar futures %s'
            	  %(str(months[month]) + '-' + year))

# Shanghai Hot Rolled Coil Futures Individual Contracts
years = ['2014', '2015', '2016', '2017', '2018', '2019']
for year in years:
    for month in months.keys():
        try:
            f['HC'+month+year] = quandl.get('SHFE/HC'+month+year)
            print('Hot rolled coil futures ' + str(months[month]) + '-' + year + ' successfully obtained')
        except:
            print('Error: no data available yet for hot rolled coil futures %s'
                  %(str(months[month]) + '-' + year))

# === Currently not needed ===

# fx (Spot rates to USD)
# currencies = ['DEXUSAL', 'DEXBZUS', 'DEXUSUK', 'DEXCAUS', 
# 			  'DEXCHUS', 'DEXDNUS', 'DEXUSEU', 'DEXHKUS',
# 			  'DEXINUS', 'DEXJPUS', 'DEXMAUS', 'DEXMXUS', 
# 			  'DEXTAUS', 'DEXUSNZ', 'DEXNOUS', 'DEXSIUS', 
# 			  'DEXSFUS', 'DEXKOUS', 'DEXSLUS', 'DEXSDUS', 
# 			  'DEXSZUS', 'DEXTHUS', 'DEXVZUS']

# for currency in currencies:
# 	try:
# 		f[currency] = quandl.get('FRED/'+currency)
# 		print(currency + ' successfully obtained')
# 	except:
# 		print('Error: no data available for %s'%currency)