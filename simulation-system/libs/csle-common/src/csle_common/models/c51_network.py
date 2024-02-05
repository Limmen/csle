import torch
import torch.nn as nn
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
    def __init__(self, envs, num_hl, num_hl_neur, n_atoms=101, output_size_critic=1):
        super(QNetwork, self).__init__()
        input_size = np.array(envs.single_observation_space.shape).prod()
        self.output_size_critic = output_size_critic
        self.output_size_action = envs.single_action_space.n
        self.num_hl = num_hl
        self.num_hl_neur = num_hl_neur
        self.n_atoms = n_atoms
        self.network = nn.Sequential()
        for layer in range(num_hl):
            self.network.add_module(name=f'Layer {layer}', module=nn.Linear(input_size, num_hl_neur*n_atoms))
            self.network.add_module(name='activation', module=nn.ReLU())
            input_size = num_hl_neur*n_atoms

    def get_action(self, x, action=None):
        logits = self.network(x)
        # probability mass function for each action
        pmfs = torch.softmax(logits.view(len(x), self.num_hl_neur, self.n_atoms), dim=2)
        # TODO: look into this
        self.atoms = torch.linspace(-100, 100, 101)

        q_values = (pmfs * self.atoms).sum(2)
        if action is None:
            action = torch.argmax(q_values, 1)
        return action, pmfs[torch.arange(len(x)), action]

    def save(self, path: str) -> None:
        """
        Saves the model to disk

        :param path: the path on disk to save the model
        :return: None
        """
        state_dict = self.state_dict()
        state_dict["output_size_critic"] = self.output_size_critic
        # state_dict["input_size"] = self.input_size
        state_dict["output_size_action"] = self.output_size_action
        state_dict["num_hidden_layers"] = self.num_hl
        state_dict["hidden_layer_dim"] = self.num_hl_neur
        torch.save(state_dict, path)

