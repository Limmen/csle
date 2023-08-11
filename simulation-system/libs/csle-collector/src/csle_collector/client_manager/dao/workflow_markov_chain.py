from typing import List, Dict, Any
import random
import numpy as np
import csle_collector.client_manager.client_manager_pb2
from csle_base.json_serializable import JSONSerializable
from csle_base.grpc_serializable import GRPCSerializable


class WorkflowMarkovChain(JSONSerializable, GRPCSerializable):
    """
    A Markov chain representation of a workflow.
    """

    def __init__(self, transition_matrix: List[List[float]], initial_state: int, id: int) -> None:
        """
        Initializes the object

        :param transition_matrix: the transition matrix of the workflow Markov chain (row-stochastic)
        :param initial_state: the initial state of the Markov chain
        :param id: the id of the workflow
        """
        self.transition_matrix = transition_matrix
        for i in range(len(transition_matrix)):
            assert round(sum(self.transition_matrix[i]), 3) == 1
        self.initial_state = initial_state
        self.current_state = initial_state
        self.t = 0
        self.id = id

    def step_forward(self) -> int:
        """
        Move t forward by one and possibly transition to a new state.
        Returns the new state.
        """
        self.t += 1
        next_state = WorkflowMarkovChain.markov_next_state(row=self.transition_matrix[self.current_state])
        self.current_state = next_state
        return self.current_state

    def reset(self) -> None:
        """
        Resets the Markov chain

        :return: None
        """
        self.current_state = self.initial_state
        self.t = 0

    @staticmethod
    def markov_next_state(row: List[float]) -> int:
        """
        Samples the next state of the Markov chain

        :param row: a numpy array of probabilities that sum up to 1.
        :return:  an integer from 0 to len(row)-1.
        """
        cumsum = np.cumsum(row)  # cumulative sum of probabilities
        r = random.random()  # random number between 0 and 1
        for i in range(len(cumsum)):
            if r < cumsum[i]:  # find the first index where r is smaller than cumsum[i]
                return i  # return that index as the outcome
        raise ValueError("Invalid transition probabilities")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "WorkflowMarkovChain":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = WorkflowMarkovChain(transition_matrix=d["transition_matrix"], initial_state=d["initial_state"],
                                  id=d["id"])
        obj.current_state = d["current_state"]
        obj.t = d["t"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["transition_matrix"] = self.transition_matrix
        d["initial_state"] = self.initial_state
        d["current_state"] = self.current_state
        d["t"] = self.t
        d["id"] = self.id
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "WorkflowMarkovChain":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return WorkflowMarkovChain.from_dict(json.loads(json_str))

    def copy(self) -> "WorkflowMarkovChain":
        """
        :return: a copy of the DTO
        """
        return WorkflowMarkovChain.from_dict(self.to_dict())

    def to_grpc_object(self) -> csle_collector.client_manager.client_manager_pb2.WorkflowMarkovChainDTO:
        """
        :return: a GRPC serializable version of the object
        """
        rows = []
        for i in range(len(self.transition_matrix)):
            rows.append(csle_collector.client_manager.client_manager_pb2.ProbabilityDistributionDTO(
                probabilities=self.transition_matrix[i]))
        transition_matrix = csle_collector.client_manager.client_manager_pb2.TransitionMatrixDTO(rows=rows)
        return csle_collector.client_manager.client_manager_pb2.WorkflowMarkovChainDTO(
            initial_state=self.initial_state, id=self.id, transition_matrix=transition_matrix)

    @staticmethod
    def from_grpc_object(obj: csle_collector.client_manager.client_manager_pb2.WorkflowMarkovChainDTO) \
            -> "WorkflowMarkovChain":
        """
        Instantiates the object from a GRPC DTO

        :param obj: the object to instantiate from
        :return: the instantiated object
        """
        transition_matrix = []
        for i in range(len(obj.transition_matrix.rows)):
            transition_matrix.append(list(obj.transition_matrix.rows[i].probabilities))
        return WorkflowMarkovChain(id=obj.id, initial_state=obj.initial_state, transition_matrix=transition_matrix)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"Workflow MC, id: {self.id}, initial_state: {self.initial_state}, " \
               f"transition_matrix: {self.transition_matrix}"
