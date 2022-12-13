from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import  StructType, StructField, StringType, BooleanType, DoubleType, IntegerType, ArrayType, TimestampType
from pyspark.sql.functions import explode, split, to_json, from_json, array, col, udf, sum, struct, lit
import locale
locale.getdefaultlocale()
locale.getpreferredencoding()
import os

spark_master_url = os.environ["DAAB_SPARK_URL"] or "spark-master:7077"
namenode_url = os.environ["DAAB_NAMENODE_URL"] or "namenode:9000"
kafka_url = os.environ["DAAB_KAFKA_URL"] or "kafka:9092"

print("spark_master_url: " + spark_master_url)
print("namenode_url: " + namenode_url)
print("kafka_url: " + kafka_url)

# Limit cores to 1, and tell each executor to use one core = only one executor is used by Spark
spark = SparkSession.builder.appName('content-connector') \
    .config('spark.master','spark://' + spark_master_url) \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max',1) \
    .config('spark.executor.memory', '1g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://' + namenode_url + '/stream-checkpoint/') \
    .getOrCreate()

#Create schema for input and output
schema = StructType([
    StructField("repo_name", StringType()),
    StructField("size", IntegerType())
])


# Create a read stream from Kafka and a topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("startingOffsets", "earliest")\
    .option("subscribe", "answerSpaceUsed") \
    .load()


value_df = df.select(from_json(col("value").cast("string"),schema).alias("value"))

selected_df = value_df.selectExpr('value.repo_name', 'value.size')

# Write parquet file to hdfs 
#df.writeStream.mode('append').parquet("hdfs://namenode:9000/data/commit.parquet")

selected_df\
    .writeStream\
    .format('parquet')\
    .option("path", "hdfs://" + namenode_url + "/data/repoSize.parquet") \
    .outputMode("append") \
    .start().awaitTermination()

