import torch
from csle_common.models.fnn_w_softmax import FNNwithSoftmax
from csle_common.models.ppo_network import PPONetwork
from csle_common.models.q_network import QNetwork
from csle_common.dao.training.agent_type import AgentType


class TestModelsSuite:
    """
    Test suite for the models package
    """

    def test_fnn_w_softmax(self) -> None:
        """
        Tests creation of the FNN-with-softmax model

        :return: None
        """
        output_dim = 1
        input_dim = 10
        hidden_dim = 64
        num_hidden_layers = 4
        hidden_activation = "ReLU"
        model = FNNwithSoftmax(input_dim=input_dim, output_dim=output_dim, hidden_dim=hidden_dim,
                               num_hidden_layers=num_hidden_layers, hidden_activation=hidden_activation)
        assert model is not None
        assert model.output_dim == output_dim
        assert model.input_dim == input_dim
        assert model.num_hidden_layers == num_hidden_layers
        assert model.hidden_activation == hidden_activation
        assert len(model.layers) == (num_hidden_layers + 2) * 2

        y = model.forward(torch.tensor([[1.0] * input_dim]))
        assert y is not None
        assert len(y.detach().numpy()[0]) == output_dim

    def test_ppo_networK(self) -> None:
        """
        Tests creation of the PPO network model

        :return: None
        """
        output_dim_critic = 1
        output_dim_action = 1
        input_dim = 10
        hidden_dim = 64
        num_hidden_layers = 4
        std_critic = 1.0
        std_action = 0.01
        model = PPONetwork(input_dim=input_dim, output_dim_critic=output_dim_critic,
                           num_hidden_layers=num_hidden_layers, hidden_layer_dim=hidden_dim, std_critic=std_critic,
                           std_action=std_action, output_dim_action=output_dim_action)
        assert model is not None
        assert model.input_dim == input_dim
        assert model.output_dim_critic == output_dim_critic
        assert model.output_dim_action == output_dim_action
        assert model.std_critic == std_critic
        assert model.std_action == std_action
        assert model.num_hidden_layers == num_hidden_layers
        assert model.hidden_layer_dim == hidden_dim
        assert len(list(model.critic.modules())) == (num_hidden_layers + 3)
        assert len(list(model.aux_critic.modules())) == (num_hidden_layers + 3)
        assert len(list(model.actor.modules())) == (num_hidden_layers + 3)
        y = model.get_value(x=torch.tensor([[1.0] * input_dim]))
        assert y is not None
        assert len(y.detach().numpy()[0]) == output_dim_critic
        y2 = model.get_pi(x=torch.tensor([[1.0] * input_dim]))
        assert y2 is not None
        assert len(y2.probs.detach().numpy()[0]) == output_dim_critic

    def test_q_network(self) -> None:
        """
        Tests creation of the Q-network model

        :return: None
        """
        output_dim = 1
        input_dim = 10
        hidden_dim = 64
        num_hidden_layers = 4
        agent_type = AgentType.DQN
        n_atoms = 101
        start = -100
        end = 100
        steps = 101
        model = QNetwork(input_dim=input_dim, num_hidden_layers=num_hidden_layers, hidden_layer_dim=hidden_dim,
                         agent_type=agent_type, action_space_dim=output_dim, n_atoms=n_atoms, start=start, end=end,
                         steps=steps)
        assert model is not None
        assert model.num_hidden_layers == num_hidden_layers
        assert model.input_dim == input_dim
        assert model.agent_type == agent_type
        assert model.hidden_layer_dim == hidden_dim
        assert len(list(model.network.modules())) == (num_hidden_layers + 2)
        val = model.forward(x=torch.tensor([[1.0] * input_dim]))
        assert val is not None
        assert len(val.detach().numpy()[0]) == hidden_dim
