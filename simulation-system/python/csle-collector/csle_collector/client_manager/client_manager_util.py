from typing import Dict, Any
import csle_collector.client_manager.client_manager_pb2


class ClientManagerUtil:
    """
    Class with utility functions related to the Client Manager
    """

    @staticmethod
    def client_dto_to_dict(clients_dto: csle_collector.client_manager.client_manager_pb2.ClientsDTO) \
            -> Dict[str, Any]:
        """
        Converts a ClientsDTO to a dict

        :param clients_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["num_clients"] = clients_dto.num_clients
        d["client_process_active"] = clients_dto.client_process_active
        d["producer_active"] = clients_dto.producer_active
        d["clients_time_step_len_seconds"] = clients_dto.clients_time_step_len_seconds
        d["producer_time_step_len_seconds"] = clients_dto.producer_time_step_len_seconds
        return d

    @staticmethod
    def clients_dto_from_dict(d: Dict[str, Any]) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Converts a dict representation of a ClientsDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        clients_dto = csle_collector.client_manager.client_manager_pb2.ClientsDTO()
        clients_dto.num_clients = d["num_clients"]
        clients_dto.client_process_active = d["client_process_active"]
        clients_dto.producer_active = d["producer_active"]
        clients_dto.clients_time_step_len_seconds = d["clients_time_step_len_seconds"]
        clients_dto.producer_time_step_len_seconds = d["producer_time_step_len_seconds"]
        return clients_dto

    @staticmethod
    def clients_dto_empty() -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        :return: an empty ClientsDTO
        """
        clients_dto = csle_collector.client_manager.client_manager_pb2.ClientsDTO()
        clients_dto.num_clients = 0
        clients_dto.client_process_active = False
        clients_dto.producer_active = False
        clients_dto.clients_time_step_len_seconds = 0
        clients_dto.producer_time_step_len_seconds = 0
        return clients_dto
