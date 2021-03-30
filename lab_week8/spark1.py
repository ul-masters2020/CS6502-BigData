import csv

from io import StringIO
from datetime import datetime
from collections import namedtuple
from operator import add, itemgetter
from pyspark import SparkConf, SparkContext

# module constants

APP_NAME = "CS6502 Spark Example"
DATE_FMT = "%Y-%m-%d"
TIME_FMT = "%H%M"

fields = ('date', 'airline', 'flightnum', 'origin', 'dest', 'dep', 'dep_delay', 'arv', 'arv_delay', 'airtime', 'distance')
Flights = namedtuple('Flights', fields)

# functions

def parse(row):
	"""
	Parse a row and returns a named tuple
	"""
	print(row)
	try:
		row[0] = datetime.strptime(row[0], DATE_FMT).date()
		row[5] = datetime.strptime(row[5], TIME_FMT).time()
		row[6] = float(row[6])
		row[7] = datetime.strptime(row[7], TIME_FMT).time()
		row[8] = float(row[8])
		row[9] = float(row[9])
		row[10] = float(row[10])

		return Flights(*row[:11])
	except ValueError:
		pass

def split(line):
	"""
	Operator function to split a line with csv module
	"""
	reader = csv.reader(StringIO(line))
	return next(reader)


def main(sc):
	rawData = sc.textFile("gs://cs6502-20135262/airlines.csv")
	# we will first remove the header row for airlines.csv
	header = rawData.first()
	filteredData = rawData.filter(lambda l: l != header)
	airlines = dict(filteredData.map(split).collect())

	#note that here we are using broadcast variables
	airlines_lookup = sc.broadcast(airlines)

	rawData = sc.textFile("gs://cs6502-20135262/flights.csv")
	# we will do the same for flights.csv
	header = rawData.first()
	filteredData = rawData.filter(lambda l: l != header)

	# now for each flight record we will covert to a namedtuple 
	flights = filteredData.map(split).map(parse).filter(lambda i: i != None)

	# get the k/v pairs
	delays = flights.map(lambda f: (airlines_lookup.value[f.airline], add(f.dep_delay, f.arv_delay)))

	# map/reduce phase, for each airline get the total delay
	delays = delays.reduceByKey(add).collect()

	# sort the result, based on total delays value
	delays = sorted(delays, key=itemgetter(1))

	# output result
	for d in delays:
		print("%0.0f minutes delayed \t%s"%(d[1], d[0]))

if __name__ == "__main__":
	conf = SparkConf().setAppName(APP_NAME)
	conf = conf.setMaster("local[*]")
	sc = SparkContext(conf = conf)

	# execute main function
	main(sc)
