# OS
FROM kimham/csle_ubuntu_22_base:0.8.0
USER root

# Spark
RUN wget https://dlcdn.apache.org/spark/spark-3.5.4/spark-3.5.4-bin-hadoop3.tgz &&\
    tar -zxvf spark-3.5.4-bin-hadoop3.tgz

ENV SPARK_HOME=/spark-3.5.4-bin-hadoop3
ENV PYSPARK_PYHON=root/miniconda3/bin/python
ENV SPARK_LOCAL_HOSTNAME=localhost
