from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType


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
