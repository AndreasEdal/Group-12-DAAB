from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import  StructType, StructField, StringType, LongType, DoubleType, IntegerType, ArrayType, BooleanType
from pyspark.sql.functions import explode, split, to_json, from_json, array, col, udf, sum, struct
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
    StructField("id", StringType()),
    StructField("size", StringType()),
    StructField("content", StringType()),
    StructField("binary", BooleanType()),
    StructField("copies", IntegerType()),
    StructField("sample_repo_name", StringType()),
    StructField("sample_ref", StringType()),
    StructField("sample_path", StringType()),
    StructField("sample_mode", IntegerType()),
    StructField("sample_symlink_target", StringType()),
])


# Create a read stream from Kafka and a topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("startingOffsets", "earliest")\
    .option("subscribe", "content") \
    .load()

    
#Todo: Change subscribed topic!
value_df = df.select(from_json(col("value").cast("string"),schema).alias("value"))

exploded_df = value_df.selectExpr('value.sample_repo_name','value.size').withColumnRenamed('sample_repo_name', 'repo_name')

data_df = exploded_df.withColumn("size", exploded_df["size"].cast(IntegerType()))

#data = exploded_df.select("repo_name", "language.name")
#languageResult = exploded_df.withColumn("languages", col("name")).drop("name")
#languageResult.show(truncate=False)

# Create a Kafka write stream containing results
data_df.select(to_json(struct(col("repo_name"),col("size"))).alias("value"))\
    .writeStream\
    .format('kafka')\
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("topic", "answerSpaceUsed") \
    .outputMode("append") \
    .start().awaitTermination()
