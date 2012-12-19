import sys
import csv
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

cash= float(sys.argv[1])
orders =sys.argv[2]
values = sys.argv[3]

print "initial cash:", cash
print "orders: ", orders
print "values: ", values

# Reading the Data for the list of Symbols.	
timeofday=dt.timedelta(hours=16)
dataobj = da.DataAccess('Yahoo')
#timestamps = du.getNYSEdays(startday,endday,timeofday)

trades=[]
symbols=[]
holdings=[]
of = open(orders, "rU")
rd = csv.reader(of)

for row in rd:
	trades.append([int(row[0]), int(row[1]), int(row[2]), row[3], row[4], int(row[5])])
	if (row[3] not in symbols):
		symbols.append(row[3])
of.close()

trades.sort(key=lambda d: d[0]*333+d[1]*222+d[2])

length = len(trades) -1
startday = dt.datetime(trades[0][0], trades[0][1], trades[0][2])
endday = dt.datetime(2009, 12, 31,16,0)

# Reading the Data for the list of Symbols.	
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)
dataobj = da.DataAccess('Yahoo')
#print timestamps
close = dataobj.get_data(timestamps, symbols, "actual_close")
close = (close.fillna(method='ffill')).fillna(method='backfill')

def calholdings(timestamp,holdings, close):
	value = 0
	for holding in holdings:
		value = value + close[holding[0]][timestamp] * holding[1]
	return value
	

currenttimestamp =dt.datetime(trades[0][0], trades[0][1], trades[0][2], 16, 0) 
currentvalue = cash

for trade in trades:
	sym = trade[3]
	timestamp = dt.datetime(trade[0], trade[1], trade[2], 16,0)
	cost=close[sym][timestamp] * trade[5]

	if (trade[4]=="Buy"):
		cash= cash - cost
		holdings.append([sym,trade[5]])
	else:
		cash = cash + cost
		holdings.append([sym, trade[5] * -1])	
	#print trade, "cost ", cost, "cash: ", cash

	#if (currenttimestamp != timestamp):
	#	print currenttimestamp, " ", currentvalue

	currenttimestamp = timestamp
	currentvalue= cash + calholdings(timestamp, holdings, close)

#print currenttimestamp, " ", currentvalue
print dt.datetime(2009,12,31, 16, 0), cash + calholdings(dt.datetime(2009,12,31, 16, 0), holdings, close)

		
	#price = close[trade[3]][]
#	print "$",sym, timestamp,close[sym][timestamp]





