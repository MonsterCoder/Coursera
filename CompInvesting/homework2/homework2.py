import pandas 
from qstkutil import DataAccess as da
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep
import sys
import csv

# Get the data from the data store
storename = "Yahoo" # get data from our daily prices source
# Available field names: open, close, high, low, close, actual_close, volume
closefield = "actual_close"
volumefield = "volume"
threshhold =5

def findEvents(symbols, startday,endday, marketSymbol,verbose=False):

	# Reading the Data for the list of Symbols.	
	timeofday=dt.timedelta(hours=16)
	timestamps = du.getNYSEdays(startday,endday,timeofday)

	dataobj = da.DataAccess('Yahoo')
	if verbose:
            print __name__ + " reading data"
	# Reading the Data
	close = dataobj.get_data(timestamps, symbols, closefield)
	
	# Completing the Data - Removing the NaN values from the Matrix
#	close = (close.fillna(method='ffill')).fillna(method='backfill')
	

	if verbose:
            print __name__ + " finding events"
	f = open('order.csv','wu')
	writer = csv.writer(f)
	for symbol in symbols:
		
	    for i in range(1,len(close[symbol])):
			if close[symbol][i-1]>=threshhold and close[symbol][i] < threshhold: 
				d = close.index[i]
				if (i+5) < len(close[symbol]):
				   s = close.index[i+5]
				else:
				   s = close.index[close[symbol]]

				print d.year,",",d.month,",",d.day,",", "Buy",",", symbol, 100
				print s.year,",",s.month,",",s.day,",", "Sell",",", symbol, 100
				writer.writerow([d.year,d.month,d.day,symbol,"Buy",100])
				writer.writerow([s.year,s.month,s.day,symbol,"Sell",100])
             		   #np_eventmat[symbol][i] = 1.0  #overwriting by the bit, marking the event
	f.close()		
	return 


#################################################
################ MAIN CODE ######################
#################################################

dataobj = da.DataAccess('Yahoo')
symbols = dataobj.get_symbols_from_list("sp5002012")
symbols.append('SPY')

#symbols =['BFRE','ATCS','RSERF','GDNEF','LAST','ATTUF','JBFCF','CYVA','SPF','XPO','EHECF','TEMO','AOLS','CSNT','REMI','GLRP','AIFLY','BEE','DJRT','CHSTF','AICAF']
startday = dt.datetime(2008,1,1)
endday = dt.datetime(2010,01,01)
eventMatrix = findEvents(symbols,startday,endday,marketSymbol='SPY',verbose=True)

#eventProfiler = ep.EventProfiler(eventMatrix,startday,endday,lookback_days=20,lookforward_days=20,verbose=True)

#:eventProfiler.study(filename="answer.pdf",plotErrorBars=True,plotMarketNeutral=True,plotEvents=False,marketSymbol='SPY')


