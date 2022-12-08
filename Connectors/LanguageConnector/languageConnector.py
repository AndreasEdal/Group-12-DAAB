from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import  StructType, StructField, StringType, BooleanType, DoubleType, IntegerType, ArrayType, TimestampType
from pyspark.sql.functions import explode, split, to_json, from_json, array, col, udf, sum, struct, lit
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

#Create schema for input and output
schema = StructType([
    StructField("repo_name", StringType()),
    StructField("languages", ArrayType(StringType()))    
])


# Create a read stream from Kafka and a topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("startingOffsets", "earliest")\
    .option("subscribe", "answerLanguages") \
    .load()


value_df = df.select(from_json(col("value").cast("string"),schema).alias("value"))

selected_df = value_df.selectExpr('value.repo_name', 'value.languages')

# Write parquet file to hdfs 
#df.writeStream.mode('append').parquet("hdfs://namenode:9000/data/commit.parquet")

selected_df\
    .writeStream\
    .format('parquet')\
    .option("path", "hdfs://namenode:9000/data/language.parquet") \
    .outputMode("append") \
    .start().awaitTermination()

