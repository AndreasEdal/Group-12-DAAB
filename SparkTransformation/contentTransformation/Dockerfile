FROM bde2020/spark-python-template:3.3.0-hadoop3.3

COPY contentTransformation.py /app

ENV SPARK_APPLICATION_PYTHON_LOCATION /app/contentTransformation.py
ENV SPARK_SUBMIT_ARGS "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0"
