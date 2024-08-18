#!/bin/bash

echo "Running csle-cli integration tests"
cd simulation-system/libs/csle-cli; pytest; cd ../../../

echo "Running emulation-system integration tests"
cd emulation-sustem/tests; pytest; cd ../../
