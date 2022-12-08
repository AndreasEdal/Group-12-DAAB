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

spark = SparkSession.builder.appName('streamTest') \
    .config('spark.master','spark://spark-master:7077') \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max',1) \
    .config('spark.executor.memory', '1g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://namenode:9000/stream-checkpoint/') \
    .getOrCreate()

@app.route('/codeLanguage')
@cross_origin()
def getLanguages():
    file = "hdfs://namenode:9000/commitData/repoLanguages.json"
    df = spark.read.json(file)

    data = df.select("repo_name", "language")

    name = request.args.get("reponame")
    dataByName = df.filter(df.repo_name == name)

    dataByName.show() 

    languages = dataByName.select("language.name").collect()

    message = "Code languages used in"+ name+ ": "

    languageArray = []
    i = 0
    print(languages)    
    while (i < len(languages[0][0])):
        languageArray.append(languages[0][0][i])
        print(languageArray[i])
        message += languageArray[i] + ", "
        i += 1

    print(message)
    
    return message

@app.route('/mostContributions')
@cross_origin()
def getMostContributions():
    file = "hdfs://namenode:9000/commitData/commitAuthorRepo.json"
    df = spark.read.json(file)
    df.show()

    name = request.args.get("reponame")

    dataByName = df.filter(df.repo_name[0] == name)
    #dataByName = dataByName.select("repo_name", "author")

    dataByName.show()
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
    df = spark.read.parquet("hdfs://namenode:9000/data/commit.parquet/")

    dataByName = df.filter(df.repo_name == name)
    dataByName = dataByName.groupBy("repo_name").count().orderBy(col('count').desc())

    dataByName.show()

    count = dataByName.select("count").collect()[0][0]
    print(count)

    return "The total commits for TIMEFRAME one "+ name +" is: " + str(count)

@app.route('/repoWithMostCommits') 
@cross_origin()
def getRepoWithMostCommits():
    return "Repository with most commits is: "

@app.route('/repoSize') 
@cross_origin()
def getRepoSize():
    return "Size of REPO is: "


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7050)
