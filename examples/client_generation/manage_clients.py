from typing import List
import time
import grpc
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.client_manager.query_clients
from csle_collector.client_manager.dao.eptmp_arrival_config import EPTMPArrivalConfig
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.client import Client
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution


def stop_client_population(execution: EmulationExecution) \
        -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
    """
    Stops the client population of a given execution

    :param execution: the execution to stop the client population for
    :return: a clientsDTO with details of the clients
    """
    client_container_external_ip = \
        execution.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip
    client_manager_port = execution.emulation_env_config.traffic_config.client_population_config.client_manager_port
    with grpc.insecure_channel(f'{client_container_external_ip}:{client_manager_port}') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        stop_clients_msg = csle_collector.client_manager.client_manager_pb2.StopClientsMsg()
        clients_dto = stub.stopClients(stop_clients_msg)
        return clients_dto


def start_client_population(execution: EmulationExecution, clients: List[Client] = None,
                            workflows_config: WorkflowsConfig = None) \
        -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
    """
    Starts the client population of a given execution

    :param execution: the execution to start the client population of
    :param clients: the client types
    :param workflows_config: the workflows configuration
    :return: a clientsDTO with details of the clients
    """
    if clients is None:
        clients = execution.emulation_env_config.traffic_config.client_population_config.clients
    clients_grpcs = list(map(lambda x: x.to_grpc_object(), clients))
    if workflows_config is None:
        workflows_config = execution.emulation_env_config.traffic_config.client_population_config.workflows_config
    workflows_config_grpc = workflows_config.to_grpc_object()
    start_clients_msg = csle_collector.client_manager.client_manager_pb2.StartClientsMsg(
        time_step_len_seconds=(
            execution.emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds),
        clients=clients_grpcs, workflows_config=workflows_config_grpc)
    client_container_external_ip = \
        execution.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip
    client_manager_port = execution.emulation_env_config.traffic_config.client_population_config.client_manager_port
    with grpc.insecure_channel(f'{client_container_external_ip}:{client_manager_port}') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        clients_dto = stub.startClients(start_clients_msg, timeout=300)
        return clients_dto


def stop_client_producer(execution: EmulationExecution) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
    """
    Stops the producer of client statistics

    :param execution: the execution to stop the producer of
    :return: a clientsDTO with details of the clients
    """
    client_container_external_ip = \
        execution.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip
    client_manager_port = execution.emulation_env_config.traffic_config.client_population_config.client_manager_port
    with grpc.insecure_channel(f'{client_container_external_ip}:{client_manager_port}') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        stop_producer_msg = csle_collector.client_manager.client_manager_pb2.StopProducerMsg()
        clients_dto = stub.stopProducer(stop_producer_msg, timeout=300)
        return clients_dto


def start_client_producer(execution: EmulationExecution) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
    """
    Starts the producer of client statistics

    :param execution: the execution to start the producer of
    :return: a clientsDTO with details of the clients
    """
    kafka_ip = execution.emulation_env_config.kafka_config.container.get_ips()[0]
    kafka_port = execution.emulation_env_config.kafka_config.kafka_port
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
    emulation = "csle-level4-070"
    execution_id = 15
    execution = MetastoreFacade.get_emulation_execution(emulation_name=emulation, ip_first_octet=execution_id)
    # clients = [
    #     Client(id=0, workflow_distribution=[1],
    #            arrival_config=ConstantArrivalConfig(lamb=40), mu=4, exponential_service_time=True)
    # ]
    # clients = [
    #     Client(id=0, workflow_distribution=[1],
    #            arrival_config=EPTMPArrivalConfig(thetas=[3.6269], gammas=[2.1, 1.1], omegas=[0.1731, 0.3264],
    #                                              phis = [-0.6193, 0.5]),
    #            mu=4, exponential_service_time=False)
    # ]

    clients = [
        Client(id=0, workflow_distribution=[1],
               arrival_config=EPTMPArrivalConfig(thetas=[1, 0.003], gammas=[0], omegas=[0], phis=[0]),
               mu=4, exponential_service_time=False)
    ]

    workflows_config = WorkflowsConfig(
        workflow_services=(
            execution.emulation_env_config.traffic_config.client_population_config.workflows_config.workflow_services),
        workflow_markov_chains=[
            WorkflowMarkovChain(
                transition_matrix=[
                    [0.8, 0.2],
                    [0, 1]
                ],
                initial_state=0,
                id=0
            )
        ]
    )
    # stop_client_producer(execution=execution)
    # time.sleep(2)
    # stop_client_population(execution=execution)
    # time.sleep(2)
    start_client_population(execution=execution, clients=clients, workflows_config=workflows_config)
    time.sleep(2)
    start_client_producer(execution=execution)
