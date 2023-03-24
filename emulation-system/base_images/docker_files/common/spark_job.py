from pyspark.sql import SparkSession
import socket
import netifaces
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-sm", "--sparkmaster", help="the ip of the spark master", type=str)
    args = parser.parse_args()
    hostname = socket.gethostname()
    try:
        local_ip = netifaces.ifaddresses("eth0")[netifaces.AF_INET][0]["addr"]
    except Exception:
        local_ip = socket.gethostbyname(hostname)
    spark = SparkSession.builder.master(f"spark://{args.sparkmaster}:7077").appName("csle_client").config(
        "spark.driver.host", local_ip).getOrCreate()
    text_file = spark.sparkContext.textFile("/etc/services")
    counts = text_file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    counts.collect()
    spark.stop()