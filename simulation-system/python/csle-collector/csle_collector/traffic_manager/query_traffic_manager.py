import csle_collector.traffic_manager.traffic_manager_pb2_grpc
import csle_collector.traffic_manager.traffic_manager_pb2


def get_traffic_status(stub: csle_collector.traffic_manager.traffic_manager_pb2_grpc.TrafficManagerStub) \
        -> csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO:
    """
    Queries the server for the Traffic generator status

    :param stub: the stub to send the remote gRPC to the server
    :return: a TrafficDTO describing the status of the traffic generator
    """
    get_traffic_status_msg = csle_collector.traffic_manager.traffic_manager_pb2.GetTrafficStatusMsg()
    traffic_dto = stub.getTrafficStatus(get_traffic_status_msg)
    return traffic_dto


def stop_traffic(stub: csle_collector.traffic_manager.traffic_manager_pb2_grpc.TrafficManagerStub) \
        -> csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO:
    """
    Sends a request to the traffic manager to stop the traffic generator

    :param stub: the stub to send the remote gRPC to the server
    :return: a TrafficDTO describing the status of the traffic generator
    """
    stop_traffic_msg = csle_collector.traffic_manager.traffic_manager_pb2.StopTrafficMsg()
    traffic_dto = stub.stopTraffic(stop_traffic_msg)
    return traffic_dto


def start_traffic(stub: csle_collector.traffic_manager.traffic_manager_pb2_grpc.TrafficManagerStub) \
        -> csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO:
    """
    Sends a request to the traffic manager to start the traffic generator script

    :param stub: the stub to send the remote gRPC to the server
    :return: an TrafficDTO describing the status of the traffic manager
    """
    start_traffic_msg = csle_collector.traffic_manager.traffic_manager_pb2.StartTrafficMsg()
    traffic_dto = stub.startTraffic(start_traffic_msg)
    return traffic_dto
