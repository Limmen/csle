#!/bin/bash

nohup prometheus --config.file=$CSLE_HOME/management-system/prometheus.yml --storage.tsdb.retention.size=10GB --storage.tsdb.retention.time=5d & > /var/log/csle/prometheus.log