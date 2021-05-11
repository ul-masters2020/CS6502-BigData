from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

timetable = sqlContext.read.json("file:///home/aman/Downloads/UL/SEM2/CS6502/LAB_WORK/project/result.json")

timetable.show()
timetable.printSchema()

timetable.groupBy('type').count().show()