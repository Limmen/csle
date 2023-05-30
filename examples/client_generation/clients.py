import time
from typing import List
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.client_manager.query_clients
import grpc


def stop_client_population():
    with grpc.insecure_channel(f'172.18.0.3:50044') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        stop_clients_msg = csle_collector.client_manager.client_manager_pb2.StopClientsMsg()
        clients_dto = stub.stopClients(stop_clients_msg)
        return clients_dto


def start_client_population(mu: float, lamb: float, time_step_len_seconds: int, commands : List[str],
                            sine_modulated: bool, num_commands: int, period_scaling_factor: float,
                            time_scaling_factor: float):
    # Open a gRPC session
    with grpc.insecure_channel(f'172.18.0.3:50044') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        start_clients_msg = csle_collector.client_manager.client_manager_pb2.StartClientsMsg(
            mu=mu, lamb=lamb, time_step_len_seconds=time_step_len_seconds, commands=commands,
            num_commands=num_commands, sine_modulated=sine_modulated, period_scaling_factor=period_scaling_factor,
            time_scaling_factor=time_scaling_factor
        )
        clients_dto = stub.startClients(start_clients_msg, timeout=300)
        return clients_dto


def stop_client_producer():
    with grpc.insecure_channel(f'172.18.0.3:50044') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        stop_producer_msg = csle_collector.client_manager.client_manager_pb2.StopProducerMsg()
        clients_dto = stub.stopProducer(stop_producer_msg, timeout=300)
        return clients_dto

def start_client_producer(kafka_ip: str, kafka_port: int, time_step_len_seconds: int):
    with grpc.insecure_channel(f'172.18.0.3:50044') as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        start_producer_msg = csle_collector.client_manager.client_manager_pb2.StartProducerMsg(
            ip=kafka_ip, port=kafka_port,
            time_step_len_seconds=time_step_len_seconds
        )
        clients_dto = stub.startProducer(start_producer_msg, timeout=300)
        return clients_dto

if __name__ == '__main__':
    print("Stopping client population..")
    stop_client_population()
    print("client population stopped")
    time.sleep(20)
    print("Starting client population")
    start_client_population(lamb=20, mu=4, num_commands=2, time_scaling_factor=0.01, period_scaling_factor=20,
                            time_step_len_seconds=30, sine_modulated=True, commands = [
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1".format("15.4.2.21"),
            "timeout 5 snmpwalk -v2c {} -c csle_1234 > /dev/null 2>&1".format("15.4.2.21"),
            "timeout 10 /irc_login_test.sh {} > /dev/null 2>&1".format("15.4.2.21"),
            "timeout 5 psql -h {} -p 5432 > /dev/null 2>&1".format("15.4.2.21"),
            "timeout 5 ping {} > /dev/null 2>&1".format("15.4.2.21"),
            "timeout 5 traceroute {} > /dev/null 2>&1".format("15.4.2.21"),
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1".format("15.4.2.10"),
            "timeout 5 ping {} > /dev/null 2>&1".format("15.4.2.10"),
            "timeout 5 traceroute {} > /dev/null 2>&1".format("15.4.2.10"),
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1".format("15.4.2.78"),
            "timeout 5 curl {}:80 > /dev/null 2>&1".format("15.4.2.78"),
            "timeout 5 ping {} > /dev/null 2>&1".format("15.4.2.78"),
            "timeout 5 traceroute {} > /dev/null 2>&1".format("15.4.2.78"),
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1".format("15.4.2.3"),
            "timeout 5 curl {} > /dev/null 2>&1".format("15.4.2.3"),
            "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {} > /dev/null 2>&1".format("15.4.2.3"),
            "timeout 5 ping {} > /dev/null 2>&1".format("15.4.2.3"),
            "timeout 5 traceroute {} > /dev/null 2>&1".format("15.4.2.3"),
            "timeout 5 ftp {} > /dev/null 2>&1".format("15.4.2.79"),
            "timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1".format("15.4.2.79"),
            "timeout 5 curl {}:8080 > /dev/null 2>&1".format("15.4.2.79"),
            "timeout 5 ping {} > /dev/null 2>&1".format("15.4.2.79"),
            "timeout 5 traceroute {} > /dev/null 2>&1".format("15.4.2.79")
        ])
    print("Client population started")
    time.sleep(20)
    print("Stopping the client producer")
    stop_client_producer()
    print("Client producer stopped")
    time.sleep(20)
    print("Starting the client producer")
    start_client_producer(kafka_ip="15.4.253.253", kafka_port=9092, time_step_len_seconds=30)
    print("Client producer started")