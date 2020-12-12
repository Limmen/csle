#!/bin/bash

cd pycr_monitor; npm run build

nohup python pycr_monitor/server/server.py &