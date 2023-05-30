from typing import Dict, Any


class SineArrivalConfig:
    """
    DTO representing the configuration of a sine-modulated poisson arrival process withb exponential service times
    """

    def __init__(self, lamb: float, mu: float, time_scaling_factor: float, period_scaling_factor: float):
        """
        Initializes the object

        :param lamb: the static arrival rate
        :param mu: the mean service time
        :param time_scaling_factor: the time-scaling factor for sine-modulated arrival processes
        :param period_scaling_factor: the period-scaling factor for sine-modulated arrival processes
        """
        self.lamb = lamb
        self.mu = mu
        self.time_scaling_factor = time_scaling_factor
        self.period_scaling_factor = period_scaling_factor

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"lamb: {self.lamb}, mu: {self.mu}, time_scaling_factor: {self.time_scaling_factor}, " \
               f"period_scaling_factor: {self.period_scaling_factor}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["lamb"] = self.lamb
        d["mu"] = self.mu
        d["time_scaling_factor"] = self.time_scaling_factor
        d["period_scaling_factor"] = self.period_scaling_factor
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SineArrivalConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = SineArrivalConfig(lamb=d["lamb"], mu=d["mu"], time_scaling_factor=d["time_scaling_factor"],
                                period_scaling_factor=d["period_scaling_factor"])
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
    def from_json_file(json_file_path: str) -> "SineArrivalConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SineArrivalConfig.from_dict(json.loads(json_str))