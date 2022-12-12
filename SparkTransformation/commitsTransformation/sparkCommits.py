from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import  StructType, StructField, StringType, BooleanType, DoubleType, IntegerType, ArrayType, TimestampType
from pyspark.sql.functions import explode, split, to_json, from_json, array, col, udf, sum, struct, lit
import locale
import os
locale.getdefaultlocale()
locale.getpreferredencoding()

spark_master_url = os.environ["DAAB_SPARK_URL"] or "spark-master:7077"
namenode_url = os.environ["DAAB_NAMENODE_URL"] or "namenode:9000"
kafka_url = os.environ["DAAB_KAFKA_URL"] or "kafka:9092"

# Limit cores to 1, and tell each executor to use one core = only one executor is used by Spark
spark = SparkSession.builder.appName('streamTest') \
    .config('spark.master','spark://' + spark_master_url) \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max',1) \
    .config('spark.executor.memory', '1g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://' + namenode_url + '/stream-checkpoint/') \
    .getOrCreate()

#Create schema for input and output
schema = StructType([
    StructField("parent", StringType()),
    StructField("tree", StringType()),
    StructField("commit", StringType()),
    StructField("author", ArrayType(
        StructType([
            StructField("name", StringType()),
            StructField("email", StringType()),
            StructField("time_sec", IntegerType()),
            StructField("tz_offset", IntegerType()),
            StructField("date", TimestampType())
        ])
    )),
    StructField("commiter", ArrayType(
        StructType([
            StructField("name", StringType()),
            StructField("email", StringType()),
            StructField("time_sec", IntegerType()),
            StructField("tz_offset", IntegerType()),
            StructField("date", TimestampType())
        ])
    )),
    StructField("subject", StringType()),
    StructField("message", StringType()),
    StructField("repo_name", StringType())
])


# Create a read stream from Kafka and a topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_url) \
    .option("startingOffsets", "earliest")\
    .option("subscribe", "commit") \
    .load()

    
#Todo: Change subscribed topic!
value_df = df.select(from_json(col("value").cast("string"),schema).alias("value"))

selected_df = value_df.selectExpr('value.repo_name')

#Create a new column in the dataframe containing a literal value.
commit_df = selected_df.withColumn("commitNumber", lit("1"))

# Create a Kafka write stream containing results
commit_df.select(to_json(struct(col("repo_name"), col("commitNumber"))).alias("value")).select("value")\
    .writeStream\
    .format('kafka')\
    .option("kafka.bootstrap.servers", kafka_url) \
    .option("topic", "answerCommitFreq") \
    .outputMode("append") \
    .start().awaitTermination()
