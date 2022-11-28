#!/bin/bash

echo "Running csle-cli integration tests"
cd simulation-system/libs/csle-cli; pytest; cd ../../../
