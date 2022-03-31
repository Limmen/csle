from typing import List
import json
import os
import numpy as np
import csle_common.constants.constants as constants


class SimulationTrajectory:
    """
    Class that represents a trajectory in the simulation system
    """

    def __init__(self):
        """
        Initializes the DTO
        """
        self.attacker_rewards = []
        self.defender_rewards = []
        self.attacker_observations = []
        self.defender_observations = []
        self.infos = []
        self.dones = []
        self.attacker_actions = []
        self.defender_actions = []
        self.states = []
        self.beliefs = []
        self.infrastructure_metrics = []

    def __str__(self) -> str:
        """
        :return: a string representation of the trajectory
        """
        return "attacker_rewards:{}, defender_rewards:{}, attacker_observations:{}, defender_observations:{}, " \
               "infos:{}, dones:{}, attacker_actions:{}, defender_actions:{}, states: {}, beliefs: {}, " \
               "infrastructure_metrics: {}".format(
            self.attacker_rewards, self.defender_rewards, self.attacker_observations,
            self.defender_observations, self.infos, self.dones, self.attacker_actions,
            self.defender_actions, self.states, self.beliefs, self.infrastructure_metrics)

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the trajectory
        """
        return {
            "attacker_rewards": self.attacker_rewards,
            "defender_rewards": self.defender_rewards,
            "attacker_observations": self.attacker_observations,
            "defender_observations": self.defender_observations,
            "infos": self.infos,
            "dones": self.dones,
            "attacker_actions": self.attacker_actions,
            "defender_actions": self.defender_actions,
            "states": self.states,
            "beliefs": self.beliefs,
            "infrastructure_metrics": self.infrastructure_metrics
        }

    @staticmethod
    def from_dict(d: dict) -> "SimulationTrajectory":
        """
        Converts a dict representation of the trajectory to a DTO representation

        :param d: the dict to convert
        :return: the trajectory DTO
        """
        trajectory = SimulationTrajectory()
        if "attacker_rewards" in d:
            trajectory.attacker_rewards = d["attacker_rewards"]
        if "defender_rewards" in d:
            trajectory.defender_rewards = d["defender_rewards"]
        if "attacker_observations" in d:
            trajectory.attacker_observations = d["attacker_observations"]
        if "defender_observations" in d:
            trajectory.defender_observations = d["defender_observations"]
        if "infos" in d:
            trajectory.infos = d["infos"]
        if "dones" in d:
            trajectory.dones = d["dones"]
        if "attacker_actions" in d:
            trajectory.attacker_actions = d["attacker_actions"]
        if "defender_actions" in d:
            trajectory.defender_actions = d["defender_actions"]
        if "beliefs" in d:
            trajectory.beliefs = d["beliefs"]
        if "states" in d:
            trajectory.states = d["states"]
        if "infrastructure_metrics" in d:
            trajectory.infrastructure_metrics = d["infrastructure_metrics"]
        return trajectory

    @staticmethod
    def save_trajectories(trajectories_save_dir, trajectories : List["SimulationTrajectory"],
                          trajectories_file : str = None) -> None:
        """
        Utility function for saving a list of trajectories to a json file

        :param trajectories_save_dir: the directory where to save the trajectories
        :param trajectories: the trajectories to save
        :param trajectories_file: the filename of the trajectories file
        :return: None
        """
        if trajectories_file is None:
            trajectories_file =  constants.SYSTEM_IDENTIFICATION.TRAJECTORIES_FILE
        trajectories = list(map(lambda x: x.to_dict(), trajectories))
        if not os.path.exists(trajectories_save_dir):
            os.makedirs(trajectories_save_dir)
        with open(trajectories_save_dir + constants.COMMANDS.SLASH_DELIM + trajectories_file, 'w') as fp:
            json.dump({"trajectories": trajectories}, fp, cls=NpEncoder)

    @staticmethod
    def load_trajectories(trajectories_save_dir, trajectories_file : str = None) -> List["SimulationTrajectory"]:
        """
        Utility function for loading and parsing a list of trajectories from a json file

        :param trajectories_save_dir: the directory where to load the trajectories from
        :param trajectories_file: (optional) a custom name of the trajectories file
        :return: a list of the loaded trajectories
        """
        if trajectories_file is None:
            trajectories_file =  constants.SYSTEM_IDENTIFICATION.TRAJECTORIES_FILE
        path = trajectories_save_dir + constants.COMMANDS.SLASH_DELIM + trajectories_file
        if os.path.exists(path):
            with open(path, 'r') as fp:
                d = json.load(fp)
                trajectories  = d["trajectories"]
                trajectories = list(map(lambda x: SimulationTrajectory.from_dict(x), trajectories))
                return trajectories
        else:
            print("Warning: Could not read trajectories file, path does not exist:{}".format(path))
            return []


class NpEncoder(json.JSONEncoder):
    """
    Encoder for Numpy arrays to JSON
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)