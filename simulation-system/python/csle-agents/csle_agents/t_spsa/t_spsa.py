from typing import Union, List, Dict
import math
import random
import gym
import sys
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_agents.base.base_agent import BaseAgent
from csle_common.util.experiment_util import ExperimentUtil


class TSPSA(BaseAgent):
    """
    RL Agent implementing the T-SPSA algorithm from (Hammar, Stadler 2021 -
                                                     Intrusion Prevention through Optimal Stopping))
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig], experiment_config: ExperimentConfig):
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.T_SPSA

    def train(self) -> ExperimentExecution:
        config = self.simulation_env_config.simulation_env_input_config
        env = gym.make(self.simulation_env_config.gym_env_name, config=config)
        for seed in self.experiment_config.random_seeds:
            ExperimentUtil.set_seed(seed)
            exp_result = ExperimentResult()
            self.spsa(exp_result=exp_result, seed=seed, env=env)

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return ["a", "c", "lambda", "A", "epsilon", "N", "L", "theta1", "eval_batch_size"]

    def spsa(self, exp_result: ExperimentResult, seed: int, env: gym.Env):
        exp_result.metrics[seed] = {}
        exp_result.metrics[seed]["thetas"] = []
        exp_result.metrics[seed]["values"] = []
        theta = self.experiment_config.hparams["theta1"].value
        eval_batch_size = self.experiment_config.hparams["eval_batch_size"].value
        avg_metrics = self.eval_theta(theta=theta, eval_batch_size=eval_batch_size, env=env)
        print(avg_metrics)
        sys.exit(0)

    def eval_theta(self, theta: List[float], eval_batch_size: int, env: gym.Env):
        metrics = {}
        for j in range(eval_batch_size):
            done = False
            o = env.reset()
            l = o[0]
            b1 = o[1]
            while not done:
                threshold = TSPSA.sigmoid(theta[l-1])
                if b1 >= threshold:
                    a = TSPSA.smooth_threshold_action_selection(threshold=threshold, b1=b1)
                else:
                    a = 0
                o, r, done, info = env.step(a)
                TSPSA.update_metrics(metrics=metrics, info=info)
            avg_metrics = TSPSA.compute_avg_metrics(metrics=metrics)
            return avg_metrics

    @staticmethod
    def update_metrics(metrics: Dict[str, List[Union[float, int]]], info: Dict[str, Union[float, int]]) -> None:
        """
        Update a dict with aggregated metrics using new information from the environment

        :param metrics: the dict with the aggregated metrics
        :param info: the new information
        :return: None
        """
        for k,v in info.items():
            if k in metrics:
                metrics[k].append(v)
            else:
                metrics[k] = [v]

    @staticmethod
    def compute_avg_metrics(metrics: Dict[str, List[Union[float, int]]]) -> Dict[str, Union[float, int]]:
        """
        Computes the average metrics of a dict with aggregated metrics

        :param metrics: the dict with the aggregated metrics
        :return: the average metrics
        """
        avg_metrics = {}
        for k,v in metrics.items():
            avg = round(sum(v)/len(v),2)
            avg_metrics[k] = avg
        return avg_metrics

    @staticmethod
    def standard_ak(a: int, A: int, epsilon: float, k: int) -> float:
        """
        Gets the step size for gradient ascent at iteration k

        :param a: a scalar hyperparameter
        :param A: a scalar hyperparameter
        :param epsilon: the epsilon scalar hyperparameter
        :param k: the iteration index
        :return: the step size a_k
        """
        return a / (k + 1 + A) ** epsilon

    @staticmethod
    def standard_ck(c: float, lamb: float, k: int) -> float:
        """
        Gets the step size of perturbations at iteration k

        :param c: a scalar hyperparameter
        :param lamb: (lambda) a scalar hyperparameter
        :param k: the iteration
        :return: the pertrubation step size
        """
        '''Create a generator for values of c_k in the standard form.'''
        return c / (k + 1) ** lamb

    @staticmethod
    def standard_deltak(dimension: int, k: int) -> List[float]:
        """
        Gets the perturbation direction at iteration k

        :param k: the iteration
        :param dimension: the dimension of the perturbation vector
        :return: delta_k the perturbation vector at iteration k
        """
        return [random.choice((-1, 1)) for _ in range(dimension)]

    @staticmethod
    def smooth_threshold_action_selection(threshold: float, b1: float) -> int:
        """
        Selects the next action according to a smooth threshold function on the belief

        :param threshold: the threshold
        :param b1: the belief
        :return: the selected action
        """
        v=20
        prob = math.pow(1 + math.pow(((b1*(1-threshold))/(threshold*(1-b1))), -v), -1)
        if random.uniform(0,1) >= prob:
            return 0
        else:
            return 1

    @staticmethod
    def sigmoid(x) -> float:
        """
        The sigmoid function

        :param x:
        :return: sigmoid(x)
        """
        return 1/(1 + math.exp(-x))