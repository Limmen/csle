import grpc
import csle_common.constants.constants as constants
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.query_clients

if __name__ == '__main__':
    ip = "172.18.0.3"
    port = 50044

    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
        status = csle_collector.client_manager.query_clients.get_clients(stub=stub)
        print(f"Number of clients: {status.num_clients}, client process active: {status.client_process_active}, "
              f"producer active: {status.producer_active}, "
              f"clients time step length: {status.clients_time_step_len_seconds}, "
              f"producer time step length: {status.producer_time_step_len_seconds}")
