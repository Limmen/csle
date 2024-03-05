from typing import Union, Tuple
import torch
import torch.nn as nn
from torch.distributions.categorical import Categorical
import numpy as np


class PPONetwork(nn.Module):
    """
    Class for instantiating a neural network for PPO training
    """

    def __init__(self, input_dim: int, output_dim_critic: int, output_dim_action: int,
                 num_hidden_layers: int, hidden_layer_dim: int, std_critic: float = 1.0,
                 std_action: float = 0.01) -> None:
        """
        Initializes the neural network

        :param input_dim: the dimension of the input
        :param output_dim_critic: the dimension of the critic output (generally 1)
        :param output_dim_action: the dimension of the actor output (action space dimension)
        :param num_hidden_layers: the number of hidden layers
        :param hidden_layer_dim: the dimension of a hidden layer
        :param std_critic: the standard deviation of the critic for sampling
        :param std_action: the standard deviation of the actor for sampling
        """
        super(PPONetwork, self).__init__()
        self.input_dim = input_dim
        self.output_dim_critic = output_dim_critic
        self.output_dim_action = output_dim_action
        self.std_critic = std_critic
        self.std_action = std_action
        self.critic = nn.Sequential()
        self.actor = nn.Sequential()
        self.aux_critic = nn.Sequential()
        self.num_hidden_layers = num_hidden_layers
        self.hidden_layer_dim = hidden_layer_dim
        input_dim = self.input_dim
        for layer in range(num_hidden_layers):
            self.critic.add_module(name=f'Layer {layer}', module=self.layer_init(nn.Linear(input_dim,
                                                                                           hidden_layer_dim)))
            self.critic.add_module(name='activation', module=nn.Tanh())
            self.aux_critic.add_module(name=f'Layer {layer}', module=self.layer_init(nn.Linear(input_dim,
                                                                                               hidden_layer_dim)))
            self.aux_critic.add_module(name='activation', module=nn.Tanh())
            self.actor.add_module(name=f'Layer {layer}', module=self.layer_init(nn.Linear(input_dim,
                                                                                          hidden_layer_dim)))
            self.actor.add_module(name='activation', module=nn.Tanh())
            input_dim = hidden_layer_dim
        self.critic.add_module(name='Classifier',
                               module=self.layer_init(nn.Linear(hidden_layer_dim, self.output_dim_critic),
                                                      std=self.std_critic))
        self.aux_critic.add_module(name='Classifier',
                                   module=self.layer_init(nn.Linear(hidden_layer_dim, self.output_dim_critic),
                                                          std=self.std_critic))
        self.actor.add_module(name='Classifier',
                              module=self.layer_init(nn.Linear(hidden_layer_dim, self.output_dim_action),
                                                     std=self.std_action))

    def layer_init(self, layer: nn.Linear, std: float = np.sqrt(2), bias_const: float = 0.0) -> nn.Linear:
        """
        Initializes a layer in the neural network

        :param layer: the layer object
        :param std: the standard deviation
        :param bias_const: the bias constant
        :return: the initialized layer
        """
        torch.nn.init.orthogonal_(layer.weight, std)
        torch.nn.init.constant_(layer.bias, bias_const)
        return layer

    def get_value(self, x: torch.Tensor) -> torch.Tensor:
        """
        Computes the value function V(x)

        :param x: the input observation
        :return: The value
        """
        value: torch.Tensor = self.critic(x)
        return value

    def get_action_and_value(self, x: torch.Tensor, action: Union[torch.Tensor, None] = None) \
            -> Tuple[torch.Tensor, float, torch.Tensor, torch.Tensor]:
        """
        Gets the action and the value prediction of the network for a given input tensor x

        :param x: the input tensor
        :param action: (optional) the action; if not specified the action is sampled
        :return: the action, log p(action), the entropy of the action, V(x)
        """
        logits = self.actor(x)
        probs = Categorical(logits=logits)
        if action is None:
            action = probs.sample()
        return action, probs.log_prob(action), probs.entropy(), self.critic(x)

    def get_pi(self, x: torch.Tensor) -> torch.distributions.Categorical:
        """
        Utility function for PPG

        :param x: the input vector
        :return: the output action distribution
        """
        return Categorical(logits=self.actor(x))

    def get_pi_value_and_aux_value(self, x: torch.Tensor) \
            -> Tuple[torch.distributions.Categorical, torch.Tensor, torch.Tensor]:
        """
        Utility function for PPG

        :param x: the input vector
        :return: output distribution, critic value, and auxiliary critic value
        """
        return Categorical(logits=self.actor(x)), self.critic(x.detach()), self.aux_critic(x)

    def save(self, path: str) -> None:
        """
        Saves the model to disk

        :param path: the path on disk to save the model
        :return: None
        """
        state_dict = self.state_dict()
        state_dict["input_dim"] = self.input_dim
        state_dict["output_dim_critic"] = self.output_dim_critic
        state_dict["output_dim_action"] = self.output_dim_action
        state_dict["std_critic"] = self.std_critic
        state_dict["std_action"] = self.std_action
        state_dict["num_hidden_layers"] = self.num_hidden_layers
        state_dict["hidden_layer_dim"] = self.hidden_layer_dim
        torch.save(state_dict, path)

    @staticmethod
    def load(path: str) -> "PPONetwork":
        """
        Loads the model from a given path

        :param path: the path to load the model from
        :return: None
        """
        state_dict = torch.load(path)
        model = PPONetwork(input_dim=state_dict["input_dim"], output_dim_action=state_dict["output_dim_action"],
                           output_dim_critic=state_dict["output_dim_critic"],
                           num_hidden_layers=state_dict["num_hidden_layers"],
                           hidden_layer_dim=state_dict["hidden_layer_dim"], std_critic=state_dict["std_critic"],
                           std_action=state_dict["std_action"])
        del state_dict["input_dim"]
        del state_dict["output_dim_critic"]
        del state_dict["output_dim_action"]
        del state_dict["std_critic"]
        del state_dict["std_action"]
        del state_dict["num_hidden_layers"]
        del state_dict["hidden_layer_dim"]
        model.load_state_dict(state_dict)
        model.eval()
        return model
