#!/bin/bash

echo "Running JavaScript Linter"
cd management-system/csle-mgmt-webapp; npx eslint . --quiet; cd ../../