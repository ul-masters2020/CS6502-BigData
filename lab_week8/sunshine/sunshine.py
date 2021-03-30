import csv

from io import StringIO
from datetime import datetime
from collections import namedtuple
from operator import add, itemgetter
from pyspark import SparkConf, SparkContext

APP_NAME = "CS6502-Longest-Sunshine"
DATE_FMT = "%Y-%m-%d"

def parse(row):
	"""
	Parse a row and returns a named tuple
	"""
	

def split(line):
	"""
	Operator function to split a line with csv module
	"""
	reader = csv.reader(StringIO(line))
	return next(reader)


def main(sc):
	rawData = sc.textFile("/dly518.csv")
	header = rawData.first()
	filteredData = rawData.filter( lambda l: l !=header)
	flights = filteredData.map(split).map(parse).filter(lambda i:i !=None)
    
	delays = flights.map(lambda f: (f.date,f.ind1,f.sun)).map(lambda x: (x[0], x))
	
	delays= delays.reduceByKey(lambda x1, x2: max(x1, x2, key=lambda x: x[-1])).values().collect()
    
	print(delays)

if __name__ == "__main__":
	conf = SparkConf().setAppName(APP_NAME)
	conf = conf.setMaster("local[*]")
	sc = SparkContext(conf = conf)

	# execute main function
	main(sc)
