# Re-generate gRPC files

To re-generate the gRPC files, run: 
```bash
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/. ./protos/client_manager.proto
```
