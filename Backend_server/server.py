from flask import Flask, jsonify, request 
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
import json
app = Flask(__name__)
cors = CORS(app)

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import explode, split, to_json, array, col, udf, sum
import locale
locale.getdefaultlocale()
locale.getpreferredencoding()

spark = SparkSession.builder.appName('streamTest') \
    .config('spark.master','spark://spark-master:7077') \
    .config('spark.executor.cores', 2) \
    .config('spark.cores.max',2) \
    .config('spark.executor.memory', '2g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://namenode:9000/stream-checkpoint/') \
    .getOrCreate()

@app.route('/language')
@cross_origin()
def getLanguages():
    file = "hdfs://namenode:9000/commitData/repoLanguages.json"
    df = spark.read.json(file)

    data = df.select("repo_name", "language")

    name = request.args.get("reponame")
    dataByName = df.filter(df.repo_name == name)


    # Take the content of the files and split them "vr367305/elaboratokitten"
    dataByName.show() 

    savedFile = 'hdfs://namenode:9000/commitData/' + name

    #dataByName.write.save(savedFile, format='json', mode='append')

    #df2 = spark.read.json(savedFile)

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
    authors = dataByName.select("author.name").collect()
    print(authors)

    authorDict = dict()
    i = 0
    while (i < len(authors)):
        print(authors[i][0])
        if (authorDict.get(authors[i][0]) != None):
            count = authorDict.get(authors[i][0])
            authorDict.update({authors[i][0]: count + 1})
        else:
            authorDict[authors[i][0]] = 1
        i += 1
    
    max_key = max(authorDict, key=authorDict.get)
    
    return "Most contributions to " + name + " are made by: " + max_key + " with " + str(authorDict.get(max_key)) + " commits"

@app.route('/person/', methods=['POST'])
@cross_origin()
def insertPerson():
    if request.method == "POST":
        firstName = request.form['firstname']
        lastName = request.form['lastname']

        cur = mysql.get_db().cursor()
        cur.execute('''INSERT INTO persons (firstName, lastName) VALUES (%s,%s)''', (firstName, lastName))
        mysql.get_db().commit()
        cur.close()
    return "Person added"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7050)
