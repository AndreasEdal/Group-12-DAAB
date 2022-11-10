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
file = "hdfs://namenode:9000/commitData/repoLanguages.json"
df = spark.read.json(file)

data = df.select("repo_name", "language")

name = "vr367305/elaboratokitten"
dataByName = df.filter(df.repo_name == name)


# Take the content of the files and split them
dataByName.show() 

savedFile = 'hdfs://namenode:9000/commitData/' + name

#dataByName.write.save(savedFile, format='json', mode='append')

#df2 = spark.read.json(savedFile)

languages = dataByName.select("language.name").collect()

languageArray = []
i = 0
while (i < len(languages[0])):
    languageArray.append(languages[0][i])
    i += 1

print("Languages used in repository ", name, ": ", languageArray)