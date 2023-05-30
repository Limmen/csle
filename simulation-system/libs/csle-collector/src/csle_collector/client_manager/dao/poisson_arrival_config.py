from typing import Dict, Any


class PoissonArrivalConfig:
    """
    DTO representing the configuration of a stationary poisson arrival process with exponential service times
    """

    def __init__(self, lamb: float, mu: float):
        """
        Initializes the object

        :param lamb: the static arrival rate
        :param mu: the mean service time
        """
        self.lamb = lamb
        self.mu = mu

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"lamb: {self.lamb}, mu: {self.mu}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["lamb"] = self.lamb
        d["mu"] = self.mu
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PoissonArrivalConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = PoissonArrivalConfig(lamb=d["lamb"], mu=d["mu"])
        return obj

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    @staticmethod
    def from_json_file(json_file_path: str) -> "PoissonArrivalConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return PoissonArrivalConfig.from_dict(json.loads(json_str))