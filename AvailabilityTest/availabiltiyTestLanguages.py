from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import  StructType, StructField, StringType, LongType, DoubleType, IntegerType, ArrayType
from pyspark.sql.functions import explode, split, to_json, from_json, array, col, udf, sum, struct, expr
import locale
locale.getdefaultlocale()
locale.getpreferredencoding()
import os

spark_master_url = "spark-master:7077"
namenode_url = "namenode:9000"
kafka_url = "kafka:9092"

print("spark_master_url: " + spark_master_url)
print("namenode_url: " + namenode_url)
print("kafka_url: " + kafka_url)

# Limit cores to 1, and tell each executor to use one core = only one executor is used by Spark
spark = SparkSession.builder.appName('language-transformation') \
    .config('spark.master','spark://' + spark_master_url) \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max',1) \
    .config('spark.executor.memory', '1g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://' + namenode_url + '/stream-checkpoint/') \
    .getOrCreate()

#Create schema for input and output
language_schema = StructType([
    StructField("repo_name", StringType()),
    StructField("language", ArrayType(
        StructType([
           StructField("name", StringType()),
           StructField("bytes", StringType())
        ])
    ))
])

answare_language_schema = StructType([
    StructField("repo_name", StringType()),
    StructField("languages", ArrayType(StringType()))    
])

# Create a read stream from Kafka and a topic
languages_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_url) \
    .option("startingOffsets", "earliest")\
    .option("subscribe", "languages") \
    .load()


answer_langauge_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_url) \
    .option("startingOffsets", "earliest")\
    .option("subscribe", "answerLanguages") \
    .load()

    
#Todo: Change subscribed topic!
value_df = languages_df.select(from_json(col("value").cast("string"),language_schema).alias("value"))

selected_df = value_df.selectExpr('value.repo_name','value.language.name')

data_collect = selected_df.collect()

data = []

for row in data_collect:


#data = exploded_df.select("repo_name", "language.name")
languageResult = selected_df.withColumn("languages", col("name")).drop("name")
#languageResult.show(truncate=False)

# Create a Kafka write stream containing results
languageResult.select(to_json(struct(col("repo_name"),col("languages"))).alias("value")).select("value")\
    .writeStream\
    .format('kafka')\
    .option("kafka.bootstrap.servers", kafka_url) \
    .option("topic", "answerLanguages") \
    .outputMode("append") \
    .start().awaitTermination()
