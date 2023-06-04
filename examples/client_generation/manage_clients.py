from typing import List
import time
import grpc
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.client_manager.query_clients
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.client import Client
from csle_common.metastore.metastore_facade import MetastoreFacade


def stop_client_population(emulation: str, execution_id: int) \
        -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
    execution = MetastoreFacade.get_emulation_execution(emulation_name=emulation, ip_first_octet=execution_id)
    client_container_external_ip = \
        execution.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip
    client_manager_port = execution.emulation_env_config.traffic_config.client_population_config.client_manager_port
    with grpc.insecure_channel(f'{client_container_external_ip}:{client_manager_port}') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        stop_clients_msg = csle_collector.client_manager.client_manager_pb2.StopClientsMsg()
        clients_dto = stub.stopClients(stop_clients_msg)
        return clients_dto


def start_client_population(emulation: str, execution_id: int, clients: List[Client] = None,
                            workflows_config: WorkflowsConfig = None):
    execution = MetastoreFacade.get_emulation_execution(emulation_name=emulation, ip_first_octet=execution_id)
    if clients is None:
        clients = execution.emulation_env_config.traffic_config.client_population_config.clients
    clients_grpcs = list(map(lambda x: x.to_grpc_object(), clients))
    if workflows_config is None:
        workflows_config = execution.emulation_env_config.traffic_config.client_population_config.workflows_config
    workflows_config_grpc = workflows_config.to_grpc_object()
    start_clients_msg = csle_collector.client_manager.client_manager_pb2.StartClientsMsg(
        time_step_len_seconds=execution.emulation_env_config.traffic_config.client_population_config.
            client_time_step_len_seconds,
        clients=clients_grpcs, workflows_config=workflows_config_grpc)
    client_container_external_ip = \
        execution.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip
    client_manager_port = execution.emulation_env_config.traffic_config.client_population_config.client_manager_port
    with grpc.insecure_channel(f'{client_container_external_ip}:{client_manager_port}') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        clients_dto = stub.startClients(start_clients_msg, timeout=300)
        return clients_dto


def stop_client_producer(emulation: str, execution_id: int):
    execution = MetastoreFacade.get_emulation_execution(emulation_name=emulation, ip_first_octet=execution_id)
    client_container_external_ip = \
        execution.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip
    client_manager_port = execution.emulation_env_config.traffic_config.client_population_config.client_manager_port
    with grpc.insecure_channel(f'{client_container_external_ip}:{client_manager_port}') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        stop_producer_msg = csle_collector.client_manager.client_manager_pb2.StopProducerMsg()
        clients_dto = stub.stopProducer(stop_producer_msg, timeout=300)
        return clients_dto


def start_client_producer(emulation: str, execution_id: int):
    execution = MetastoreFacade.get_emulation_execution(emulation_name=emulation, ip_first_octet=execution_id)
    kafka_ip = execution.emulation_env_config.kafka_config.container.docker_gw_bridge_ip
    kafka_port = execution.emulation_env_config.kafka_config.kafka_port_external
    client_container_external_ip = \
        execution.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip
    client_manager_port = execution.emulation_env_config.traffic_config.client_population_config.client_manager_port
    time_step_len_seconds = \
        execution.emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds
    with grpc.insecure_channel(f'{client_container_external_ip}:{client_manager_port}') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        start_producer_msg = csle_collector.client_manager.client_manager_pb2.StartProducerMsg(
            ip=kafka_ip, port=kafka_port,
            time_step_len_seconds=time_step_len_seconds
        )
        clients_dto = stub.startProducer(start_producer_msg, timeout=300)
        return clients_dto


if __name__ == '__main__':
    emulation = "csle-level4-020"
    execution_id = 15
    clients = [
        Client(id=0, workflow_distribution=[1],
               arrival_config=ConstantArrivalConfig(lamb=40), mu=4, exponential_service_time=True)
    ]
    # stop_client_producer(emulation=emulation, execution_id=execution_id)
    # time.sleep(2)
    # stop_client_population(emulation=emulation, execution_id=execution_id)
    # time.sleep(2)
    start_client_population(emulation=emulation, execution_id=execution_id, clients=clients)
    time.sleep(2)
    start_client_producer(emulation=emulation, execution_id=execution_id)
