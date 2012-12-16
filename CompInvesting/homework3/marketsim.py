import sys
import csv

cash= sys.argv[1]
orders =sys.argv[2]
values = sys.argv[3]

print "initial cash:", cash
print "orders: ", orders
print "values: ", values

of = open(orders, "rU")
rd = csv.reader(of)
for row in rd:
	for col in row:
		print col
of.close()
