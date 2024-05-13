#!/bin/bash

cd csle-mgmt-webapp; npm run build

cd csle-mgmt-webapp; python server/server.py &