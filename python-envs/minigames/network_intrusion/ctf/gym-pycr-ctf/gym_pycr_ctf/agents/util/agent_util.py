import torch
from gym_pycr_ctf.agents.config.agent_config import AgentConfig


class AgentUtil:
    """
    Class with utility functions for training agents
    """

    @staticmethod
    def get_hidden_activation(config: AgentConfig):
        """
        Interprets the hidden activation

        :return: the hidden activation function
        """
        if config.hidden_activation == "ReLU":
            return torch.nn.ReLU
        elif config.hidden_activation == "LeakyReLU":
            return torch.nn.LeakyReLU
        elif config.hidden_activation == "LogSigmoid":
            return torch.nn.LogSigmoid
        elif config.hidden_activation == "PReLU":
            return torch.nn.PReLU
        elif config.hidden_activation == "Sigmoid":
            return torch.nn.Sigmoid
        elif config.hidden_activation == "Softplus":
            return torch.nn.Softplus
        elif config.hidden_activation == "Tanh":
            return torch.nn.Tanh
        else:
            raise ValueError("Activation type: {} not recognized".format(self.attacker_config.hidden_activation))

