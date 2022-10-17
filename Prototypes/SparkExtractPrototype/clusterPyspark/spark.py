from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import explode, split, to_json, array, col, udf, sum
import locale
locale.getdefaultlocale()
locale.getpreferredencoding()

# Limit cores to 1, and tell each executor to use one core = only one executor is used by Spark
spark = SparkSession.builder.appName('streamTest') \
    .config('spark.master','spark://spark-master:7077') \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max',1) \
    .config('spark.executor.memory', '1g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://namenode:9000/stream-checkpoint/') \
    .getOrCreate()
    
# Create a read stream from Kafka and a topic
file = "hdfs://namenode:9000/commitData/commitAuthorMessage.json"
df = spark.read.json(file)

data = df.select("author.name", "commit", "message")

name = "cph"
dataByName = df.filter(df.author["name"] == name)


# Take the content of the files and split them
dataByName.show() 

dataByName.write.save('hdfs://namenode:9000/commitData/commitsBy' + name, format='json', mode='append')