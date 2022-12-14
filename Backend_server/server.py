from flask import Flask, jsonify, request 
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
import json
app = Flask(__name__)
cors = CORS(app)

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import explode, split, to_json, array, col, udf, sum, max
import locale
locale.getdefaultlocale()
locale.getpreferredencoding()
import os

spark_master_url = os.environ["DAAB_SPARK_URL"] or "spark-master:7077"
namenode_url = os.environ["DAAB_NAMENODE_URL"] or "namenode:9000"
kafka_url = os.environ["DAAB_KAFKA_URL"] or "kafka:9092"

spark = SparkSession.builder.appName('backend') \
    .config('spark.master','spark://' + spark_master_url) \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max',1) \
    .config('spark.executor.memory', '1g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://' + namenode_url + '/stream-checkpoint/') \
    .getOrCreate()

@app.route('/codeLanguage')
@cross_origin()
def getLanguages():
    name = request.args.get("reponame")
    df = spark.read.parquet('hdfs://' + namenode_url + '/data/language.parquet/')

    dataByName = df.filter(df.repo_name == name)

    data = dataByName.select("repo_name", "languages")

    if (len(data.select("repo_name").collect()) == 0):
        return "Could not find a matching result for repository: " + name
    languages = data.select("languages").collect()[0][0]
    

    message = "Code languages used in"+ name+ ": "

    i = 0
    print(languages)    
    while (i < len(languages)):
        message += languages[i] + ", "
        i += 1

    print(message)
    
    return message

@app.route('/mostContributions')
@cross_origin()
def getMostContributions():
    file = 'hdfs://' + namenode_url + "/commitData/commitAuthorRepo.json"
    df = spark.read.json(file)

    name = request.args.get("reponame")

    dataByName = df.filter(df.repo_name[0] == name)
    #dataByName = dataByName.select("repo_name", "author")

    authors = dataByName.groupBy("author.name").count().orderBy(col('count').desc())
    author = authors.first()
    
    print(author)

    return "Most contributions to " + name + " are made by: " + author[0] + " with " + str(author[1]) + " commits"

@app.route('/linesOfCode')
@cross_origin()
def getLinesOfCode():
    return "Total lines of code for REPO is: "

@app.route('/commitFrequency')
@cross_origin()
def getCommitFrequency():
    name = request.args.get("reponame")
    df = spark.read.parquet('hdfs://' + namenode_url + '/data/commit.parquet/')

    dataByName = df.filter(df.repo_name == name)
    if (len(dataByName.select("repo_name").collect()) == 0):
        return "No response found"

    dataByName = dataByName.groupBy("repo_name").count().orderBy(col('count').desc())

    count = dataByName.select("count").collect()[0][0]

    return "The total commits for TIMEFRAME one "+ name +" is: " + str(count)

@app.route('/repoWithMostCommits') 
@cross_origin()
def getRepoWithMostCommits():
    return "Repository with most commits is: "

@app.route('/repoSize') 
@cross_origin()
def getRepoSize():
    name = request.args.get("reponame")
    df = spark.read.parquet('hdfs://' + namenode_url + '/data/repoSize.parquet/')

    dataByName = df.filter(df.repo_name == name)
    if (len(dataByName.select("repo_name").collect()) == 0):
        return "No response found"

    dataByName = dataByName.groupBy("repo_name").sum("size")


    size = dataByName.select("sum(size)").collect()[0][0]

    return "Total bytes of "+ name +" is: " + str(size)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7050)
