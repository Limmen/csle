#!/bin/bash

# Start elasticsearch
./elasticsearch/bin/elasticsearch -d

# take a break
sleep 10

# Add sample data
curl -XPUT 'http://127.0.0.1:9200/blog/user/dilbert' \
	-d '{"name" : "Dilbert Brown"}'

# get log
tail -f ./elasticsearch/logs/elasticsearch.log