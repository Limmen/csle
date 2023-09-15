from typing import Union, Dict, Any
import time
from emukit.model_wrappers.gpy_model_wrappers import GPyModelWrapper
from emukit.core.acquisition.acquisition import Acquisition
from emukit.core.optimization import AcquisitionOptimizerBase
import numpy as np
import numpy.typing as npt


class BOResults:
    """
    DTO representing the state and results of an execution of Bayesian Optimization
    """

    def __init__(self, remaining_budget: float) -> None:
        """
        Initializes the DTO

        :param remaining_budget: the remaining budget of the BO execution
        """
        self.remaining_budget: float = remaining_budget
        self.evaluation_budget: float = remaining_budget
        self.X: npt.NDArray[Any] = np.array([])
        self.Y: npt.NDArray[Any] = np.array([])
        self.X_best: npt.NDArray[Any] = np.array([])
        self.Y_best: npt.NDArray[Any] = np.array([])
        self.C: npt.NDArray[Any] = np.array([])
        self.cumulative_cost: float = 0.
        self.start_time: float = time.time()
        self.iteration: int = 0
        self.total_time: float = 0
        self.surrogate_model: Union[GPyModelWrapper, None] = None
        self.acquisition: Union[Acquisition, None] = None
        self.acquisition_optimizer: Union[AcquisitionOptimizerBase, None] = None
        self.X_objective: npt.NDArray[Any] = np.array([])
        self.Y_objective: npt.NDArray[Any] = np.array([])
        self.y_opt = 0

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"remaining_budget: {self.remaining_budget}, X: {self.X}, Y: {self.Y}, X_best: {self.X_best}, " \
               f"Y_best: {self.Y_best}, C: {self.C}, cumulative_cost: {self.cumulative_cost}, " \
               f"iteration: {self.iteration}, total_time: {self.total_time}, surrogate_model{self.surrogate_model}," \
               f"acquisition: {self.acquisition}, acquisition_optimizer: {self.acquisition_optimizer}, " \
               f"X_objective: {self.X_objective}, Y_objective: {self.Y_objective}, y_opt: {self.y_opt}," \
               f" evaluation_budget: {self.evaluation_budget}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BOResults":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = BOResults(remaining_budget=d["remaining_budget"])
        obj.X = np.array(d["X"])
        obj.Y = np.array(d["Y"])
        obj.X_best = np.array(d["X_best"])
        obj.Y_best = np.array(d["Y_best"])
        obj.X_objective = np.array(d["X_objective"])
        obj.Y_objective = np.array(d["Y_objective"])
        obj.C = np.array(d["C"])
        obj.cumulative_cost = d["cumulative_cost"]
        obj.start_time = d["start_time"]
        obj.iteration = d["iteration"]
        obj.total_time = d["total_time"]
        obj.y_opt = d["y_opt"]
        obj.evaluation_budget = d["evaluation_budget"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["remaining_budget"] = self.remaining_budget
        d["X"] = list(self.X.copy().tolist())
        d["Y"] = list(self.Y.copy().tolist())
        d["X_best"] = list(self.X_best.copy().tolist())
        d["Y_best"] = list(self.Y_best.copy().tolist())
        d["C"] = list(self.C.copy().tolist())
        d["start_time"] = self.start_time
        d["iteration"] = self.iteration
        d["total_time"] = self.total_time
        d["surrogate_model"] = ""
        d["acquisition"] = ""
        d["acquisition_optimizer"] = ""
        d["X_objective"] = list(self.X_objective.copy().tolist())
        d["Y_objective"] = list(self.Y_objective.copy().tolist())
        d["y_opt"] = self.y_opt
        d["cumulative_cost"] = self.cumulative_cost
        d["evaluation_budget"] = self.evaluation_budget
        return d

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
    def from_json_str(json_str: str) -> "BOResults":
        """
        Converts json string into a DTO

        :param json_str: the json string representation
        :return: the DTO instance
        """
        import json
        dto: BOResults = BOResults.from_dict(json.loads(json_str))
        return dto

    @staticmethod
    def from_json_file(json_file_path: str) -> "BOResults":
        """
        Reads a json file and converts it into a dto

        :param json_file_path: the json file path to load the DTO from
        :return: the loaded DTO
        """
        import io
        with io.open(json_file_path, 'r', encoding='utf-8') as f:
            json_str = f.read()
            dto = BOResults.from_json_str(json_str=json_str)
            return dto

    def copy(self) -> "BOResults":
        """
        :return: a copy of the DTO
        """
        return BOResults.from_dict(self.to_dict())
