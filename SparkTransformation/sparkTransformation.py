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
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("startingOffsets", "earliest")\
    .option("subscribe", "repoEvents") \
    .load()
#Todo: Change subscribed topic!


# Create a Kafka write stream containing results