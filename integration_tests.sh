#!/bin/bash

echo "Running csle-cli integration tests"
cd simulation-system/python/csle-cli; pytest; cd ../../../
