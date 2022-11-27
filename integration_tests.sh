#!/bin/bash

echo "Running csle-cli integration tests"
cd csle-cli; pytest; cd ../
