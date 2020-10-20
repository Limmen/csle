"""
A bot attack agent for the pycr-wcrack environment that acts greedily according to a pre-trained policy network
"""
import torch
import traceback
import time
from gym_pycr_pwcrack.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackEnv
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.agents.config.agent_config import AgentConfig

class PPOAttackerBotAgent:
    """
    Class implementing an attack policy that acts greedily according to a given policy network
    """

    def __init__(self, pg_config: AgentConfig, env_config: EnvConfig, model_path: str = None,
                 env: PyCRPwCrackEnv = None):
        """
        Constructor, initializes the policy

        :param game_config: the game configuration
        """
        self.env_config = env_config
        if model_path is None:
            raise ValueError("Cannot create a PPOAttackerBotAgent without specifying the path to the model")
        self.env = env
        self.agent_config = pg_config
        self.model_path = model_path
        self.device = "cpu" if not self.agent_config.gpu else "cuda:" + str(self.agent_config.gpu_id)
        self.initialize_models()


    def initialize_models(self) -> None:
        """
        Initialize models
        :return: None
        """
        policy = "MlpPolicy"
        # Initialize models
        self.model = PPO.load(env=self.env, load_path=self.agent_config.load_path, device=self.device,
                              agent_config=self.agent_config)

    def action(self, s: EnvState) -> int:
        """
        Samples an action from the policy.

        :param game_state: the game state
        :return: action_id
        """
        try:
            #actions = list(range(self.agent_config.output_dim))
            # non_legal_actions = list(filter(lambda action: not PyCRPwCrackEnv.is_action_legal(
            #     action, env_config=self.env_config, env_state=s), actions))
            m_obs, p_obs = s.get_observation()
            obs_tensor = torch.as_tensor(m_obs.flatten()).to(self.device)            
            actions, values = self.model.predict(observation=obs_tensor, deterministic = True,
                                                            state=obs_tensor)
            time.sleep(2)

            action = actions[0]
        except Exception as e:
            print(str(e))
            traceback.print_exc()

        return action
