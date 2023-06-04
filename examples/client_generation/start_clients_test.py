import time
from typing import List
import grpc
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.client_manager.query_clients
from csle_common.metastore.metastore_facade import MetastoreFacade


def stop_client_population():
    with grpc.insecure_channel(f'172.18.0.3:50044') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        stop_clients_msg = csle_collector.client_manager.client_manager_pb2.StopClientsMsg()
        clients_dto = stub.stopClients(stop_clients_msg)
        return clients_dto


def start_client_population():
    emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level4-020")
    clients = emulation_env_config.traffic_config.client_population_config.clients
    clients_grpcs = list(map(lambda x: x.to_grpc_object(), clients))
    workflows_config = emulation_env_config.traffic_config.client_population_config.workflows_config
    workflows_config_grpc = workflows_config.to_grpc_object()
    start_clients_msg = csle_collector.client_manager.client_manager_pb2.StartClientsMsg(
        time_step_len_seconds=emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds,
        clients=clients_grpcs, workflows_config=workflows_config_grpc)
    # Open a gRPC session
    with grpc.insecure_channel(f'172.18.0.3:50044') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        clients_dto = stub.startClients(start_clients_msg, timeout=300)
        return clients_dto

if __name__ == '__main__':
    start_client_population()