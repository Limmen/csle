from typing import List, Dict, Any
import random
import numpy as np


class WorkflowMarkovChain:
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
        cumsum = np.cumsum(row) # cumulative sum of probabilities
        r = random.random() # random number between 0 and 1
        for i in range(len(cumsum)):
            if r < cumsum[i]: # find the first index where r is smaller than cumsum[i]
                return i # return that index as the outcome

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
        :return: a dict representation of the object
        """
        d = {}
        d["transition_matrix"] = self.transition_matrix
        d["initial_state"] = self.initial_state
        d["current_state"] = self.current_state
        d["t"] = self.t
        d["id"] = self.id
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