from typing import Union, Tuple
import torch
import torch.nn as nn
import gymnasium as gym
from torch.distributions.categorical import Categorical
import numpy as np


class PPONetwork(nn.Module):
    """
    Class for instantiating a neural network for PPO training

    :param envs: envs parameter
    :param num_hl: number of hidden layers in the neural network
    :param num_hl_neur: number of neurons in a hidden layer in the network
    :param output_size_critic: the output size of the critic function/policy in the model
    :param outout_size_actor: the output size of the actor function/policy in the model
    """

    def __init__(self, envs: gym.vector.SyncVectorEnv, num_hl: int, num_hl_neur: int, output_size_critic: int = 1,
                 std_critic: float = 1.0, std_action: float = 0.01) -> None:
        super(PPONetwork, self).__init__()

        input_size = np.array(envs.single_observation_space.shape).prod()
        self.output_size_critic = output_size_critic
        self.output_size_action = envs.single_action_space.n

        self.critic = nn.Sequential()
        self.actor = nn.Sequential()
        for layer in range(num_hl):
            self.critic.add_module(name=f'Layer {layer}', module=self.layer_init(nn.Linear(input_size, num_hl_neur)))
            self.critic.add_module(name='activation', module=nn.Tanh())
            self.actor.add_module(name=f'Layer {layer}', module=self.layer_init(nn.Linear(input_size, num_hl_neur)))
            self.actor.add_module(name='activation', module=nn.Tanh())
            input_size = num_hl_neur
        self.critic.add_module(name='Classifier',
                               module=self.layer_init(nn.Linear(num_hl_neur, self.output_size_critic), std=std_critic))
        self.actor.add_module(name='Classifier',
                              module=self.layer_init(nn.Linear(num_hl_neur, self.output_size_action),
                                                     std=std_action))

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
        return self.critic(x)

    def get_action_and_value(self, x: torch.Tensor, action: Union[torch.Tensor, None] = None) \
            -> Tuple[torch.Tensor, float, float, torch.Tensor]:
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
