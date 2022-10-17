import org.apache.spark.sql.SparkSession

object Main extends App {
  val spark = SparkSession.builder.appName("streamTest")
  .config("spark.master", "spark://spark-master:7077")
  .config("spark.executor.cores", 1)
  .config("spark.cores.max", 1)
  .config("spark.executor.memory", "1g")
  .config("spark.sql.streaming.checkpointlocation", "hdfs://namenode:9000/stream-checkpoint/")
  .getOrCreate()

  val df = spark.read.json("hdfs://namenode:9000/commitData/commitAuthorMessage.json")
  
  val data = df.select("author.name", "commit", "message")

  val name : String = "cph"
  val dataByname = df.filter(df("author.name") === name)

  dataByname.show()


}