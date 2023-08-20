#!/bin/bash

echo "Running Python Linter"
flake8 simulation-system/
flake8 emulation-system/envs
flake8 examples/

echo "Running JavaScript Linter"
cd management-system/csle-mgmt-webapp; npx eslint . --quiet