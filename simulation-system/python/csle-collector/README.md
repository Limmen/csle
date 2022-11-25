# `csle-collector`

This library contains scripts and programs for collecting data from the emulation. 

<p align="center">
<img src="docs/data_collection_1.png" width="600">
</p>

## Re-generate gRPC files

To re-generate the gRPC files, run: 
```bash
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/client_manager/. ./protos/client_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/kafka_manager/. ./protos/kafka_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/elk_manager/. ./protos/elk_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/docker_stats_manager/. ./protos/docker_stats_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/snort_ids_manager/. ./protos/snort_ids_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/host_manager/. ./protos/host_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/ossec_ids_manager/. ./protos/ossec_ids_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/traffic_manager/. ./protos/traffic_manager.proto
```

## Requirements

- Python 3.5+
- `grpcio` (for the collector API)
- `grpcio-tools` (for the collector API)
- `scipy` (for statistical models of client processes)
- `confluent-kafka` (for interacting with Kafka)
- `docker` (for interacting with Docker)

## API documentation

This section contains instructions for generating API documentation using `sphinx`.

### Latest Documentation

The latest documentation is available at [https://limmen.dev/csle/docs/csle-collector](https://limmen.dev/csle/docs/csle-collector)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../csle_collector/
make html
```
To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle), copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/csle-collector
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[../../LICENSE](LICENSE.md)

Creative Commons

(C) 2020-2022, Kim Hammar