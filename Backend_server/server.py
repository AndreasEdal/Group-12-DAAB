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
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max',1) \
    .config('spark.executor.memory', '1g') \
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

    languageArray = []
    i = 0
    while (i < len(languages[0])):
        languageArray.append(languages[0][i])
        i += 1

    
    message = "Code languages used in"+ name+ ": "+ languageArray[0][0]+ ", " + languageArray[0][1]+ " and " + languageArray[0][2]
    print(message)
    
    return message

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
