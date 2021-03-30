import csv

from io import StringIO
from datetime import datetime
from collections import namedtuple
from operator import add, itemgetter
from pyspark import SparkConf, SparkContext

APP_NAME = "CS6502-Longest-Sunshine"
DATE_FMT = "%d-%m-%Y"

def parse(row):
    #print(row)
    try:
        #if(datetime.strptime(row[0],DATE_FMT).year())
        row[1]=datetime.strptime(row[0],DATE_FMT).date()
        row[0]=datetime.strptime(row[0],DATE_FMT).date().year
        row[17]=float(row[17])
        #print(row)
        return Sunshine(*row[:25])
    except ValueError:
        pass
    

 

def split(line):
    """
    Operator function to split a line with csv module
    """
    reader = csv.reader(StringIO(line))
    return next(reader)

 

def main(sc):
    rawData=sc.textFile("gs://cs6502-20135262/dly518.csv")
    header=rawData.first()
    filteredData=rawData.filter( lambda l: l !=header)
    eachday=  filteredData.map(split).map(parse).filter(lambda i:i !=None)
    
    sunny = flights.map(lambda f: (f.date,f.ind1,f.sun)).map(lambda x: (x[0], x))

    delays=delays.reduceByKey(lambda x1, x2: max(x1, x2, key=lambda x: x[-1])).values().collect()
    print(delays)
 
    
    sunshine = sorted(delays, key=itemgetter(0))

    for d in sunshine:
        print("In the year %s on %s there was maximum sunshine of %s hrs"%(d[0],d[1], d[2]))

if __name__ == "__main__":
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc = SparkContext(conf = conf)

 

    # execute main function
    main(sc)
