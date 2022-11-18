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

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[../../LICENSE](LICENSE.md)

Creative Commons

(C) 2020-2022, Kim Hammar