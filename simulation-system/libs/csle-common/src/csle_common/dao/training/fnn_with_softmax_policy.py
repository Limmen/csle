from typing import List, Dict, Union, Tuple, Any
import numpy as np
from numpy.typing import NDArray
import torch
import math
from torch.distributions import Categorical
from csle_common.models.fnn_w_softmax import FNNwithSoftmax
import csle_common.constants.constants as constants
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.policy_type import PolicyType
from csle_common.logging.log import Logger


class FNNWithSoftmaxPolicy(Policy):
    """
    A feed-forward neural network policy with softmax output
    """

    def __init__(self, policy_network, simulation_name: str, save_path: str,
                 player_type: PlayerType, states: List[State],
                 actions: List[Action], experiment_config: ExperimentConfig, avg_R: float, input_dim: int,
                 output_dim: int):
        """
        Initializes the policy

        :param policy_network: the PPO model
        :param simulation_name: the simulation name
        :param save_path: the path to save the model to
        :param states: list of states (required for computing stage policies)
        :param actions: list of actions
        :param experiment_config: the experiment configuration for training the policy
        :param avg_R: the average reward of the policy when evaluated in the simulation
        """
        super(FNNWithSoftmaxPolicy, self).__init__(agent_type=AgentType.PPO, player_type=player_type)
        self.policy_network = policy_network
        self.id = -1
        self.simulation_name = simulation_name
        self.save_path = save_path
        self.states = states
        self.actions = actions
        self.experiment_config = experiment_config
        self.avg_R = avg_R
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.policy_type = PolicyType.FNN_W_SOFTMAX
        if self.policy_network is None and self.save_path != "":
            try:
                hidden_dim = \
                    self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER].value
                hidden_layers = self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS].value
                activation = self.experiment_config.hparams[constants.NEURAL_NETWORKS.ACTIVATION_FUNCTION].value
                if not isinstance(hidden_dim, int):
                    raise ValueError(f"The number of neurons must be an integer, got type: {type(hidden_dim)}")
                if not isinstance(hidden_layers, int):
                    raise ValueError(f"The number of layers must be an integer, got type: {type(hidden_layers)}")
                if not isinstance(activation, str):
                    raise ValueError(f"The type of the actvation function must be a string, "
                                     f"got type: {type(activation)}")
                self.policy_network = FNNwithSoftmax(
                    input_dim=input_dim,
                    output_dim=output_dim,
                    hidden_dim=hidden_dim,
                    num_hidden_layers=hidden_layers,
                    hidden_activation=activation)
                self.policy_network = self.policy_network.load_state_dict(torch.load(self.save_path))
            except Exception as e:
                Logger.__call__().get_logger().warning(
                    f"There was an exception loading the model from path: {self.save_path}, "
                    f"exception: {str(e)}, {repr(e)}")

    def action(self, o: NDArray[Any], deterministic: bool = True) -> Any:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :param deterministic: boolean flag indicating whether the action selection should be deterministic
        :return: the selected action
        """
        state = torch.from_numpy(o).float()
        device = self.experiment_config.hparams[constants.NEURAL_NETWORKS.DEVICE].value
        if not isinstance(device, str):
            raise ValueError(f"Device must be a str, got type: {type(device)}")
        state1 = state.to(str(torch.device(device)))

        # Forward pass using the current policy network to predict P(a|s)
        action_probs = self.policy_network(state1).squeeze()
        # Set probability of non-legal actions to 0
        action_probs_1 = action_probs.clone()

        # Use torch.distributions package to create a parameterizable probability distribution of the learned policy
        # PG uses a trick to turn the gradient into a stochastic gradient which we can sample from in order to
        # approximate the true gradient (which we can’t compute directly). It can be seen as an alternative to the
        # reparameterization trick
        policy_dist = Categorical(action_probs_1)

        # Sample an action from the probability distribution
        action = policy_dist.sample()
        return action

    def get_action_and_log_prob(self, state: NDArray[Any]) -> Tuple[int, float]:
        """
        Samples an action from the policy network

        :param policy_network: the policy network
        :param state: the state to sample an action for
        :return: The sampled action id and the log probability
        """
        state1 = torch.from_numpy(state.flatten()).float()
        device = self.experiment_config.hparams[constants.NEURAL_NETWORKS.DEVICE].value
        if not isinstance(device, str):
            raise ValueError(f"Device must be a str, got type: {type(device)}")
        state2 = state1.to(torch.device(device))

        # Forward pass using the current policy network to predict P(a|s)
        action_probs = self.policy_network(state2).squeeze()
        # Set probability of non-legal actions to 0
        action_probs_1 = action_probs.clone()

        # Use torch.distributions package to create a parameterizable probability distribution of the learned policy
        # PG uses a trick to turn the gradient into a stochastic gradient which we can sample from in order to
        # approximate the true gradient (which we can’t compute directly). It can be seen as an alternative to the
        # reparameterization trick
        policy_dist = Categorical(action_probs_1)

        # Sample an action from the probability distribution
        action = policy_dist.sample()

        # log_prob returns the log of the probability density/mass function evaluated at value.
        # save the log_prob as it will use later on for computing the policy gradient
        # policy gradient theorem says that the stochastic gradient of the expected return of the current policy is
        # the log gradient of the policy times the expected return, therefore we save the log of the policy distribution
        # now and use it later to compute the gradient once the episode has finished.
        log_prob = policy_dist.log_prob(action)
        return action.item(), log_prob

    def probability(self, o: NDArray[Any], a: int) -> Union[int, float]:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :return: the selected action
        """
        action, log_prob = self.get_action_and_log_prob(state=o)
        if action == a:
            return math.exp(log_prob)
        else:
            return 0

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the policy
        """
        d: Dict[str, Any] = {}
        d["id"] = self.id
        d["simulation_name"] = self.simulation_name
        d["save_path"] = self.save_path
        d["states"] = list(map(lambda x: x.to_dict(), self.states))
        d["player_type"] = self.player_type
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["experiment_config"] = self.experiment_config.to_dict()
        d["agent_type"] = self.agent_type
        d["avg_R"] = self.avg_R
        d["input_dim"] = self.input_dim
        d["output_dim"] = self.output_dim
        d["policy_type"] = self.policy_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FNNWithSoftmaxPolicy":
        """
        Converst a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FNNWithSoftmaxPolicy(policy_network=None, simulation_name=d["simulation_name"],
                                   save_path=d["save_path"],
                                   states=list(map(lambda x: State.from_dict(x), d["states"])),
                                   player_type=d["player_type"],
                                   actions=list(map(lambda x: Action.from_dict(x), d["actions"])),
                                   experiment_config=ExperimentConfig.from_dict(d["experiment_config"]),
                                   avg_R=d["avg_R"], input_dim=d["input_dim"], output_dim=d["output_dim"])
        # policy_type=d["policy_type"])
        obj.id = d["id"]
        return obj

    def stage_policy(self, o: Union[List[int], List[float]]) -> List[List[float]]:
        """
        Gets the stage policy, i.e a |S|x|A| policy

        :param o: the latest observation
        :return: the |S|x|A| stage policy
        """
        b1 = o[1]
        l = int(o[0])
        if not self.player_type == PlayerType.ATTACKER:
            stage_policy = []
            for _ in self.states:
                stage_policy.append(self._get_attacker_dist(obs=o))
            return stage_policy
        else:
            stage_policy = []
            for s in self.states:
                if s.state_type != StateType.TERMINAL:
                    o = [l, b1, s.id]
                    stage_policy.append(self._get_attacker_dist(obs=o))
                else:
                    stage_policy.append([0.5, 0.5])
            return stage_policy

    def _get_attacker_dist(self, obs) -> List[float]:
        """
        Utility function for getting the action distribution conditioned on a given observation

        :param obs: the observation to condition on
        :return: the conditional ation distribution
        """
        obs = np.array([obs])
        actions, values, log_prob = self.policy_network.policy.forward(
            obs=torch.tensor(obs).to(self.policy_network.device))
        action = actions[0]
        if action == 1:
            stop_prob = math.exp(log_prob)
        else:
            stop_prob = 1 - math.exp(log_prob)
        return [1 - stop_prob, stop_prob]

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"policy network: {self.policy_network}, id: {self.id}, simulation_name: {self.simulation_name}, " \
               f"save path: {self.save_path}, states: {self.states}, experiment_config: {self.experiment_config}," \
               f"avg_R: {self.avg_R}, input_dim: {self.input_dim}, output_dim: {self.output_dim}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "FNNWithSoftmaxPolicy":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FNNWithSoftmaxPolicy.from_dict(json.loads(json_str))

    def save_policy_network(self) -> None:
        """
        Saves the PyTorch Model Weights

        :return: None
        """
        path = self.save_path
        torch.save(self.policy_network.state_dict(), path)

    def copy(self) -> "FNNWithSoftmaxPolicy":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())
