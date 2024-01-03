import torch
import torch.nn as nn
from torch.distributions.categorical import Categorical
import numpy as np


class QNetwork(nn.Module):
    """
    Class for instantiating the neural network trained upon
    :param envs: envs parameter
    :param num_hl: number of hidden layers in the neural network
    :param num_hl_neur: number of neurons in a hidden layer in the network
    :param output_size_critic: the output size of the critic function/policy in the model
    :param outout_size_actor: the output size of the actor function/policy in the model
    """
    def __init__(self, envs, num_hl, num_hl_neur, output_size_critic=1, std_critic=1.0, std_action=0.01):

        super(QNetwork, self).__init__()

        input_size = np.array(envs.single_observation_space.shape).prod()
        self.output_size_critic = output_size_critic
        self.output_size_action = envs.single_action_space.n

        self.network = nn.Sequential()
        for layer in range(num_hl):
            self.network.add_module(name=f'Layer {layer}', module=self.layer_init(nn.Linear(input_size, num_hl_neur)))
            self.network.add_module(name='activation', module=nn.ReLU())
            input_size = num_hl_neur
        self.critic.add_module(name='Classifier',
                               module=self.layer_init(nn.Linear(num_hl_neur, self.output_size_critic), std=std_critic))
        self.actor.add_module(name='Classifier',
                              module=self.layer_init(nn.Linear(num_hl_neur, self.output_size_action),
                                                     std=std_action))

    def foward(self, x):
        return self.network(x)