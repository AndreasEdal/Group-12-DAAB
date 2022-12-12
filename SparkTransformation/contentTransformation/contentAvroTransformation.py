from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import  StructType, StructField, StringType, LongType, DoubleType, IntegerType, ArrayType, BooleanType
from pyspark.sql.functions import explode, split, to_json, from_json, array, col, udf, sum, struct
from confluent_kafka import Consumer, KafkaException, KafkaError
import avro.schema
import avro.io
import io
import sys
import locale
locale.getdefaultlocale()
locale.getpreferredencoding()

# https://mtpatter.github.io/python-kafka-avro/python-kafka-avro-01.html
schemaAvro = {
  'name': 'Content',
  'type': 'record',
  'namespace': 'com.acme.avro',
  'fields': [
    {
      'name': 'id',
      'type': 'string'
    },
    {
      'name': 'size',
      'type': 'string'
    },
    {
      'name': 'content',
      'type': 'string'
    },
    {
      'name': 'binary',
      'type': 'boolean'
    },
    {
      'name': 'copies',
      'type': 'string'
    },
    {
      'name': 'sample_repo_name',
      'type': 'string'
    },
    {
      'name': 'sample_ref',
      'type': 'string'
    },
    {
      'name': 'sample_path',
      'type': 'string'
    },
    {
      'name': 'sample_mode',
      'type': 'string'
    }
  ]
}

# Create a read stream from Kafka and a topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("startingOffsets", "earliest")\
    .option("subscribe", "content_avro") \
    .load()

if __name__ == "__main__":

    #To consume messages
    conf = {'kafka.bootstrap.servers': 'kafka:9092',
            'default.topic.config': {'auto.offset.reset': 'earliest'}}
    consumer = Consumer(**conf)
    topic = consumer.subscribe(['content_avro'])
    schema = avro.schema.Parse(open(schemaAvro).read())

    try:
        running = True
        while running:
            msg = consumer.poll(timeout=60000)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(),
                                      msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))

            message = msg.value()
            bytes_reader = io.BytesIO(message)
            decoder = avro.io.BinaryDecoder(bytes_reader)
            reader = avro.io.DatumReader(schema)
            try:
                decoded_msg = reader.read(decoder)
                print(decoded_msg)
                sys.stdout.flush()
            except AssertionError:
                continue

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')






# Limit cores to 1, and tell each executor to use one core = only one executor is used by Spark
spark = SparkSession.builder.appName('streamTest') \
    .config('spark.master','spark://spark-master:7077') \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max',1) \
    .config('spark.executor.memory', '1g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://namenode:9000/stream-checkpoint/') \
    .getOrCreate()



#   #Todo: Change subscribed topic!
#   value_df = df.select(from_json(col("value").cast("string"),schema).alias("value"))
#   
#   exploded_df = value_df.selectExpr('value.sample_repo_name','value.size').withColumnRenamed('sample_repo_name', 'repo_name')
#   
#   data_df = exploded_df.withColumn("size", exploded_df["size"].cast(IntegerType()))
#   
#   #data = exploded_df.select("repo_name", "language.name")
#   #languageResult = exploded_df.withColumn("languages", col("name")).drop("name")
#   #languageResult.show(truncate=False)
#   
#   # Create a Kafka write stream containing results
#   data_df.select(to_json(struct(col("repo_name"),col("size"))).alias("value"))\
#       .writeStream\
#       .format('kafka')\
#       .option("kafka.bootstrap.servers", "kafka:9092") \
#       .option("topic", "answerAvroSpaceUsed") \
#       .outputMode("append") \
#       .start().awaitTermination()
#   