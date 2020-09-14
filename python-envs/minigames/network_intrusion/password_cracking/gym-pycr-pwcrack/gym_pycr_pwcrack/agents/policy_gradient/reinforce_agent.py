from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackEnv
from gym_pycr_pwcrack.agents.config.pg_agent_config import PolicyGradientAgentConfig
from gym_pycr_pwcrack.agents.policy_gradient.pg_agent import PolicyGradientAgent
from gym_pycr_pwcrack.dao.experiment_result import ExperimentResult

class ReinforceAgent(PolicyGradientAgent):

    def __init__(self, env:PyCRPwCrackEnv, config: PolicyGradientAgentConfig):
        super(ReinforceAgent, self).__init__(env, config)

    def train(self) -> ExperimentResult:
        pass

    def eval(self) -> ExperimentResult:
        pass