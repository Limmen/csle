from typing import Union
import time
import logging
import grpc
from concurrent import futures
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.threads.arrival_thread import ArrivalThread
from csle_collector.client_manager.threads.producer_thread import ProducerThread
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.constants.constants as constants


class ClientManagerServicer(csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerServicer):
    """
    gRPC server for managing the running clients. Allows to start/stop clients remotely and also to query the
    state of the clients.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        self.arrival_thread: Union[None, ArrivalThread] = None
        self.producer_thread: Union[None, ProducerThread] = None
        logging.basicConfig(filename=f"{constants.LOG_FILES.CLIENT_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.CLIENT_MANAGER_LOG_FILE}", level=logging.INFO)

    def get_arrival_thread(self) -> Union[None, ArrivalThread]:
        """
        Gets the arrival thread

        :return: The arrival thread if it is initialized, otherwise None
        """
        return self.arrival_thread

    def get_producer_thread(self) -> Union[None, ProducerThread]:
        """
        Gets the producer thread

        :return: The producer thread if it is initialized, otherwise None
        """
        return self.producer_thread

    def getClients(self, request: csle_collector.client_manager.client_manager_pb2.GetClientsMsg,
                   context: grpc.ServicerContext) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Gets the state of the clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info("Getting client information")
        num_clients = 0
        clients_time_step_len_seconds = 0.0
        producer_time_step_len_seconds = 0.0
        arrival_thread = self.get_arrival_thread()
        producer_thread = self.get_producer_thread()

        client_process_active = False
        if arrival_thread is not None:
            num_clients = len(arrival_thread.client_threads)
            client_process_active = True
            clients_time_step_len_seconds = arrival_thread.time_step_len_seconds

        producer_active = False
        if producer_thread is not None:
            producer_active = True
            producer_time_step_len_seconds = producer_thread.time_step_len_seconds

        clients_dto = csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients=num_clients, client_process_active=client_process_active, producer_active=producer_active,
            clients_time_step_len_seconds=int(clients_time_step_len_seconds),
            producer_time_step_len_seconds=int(producer_time_step_len_seconds))
        return clients_dto

    def stopClients(self, request: csle_collector.client_manager.client_manager_pb2.StopClientsMsg,
                    context: grpc.ServicerContext):
        """
        Stops the Poisson-process that generates new clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info("Stopping clients")

        clients_time_step_len_seconds = 0.0
        producer_time_step_len_seconds = 0.0
        producer_thread = self.get_producer_thread()
        arrival_thread = self.get_producer_thread()

        if arrival_thread is not None:
            clients_time_step_len_seconds = arrival_thread.time_step_len_seconds
            arrival_thread.stopped = True
            time.sleep(1)
        self.arrival_thread = None

        producer_active = False
        if producer_thread is not None:
            producer_active = True
            producer_time_step_len_seconds = producer_thread.time_step_len_seconds

        return csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients=0, client_process_active=False, producer_active=producer_active,
            clients_time_step_len_seconds=int(clients_time_step_len_seconds),
            producer_time_step_len_seconds=int(producer_time_step_len_seconds))

    def startClients(self, request: csle_collector.client_manager.client_manager_pb2.StartClientsMsg,
                     context: grpc.ServicerContext) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Starts/Restarts the Poisson process(es) that generate(s) clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        clients = list(map(lambda x: Client.from_grpc_object(x), request.clients))
        workflows_config = WorkflowsConfig.from_grpc_object(request.workflows_config)
        logging.info(f"Starting clients, num clients:{len(clients)}, "
                     f"num workflows: {len(workflows_config.workflow_markov_chains)}, "
                     f"num services: {len(workflows_config.workflow_services)}, "
                     f"client types: {list(map(lambda x: str(x), clients))},"
                     f"workflow markov chains: {list(map(lambda x: str(x), workflows_config.workflow_markov_chains))},"
                     f"workflow services: {list(map(lambda x: str(x), workflows_config.workflow_services))},"
                     f"\n commands: {workflows_config.commands()}")
        producer_time_step_len_seconds = 0
        arrival_thread = self.get_arrival_thread()
        producer_thread = self.get_producer_thread()
        if arrival_thread is not None:
            arrival_thread.stopped = True
            time.sleep(1)
        if request.time_step_len_seconds <= 0:
            request.time_step_len_seconds = 1
        arrival_thread = ArrivalThread(time_step_len_seconds=request.time_step_len_seconds, clients=clients,
                                       workflows_config=workflows_config)
        arrival_thread.start()
        self.arrival_thread = arrival_thread
        clients_time_step_len_seconds = request.time_step_len_seconds
        producer_active = False
        if producer_thread is not None:
            producer_active = True
            producer_time_step_len_seconds = producer_thread.time_step_len_seconds
        clients_dto = csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients=0, client_process_active=True, producer_active=producer_active,
            clients_time_step_len_seconds=int(clients_time_step_len_seconds),
            producer_time_step_len_seconds=producer_time_step_len_seconds)
        return clients_dto

    def startProducer(self, request: csle_collector.client_manager.client_manager_pb2.StartProducerMsg,
                      context: grpc.ServicerContext) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Starts/Restarts the producer thread that pushes data to Kafka

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        clients_time_step_len_seconds = 0.0
        producer_thread = self.get_producer_thread()
        arrival_thread = self.get_arrival_thread()
        logging.info(f"Starting producer, time-step len:{request.time_step_len_seconds}s, "
                     f"arrival_thread: {arrival_thread}")

        time.sleep(5)
        if producer_thread is not None:
            producer_thread.stopped = True
            time.sleep(1)
        if request.time_step_len_seconds <= 0:
            request.time_step_len_seconds = 1
        if arrival_thread is None:
            raise ValueError("Cannot start producer if the arrival thread is not started")
        producer_thread = ProducerThread(arrival_thread=arrival_thread,
                                         time_step_len_seconds=request.time_step_len_seconds,
                                         ip=request.ip, port=request.port)
        producer_thread.start()
        self.producer_thread = producer_thread
        client_process_active = False
        num_clients = 0
        if arrival_thread is not None:
            num_clients = len(arrival_thread.client_threads)
            client_process_active = True
            clients_time_step_len_seconds = arrival_thread.time_step_len_seconds
        clients_dto = csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients=num_clients, client_process_active=client_process_active, producer_active=True,
            clients_time_step_len_seconds=int(clients_time_step_len_seconds),
            producer_time_step_len_seconds=request.time_step_len_seconds)
        return clients_dto

    def stopProducer(self, request: csle_collector.client_manager.client_manager_pb2.StopProducerMsg,
                     context: grpc.ServicerContext) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Stops the producer thread that pushes data to Kafka

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info("Stopping producer")
        clients_time_step_len_seconds = 0.0
        producer_thread = self.get_producer_thread()
        arrival_thread = self.get_arrival_thread()

        if producer_thread is not None:
            producer_thread.stopped = True
            time.sleep(1)
        self.producer_thread = None
        client_process_active = False
        num_clients = 0
        if arrival_thread is not None:
            num_clients = len(arrival_thread.client_threads)
            client_process_active = True
            clients_time_step_len_seconds = arrival_thread.time_step_len_seconds
        clients_dto = csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients=num_clients, client_process_active=client_process_active, producer_active=False,
            clients_time_step_len_seconds=int(clients_time_step_len_seconds), producer_time_step_len_seconds=0)
        return clients_dto


def serve(port: int = 50044, log_dir: str = "/", log_file_name: str = "client_manager.log",
          max_workers: int = 10) -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.CLIENT_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.CLIENT_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.client_manager.client_manager_pb2_grpc.add_ClientManagerServicer_to_server(
        ClientManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"ClientManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
