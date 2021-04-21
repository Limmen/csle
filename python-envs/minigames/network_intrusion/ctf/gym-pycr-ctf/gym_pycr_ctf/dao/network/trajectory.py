from typing import List
import json
import os
import gym_pycr_ctf.constants.constants as constants


class Trajectory:
    """
    Class that represents a trajectory in the environment
    """

    def __init__(self):
        self.attacker_rewards = []
        self.defender_rewards = []
        self.attacker_observations = []
        self.defender_observations = []
        self.infos = []
        self.dones = []
        self.attacker_actions = []
        self.defender_actions = []

    def __str__(self) -> str:
        return "attacker_rewards:{}, defender_rewards:{}, attacker_observations:{}, defender_observations:{}, " \
               "infos:{}, dones:{}, attacker_actions:{}, defender_actions:{}".format(
            self.attacker_rewards, self.defender_rewards, self.attacker_observations,
            self.defender_observations, self.infos, self.dones, self.attacker_actions,
            self.defender_actions)


    def to_dict(self) -> dict:
        return {
            "attacker_rewards": self.attacker_rewards,
            "defender_rewards": self.defender_rewards,
            "attacker_observations": self.attacker_observations,
            "defender_observations": self.defender_observations,
            "infos": self.infos,
            "dones": self.dones,
            "attacker_actions": self.attacker_actions,
            "defender_actions": self.defender_actions
        }

    @staticmethod
    def from_dict(d: dict) -> "Trajectory":
        trajectory = Trajectory()
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
        return trajectory


    @staticmethod
    def save_trajectories(trajectories_save_dir, trajectories : List["Trajectory"]) -> None:
        trajectories = list(map(lambda x: x.to_dict(), trajectories))
        with open(trajectories_save_dir + "/" + constants.SYSTEM_IDENTIFICATION.TRAJECTORIES_FILE, 'w') as fp:
            json.dump({"trajectories": trajectories}, fp)

    @staticmethod
    def load_trajectories(trajectories_save_dir):
        path = trajectories_save_dir + "/" + constants.SYSTEM_IDENTIFICATION.TRAJECTORIES_FILE
        if os.path.exists(path):
            with open(path, 'r') as fp:
                d = json.load(fp)
                trajectories  = d["trajectories"]
                trajectories = list(map(lambda x: Trajectory.from_dict(x), trajectories))
                return trajectories
        else:
            print("Warning: Could not read trajectories file, path does not exist:{}".format(path))
            return []