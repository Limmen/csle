# Re-generate gRPC files

To re-generate the gRPC files, run: 
```bash
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/client_manager/. ./protos/client_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/kafka_manager/. ./protos/kafka_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/docker_stats_manager/. ./protos/docker_stats_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/ids_manager/. ./protos/ids_manager.proto
```
