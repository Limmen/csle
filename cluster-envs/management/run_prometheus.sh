#!/bin/bash

nohup ./prometheus/prometheus --config.file=prometheus/prometheus.yml --storage.tsdb.retention.size=10GB --storage.tsdb.retention.time=5d & > prometheus.log