from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
from typing import Dict, Any


class ArrivalConfig():
    """
    Abstract arrival configuration class
    """

    def __init__(self, client_arrival_type: ClientArrivalType) -> None:
        """
        Initializes the object

        :param client_arrival_type: the type of the arrival configuration
        """
        self.client_arrival_type = client_arrival_type

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d = {}
        d["client_arrival_type"] = self.client_arrival_type
        return d
