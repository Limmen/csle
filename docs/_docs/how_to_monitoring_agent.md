---
title: How-to Update Monitoring Agents
permalink: /docs/how-to-monitoring-agent/
---

## How-to: Update Monitoring Agents
To update the monitoring agents that run on the emulated devices, perform the following steps:

1. Do the necessary code changes to the monitoring agent by editing the files in the directory:
    ```bash
      csle/simulation-system/libs/csle-collector/src/
    ```
   <p class="captionFig">
   Listing 174: Directory with source code of the monitoring agents in CSLE.
   </p>
2. Update the gRPC API by editing the protocol-buffer files in the directory:
    ```bash
      csle/simulation-system/libs/csle-collector/protos/
    ```
   <p class="captionFig">
   Listing 175: Directory with protocol buffers for the monitoring agents in CSLE.
   </p>
3. Regenerate the gRPC Python files by running the commands:
    ```bash
     python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/client_manager/. ./protos/client_manager.proto
     python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/kafka_manager/. ./protos/kafka_manager.proto
     python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/elk_manager/. ./protos/elk_manager.proto
     python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/docker_stats_manager/. ./protos/docker_stats_manager.proto
     python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/snort_ids_manager/. ./protos/snort_ids_manager.proto
     python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/host_manager/. ./protos/host_manager.proto
     python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/ossec_ids_manager/. ./protos/ossec_ids_manager.proto
     python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/traffic_manager/. ./protos/traffic_manager.proto
     python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/ryu_manager/. ./protos/ryu_manager.proto
    ```
   <p class="captionFig">
   Listing 176: Commands to generate gRPC Python files from protobuf files.
   </p>
