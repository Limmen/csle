from typing import Tuple
import logging
import os
import subprocess
from concurrent import futures
import grpc
import socket
import csle_collector.traffic_manager.traffic_manager_pb2_grpc
import csle_collector.traffic_manager.traffic_manager_pb2
import csle_collector.constants.constants as constants


class TrafficManagerServicer(csle_collector.traffic_manager.traffic_manager_pb2_grpc.TrafficManagerServicer):
    """
    gRPC server for managing a traffic generator. Allows to start/stop the script and also to query the
    state of the script.
    """

    def __init__(self, ip : str=None, hostname :str = None,) -> None:
        """
        Initializes the server

        :param ip: the ip of the traffic manager
        :param hostname: the hostname of the traffic manager
        """
        logging.basicConfig(filename=f"/{constants.LOG_FILES.TRAFFIC_MANAGER_LOG_FILE}", level=logging.INFO)
        self.ip = ip
        self.hostname = hostname
        if self.hostname is None:
            self.hostname = socket.gethostname()
        if self.ip is None:
            self.ip = socket.gethostbyname(self.hostname)
        logging.info(f"Setting up TrafficManager hostname: {self.hostname} ip: {self.ip}")

    def _get_traffic_status(self) -> bool:
        """
        Utility method to get the status of the traffic generator script

        :return: status of the traffic generator
        """
        cmd = "ps -aux | grep traffic_generator"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        output = str(output)
        running = "traffic_generator.sh" in output
        return running

    def getTrafficStatus(self, request: csle_collector.traffic_manager.traffic_manager_pb2.GetTrafficStatusMsg,
                       context: grpc.ServicerContext) \
            -> csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO:
        """
        Gets the state of the traffic manager

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a TrafficDTO with the state of the traffic manager
        """
        running = self._get_traffic_status()
        traffic_dto = csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO(running=running)
        return traffic_dto

    def stopTraffic(self, request: csle_collector.traffic_manager.traffic_manager_pb2.StartTrafficMsg,
                    context: grpc.ServicerContext):
        """
        Stops the traffic generator

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a traffic DTO with the state of the traffic generator
        """
        logging.info("Stopping the traffic generator script")
        cmd = "sudo pkill -f traffic_generator.sh"
        os.system(cmd)
        return csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO(running=False)

    def startTraffic(self, request: csle_collector.traffic_manager.traffic_manager_pb2.StartTrafficMsg,
                     context: grpc.ServicerContext) -> csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO:
        """
        Starts the traffic generator

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a TrafficDTO with the state of the traffic generator
        """
        logging.info(f"Starting the traffic generator")
        cmd = "sudo nohup /traffic_generator.sh &"
        os.system(cmd)
        traffic_dto = csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO(running=True)
        return traffic_dto


def serve(port : int = 50043, ip=None, hostname=None) -> None:
    """
    Starts the gRPC server for managing traffic scripts

    :param port: the port that the server will listen to
    :return: None
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    csle_collector.traffic_manager.traffic_manager_pb2_grpc.add_TrafficManagerServicer_to_server(
        TrafficManagerServicer(hostname=hostname, ip=ip), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"TrafficManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve(port=50043)