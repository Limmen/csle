from typing import List
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.constants.constants as constants


def get_clients(stub: csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub,
                timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
    """
    Queries the server for the client state

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a clientsDTO describing the state of the clients
    """
    get_clients_dto_msg = csle_collector.client_manager.client_manager_pb2.GetClientsMsg()
    clients_dto = stub.getClients(get_clients_dto_msg)
    return clients_dto


def stop_clients(stub: csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub,
                 timeout=constants.GRPC.TIMEOUT_SECONDS):
    """
    Stops the client arrival process

    :param stub: the stub to the gRPC server
    :param timeout: the GRPC timeout (seconds)
    :return: a clientsDTO describing the state of the clients
    """
    stop_clients_msg = csle_collector.client_manager.client_manager_pb2.StopClientsMsg()
    clients_dto = stub.stopClients(stop_clients_msg)
    return clients_dto


def start_clients(stub: csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub,
                  mu: float, lamb: float, time_step_len_seconds: int, commands: List[str], num_commands: int = 2,
                  sine_modulated: bool = False, time_scaling_factor: float = 0.01, period_scaling_factor: float = 20,
                  timeout=constants.GRPC.TIMEOUT_SECONDS):
    """
    Starts the client arrival process

    :param stub: the stub to the gRPC server
    :param mu: the mu parameter for the Exponential service time
    :param lamb: the lambda parameter for the Poisson process
    :param time_step_len_seconds: the length of a time-step for simulating the arrival process
    :param num:commands: the number of commands that each client will use
    :param sine_modulated: whether the arrival process is sine modulated or not
    :param time_scaling_factor: the time scaling factor for the sine modulated arrival process
    :param period_scaling_factor: the period scaling factor for the sine modulated arrival process
    :param timeout: the GRPC timeout (seconds)
    :return: a clientsDTO describing the state of the clients
    """
    start_clients_msg = csle_collector.client_manager.client_manager_pb2.StartClientsMsg(
        mu=mu, lamb=lamb, time_step_len_seconds=time_step_len_seconds, commands=commands,
        num_commands=num_commands, sine_modulated=sine_modulated, period_scaling_factor=period_scaling_factor,
        time_scaling_factor=time_scaling_factor
    )
    clients_dto = stub.startClients(start_clients_msg)
    return clients_dto


def stop_producer(stub: csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub,
                  timeout=constants.GRPC.TIMEOUT_SECONDS):
    """
    Stops the producer process

    :param stub: the stub to the gRPC server
    :param timeout: the GRPC timeout (seconds)
    :return: a clientsDTO describing the state of the clients
    """
    stop_producer_msg = csle_collector.client_manager.client_manager_pb2.StopProducerMsg()
    clients_dto = stub.stopProducer(stop_producer_msg, timeout=timeout)
    return clients_dto


def start_producer(stub: csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub, ip: str, port: int,
                   time_step_len_seconds: int, timeout=constants.GRPC.TIMEOUT_SECONDS):
    """
    Stops the producer process

    :param stub: the stub to the gRPC server
    :param ip: ip of the kafka server to produce to
    :param port: port of the kafka server to produce to
    :param timeout: the GRPC timeout (seconds)
    :return: a clientsDTO describing the state of the clients
    """
    start_producer_msg = csle_collector.client_manager.client_manager_pb2.StartProducerMsg(
        ip=ip,
        port=port,
        time_step_len_seconds=time_step_len_seconds
    )
    clients_dto = stub.startProducer(start_producer_msg, timeout=timeout)
    return clients_dto
