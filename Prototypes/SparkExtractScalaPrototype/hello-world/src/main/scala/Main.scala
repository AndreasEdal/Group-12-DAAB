import org.apache.spark.sql.SparkSession

@main def hello: Unit =
  val spark = SparkSession.builder.appName("Simple Application").getOrCreate()
  val textFile = spark.read.textFile("hdfs://namenode:9000/commitData/commitAuthorMessage.json")
  println(textFile)

  spark.stop()
  //

def msg = "I was compiled by Scala 3. :)"

