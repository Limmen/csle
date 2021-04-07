from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env import PyCRCTFLevel1Emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.agents.manual.manual_defender_agent import ManualDefenderAgent
from gym_pycr_ctf.agents.bots.random_attacker_bot_agent import RandomAttackerBotAgent
from gym_pycr_ctf.agents.bots.custom_attacker_bot_agent import CustomAttackerBotAgent
from gym_pycr_ctf.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
import gym


def initialize_models(self) -> None:
    """
    Initialize models

    :return: None
    """
    # Initialize models
    model = PPO.load(env=self.env, load_path=self.agent_config.load_path, device=self.device,
                          agent_config=self.agent_config)
    return model

def manual_control():
    # emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    # emulation_config = EmulationConfig(agent_ip="172.18.4.191", agent_username="agent", agent_pw="agent",
    #                                  server_connection=False, port_forward_next_port=9600)
    emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.4.191",
                                            agent_username="agent", agent_pw="agent", server_connection=True,
                                            server_private_key_file="/home/kim/.ssh/id_rsa",
                                            server_username="kim", port_forward_next_port=3000)
    emulation_config.skip_exploration = True
    model_path_dir = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/" \
                     "examples/difficulty_level_4/hello_world/"
    # model_path_dir = "/home/kim/pycr/python-envs/minigames/network_intrusion/ctf/" \
    #                  "gym-pycr-ctf/examples/difficulty_level_4/hello_world"
    emulation_config.save_dynamics_model_dir = model_path_dir

    env = gym.make("pycr-ctf-level-4-emulation-v5", env_config=None, emulation_config=emulation_config)
    env.env_config.attacker_use_nmap_cache = False
    env.env_config.attacker_nmap_scan_cache = False
    env.env_config.attacker_use_nikto_cache = False
    env.env_config.attacker_use_file_system_cache = False
    env.env_config.attacker_use_user_command_cache = False
    #env = gym.make("pycr-ctf-level-4-generated-sim-v5", env_config=None, emulation_config=emulation_config)

    #attacker_opponent = RandomAttackerBotAgent(env_config = env.env_config, env=env)
    attacker_opponent = CustomAttackerBotAgent(env_config=env.env_config, env=env)
    ManualDefenderAgent(env=env, env_config=env.env_config, attacker_opponent=attacker_opponent)




if __name__ == '__main__':
    manual_control()