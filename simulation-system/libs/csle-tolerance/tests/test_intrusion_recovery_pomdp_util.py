from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil
from csle_tolerance.dao.intrusion_recovery_pomdp_config import IntrusionRecoveryPomdpConfig
import numpy as np

class TestIntrusionTolerancePomdpSuite:
    """
    Test suite for intrusion_recovery_pomdp_util.py
    """

    def test__state_space(self) -> None:
        """
        Tests the state space of the POMDP

        :return: None
        """
        assert (isinstance(item,int) for item in IntrusionRecoveryPomdpUtil.state_space())
        assert IntrusionRecoveryPomdpUtil.state_space() is not None
        assert IntrusionRecoveryPomdpUtil.state_space() == [0,1,2]

    def test_initial_belief(self) -> None:
        """
        Tests the initial_belief function

        :return: None
        """
        assert sum(IntrusionRecoveryPomdpUtil.initial_belief(p_a=0.5)) == 1

    def test_action_space(self) -> None:
        """
        Tests the action space of the POMDP

        :return: None
        """
        assert (isinstance(item,int) for item in IntrusionRecoveryPomdpUtil.action_space())
        assert IntrusionRecoveryPomdpUtil.action_space() is not None
        assert IntrusionRecoveryPomdpUtil.action_space() == [0,1]

    def test_observation_space(self) -> None:
        """
        Tests the observation space of the POMDP

        :return: None
        """
        num_observation = 3
        expected = [0,1,2]
        assert IntrusionRecoveryPomdpUtil.observation_space(num_observation) == expected

    def test_cost_function(self) -> None:
        """
        Tests the cost function of the POMDP

        :return: None
        """
        s = 1
        a = 0
        eta = 0.5
        negate = False
        assert IntrusionRecoveryPomdpUtil.cost_function(s,a,eta,negate) == 0.5

    def test_cost_tensor(self) -> None:
        """
        Tests the function of creating a tensor with the costs of the POMDP
        
        :return: None
        """
        eta = 0.5
        states = [0,1]
        actions = [0]
        negate = False
        expected = [[0,0.5]]
        assert IntrusionRecoveryPomdpUtil.cost_tensor(eta,states,actions,negate) == expected

    def test_observation_function(self) -> None:
        """
        Tests the observation function of the POMDP

        :return: None
        """
        s = 1
        o = 1
        num_observations = 2
        expected = 0.6
        assert round(IntrusionRecoveryPomdpUtil.observation_function(s,o,num_observations),1)

    def test_observation_tensor(self) -> None:
        """
        Tests the function of creating a tensor with observation probabilities

        :return: None
        """
        states = [0,1]
        observations = [0,1]
        expected = [[0.8,0.2],[0.4,0.6]]
        obs_tensor = IntrusionRecoveryPomdpUtil.observation_tensor(states,observations)
        for i in range(len(obs_tensor)):
            for j in range(len(obs_tensor[i])):
                obs_tensor[i][j] = round(obs_tensor[i][j],1)
            assert sum(obs_tensor[i]) == 1
        assert obs_tensor == expected

    def test_transition_function(self) -> None:
        """
        Tests the transition function of the POMDP

        :return: None
        """
        s = 0
        s_prime = 1
        a = 0
        p_a = 0.2
        p_c_1 = 0.1
        p_c_2 = 0.2
        p_u = 0.5
        assert round(IntrusionRecoveryPomdpUtil.transition_function(s,s_prime,a,p_a,p_c_1,p_c_2,p_u),1) == 0.2

    def test_transition_tensor(self) -> None:
        """
        Tests the function of creating  a tensor with the transition probabilities of the POMDP

        :return: None
        """
        states = [0,1]
        actions = [0]
        p_a = 0.2
        p_c_1 = 0.1
        p_c_2 = 0.2
        p_u = 0.5
        expected = [[[0.7,0.2],[0.4,0.4]]]
        transition_tensor = IntrusionRecoveryPomdpUtil.transition_tensor(states,actions,p_a,p_c_1,p_c_2,p_u)
        for i in range(len(transition_tensor)):
            for j in range(len(transition_tensor[i])):
                for k in range(len(transition_tensor[i][j])):
                    transition_tensor[i][j][k] = round(transition_tensor[i][j][k],1)
        assert transition_tensor == expected

    def test_sample_initial_state(self) -> None:
        """
        Tests the function of sampling the initial state

        :return: None
        """
        b1 = [0.2,0.8]
        assert isinstance(IntrusionRecoveryPomdpUtil.sample_initial_state(b1),int)
        assert IntrusionRecoveryPomdpUtil.sample_initial_state(b1) <= len(b1)
        assert IntrusionRecoveryPomdpUtil.sample_initial_state(b1) >= 0

    def test_sampe_next_observation(self) -> None:
        """
        Tests the function of sampling the next observation

        :return: None
        """
        observation_tensor = [[0.8,0.2],[0.4,0.6]]
        s_prime = 1
        observations = [0,1]
        assert isinstance(IntrusionRecoveryPomdpUtil.sample_next_observation(observation_tensor,s_prime,observations),int)

    def test_bayes_filter(self) -> None:
        """
        Tests the function of a bayesian filter to computer b[s_prime] of the POMDP

        :return: None
        """
        s_prime = 1
        o = 0
        a = 0
        b = [0.2,0.8]
        states = [0,1]
        observations = [0,1]
        observation_tensor = [[0.8,0.2],[0.4,0.6]]
        transition_tensor = [[[0.6,0.4],[0.1,0.9]]]
        b_prime_s_prime = 0.7
        assert round(IntrusionRecoveryPomdpUtil.bayes_filter(s_prime,o,a,b,states,observations,observation_tensor,transition_tensor),1) == b_prime_s_prime

    def test_p_o_given_b_a1_a2(self) -> None:
        """
        Tests the function of computing P[o|a,b] of the POMDP

        :return: None
        """
        o = 0
        b = [0.2,0.8]
        a = 0
        states = [0,1]
        observation_tensor = [[0.8,0.2],[0.4,0.6]]
        transition_tensor = [[[0.6,0.4],[0.1,0.9]]]
        expected = 0.5
        assert round(IntrusionRecoveryPomdpUtil.p_o_given_b_a1_a2(o,b,a,states,transition_tensor,observation_tensor),1) == expected

    def test_next_belief(self) -> None:
        """
        Tests the funtion of computing the next belief using a Bayesian filter

        :return: None
        """
        o = 0
        a = 0
        b = [0.2,0.8]
        states = [0,1]
        observations = [0,1]
        observation_tensor = [[0.8,0.2],[0.4,0.6]]
        transition_tensor = [[[0.3,0.7],[0.6,0.4]]]
        assert round(sum(IntrusionRecoveryPomdpUtil.next_belief(o,a,b,states,observations,observation_tensor,transition_tensor)),1) == 1

    def test_pomdp_solver_file(self) -> None:
        """
        Tests the function of getting the POMDP environment specification

        :return: None
        """
        
        assert IntrusionRecoveryPomdpUtil.pomdp_solver_file(IntrusionRecoveryPomdpConfig(eta=0.1,p_a=0.4,p_c_1=0.3,p_c_2=0.3,p_u=0.5,BTR=1,negate_costs=True,seed=1,discount_factor = 0.5,
                                           states=[0,1],actions=[0],observations=[0,1],cost_tensor=[[0.1,0.5],[0.5,0.6]],observation_tensor = [[0.8,0.2],[0.4,0.6]],
                                           transition_tensor = [[[0.8,0.2],[0.6,0.4]]],b1=[0.3,0.7],T=3,simulation_env_name="env",gym_env_name="gym",max_horizon=np.inf)) is not None
