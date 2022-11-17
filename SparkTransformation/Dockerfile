FROM bde2020/spark-python-template:3.3.0-hadoop3.3

RUN pip3 install flask
RUN pip3 install flask_cors
RUN pip3 install flask-mysql

COPY server.py /app

EXPOSE 7050

ENV SPARK_APPLICATION_PYTHON_LOCATION /app/sparkLanguages.py
ENV SPARK_SUBMIT_ARGS "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0"

CMD python3 /app/server.py
