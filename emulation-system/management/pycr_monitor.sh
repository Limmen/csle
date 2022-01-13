#!/bin/bash

cd csle_monitor; npm run build

cd csle_monitor; python server/server.py &