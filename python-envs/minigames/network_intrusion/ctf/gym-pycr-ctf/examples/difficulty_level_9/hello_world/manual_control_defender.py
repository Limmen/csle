from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env import PyCRCTFLevel1Emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.agents.manual.manual_defender_agent import ManualDefenderAgent
from gym_pycr_ctf.agents.bots.random_attacker_bot_agent import RandomAttackerBotAgent
from gym_pycr_ctf.agents.bots.custom_attacker_bot_agent import CustomAttackerBotAgent
from gym_pycr_ctf.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
from gym_pycr_ctf.envs_model.logic.exploration.custom_exploration_policy import CustomExplorationPolicy
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
    # emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
    #                                  server_connection=False, port_forward_next_port=9600)
    emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
                                            agent_username="agent", agent_pw="agent", server_connection=True,
                                            server_private_key_file="/home/kim/.ssh/id_rsa",
                                            server_username="kim", port_forward_next_port=3000)
    emulation_config.skip_exploration = True
    model_path_dir = "/home/kim/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/" \
                     "difficulty_level_9/hello_world"
    # model_path_dir = "/home/kim/pycr/python-envs/minigames/network_intrusion/ctf/" \
    #                  "gym-pycr-ctf/examples/difficulty_level_9/hello_world/"
    emulation_config.save_dynamics_model_dir = model_path_dir

    env = gym.make("pycr-ctf-level-9-generated-sim-v6", env_config=None, emulation_config=emulation_config)
    #env = gym.make("pycr-ctf-level-9-emulation-v5", env_config=None, emulation_config=emulation_config)
    env.env_config.attacker_use_nmap_cache = True
    env.env_config.attacker_use_nikto_cache = True
    env.env_config.attacker_use_file_system_cache = True
    env.env_config.attacker_use_user_command_cache = True
    env.env_config.randomize_attacker_starting_state = False
    env.env_config.attacker_max_exploration_steps = 5000
    env.env_config.attacker_max_exploration_trajectories = 1000
    env.env_config.domain_randomization = False
    env.env_config.emulate_detection = False
    env.env_config.explore_defense_states = False
    env.env_config.use_attacker_action_stats_to_update_defender_state = False
    env.env_config.defender_sleep_before_state_update = 0
    env.env_config.attacker_continue_action_sleep = 0

    #env = gym.make("pycr-ctf-level-4-generated-sim-v5", env_config=None, emulation_config=emulation_config)

    #attacker_opponent = RandomAttackerBotAgent(env_config = env.env_config, env=env)

    # Novice Attacker
    # attacker_opponent = CustomAttackerBotAgent(
    #     env_config=env.env_config, env=env,
    #     # TCP/UDP Scan, SSH Brute (0), Telnet Brute (1), FTP Brute (4), Login, Install Tools, Backdoor, Continue,
    #     # TCP/UDP Scan, Shellshock (CVE-2014-6271) (24) with backdoor, Login, Install Tools,
    #     # Continue, SSH brute (25), Login,
    #     # CVE-2010-0426 (25), Continue, TCP/UDP Scan
    #     strategy=[99, 33, 1, 70, 104, 106, 107, 99, 165, 104, 106, 58, 104, 331, 99],
    #     random_start=True, start_p=0.2, continue_action=372)
    # env.env_config.attacker_prevented_stops_remaining = 2

    # Experienced Attacker
    attacker_opponent = CustomAttackerBotAgent(
        env_config=env.env_config, env=env,
        # Continue, Ping Scan, SambaCry Exploit(1) with backdoor,
        # Shellshock (CVE-2014-6271) (24) with backdoor, login, SSH brute (25), Login, CVE-2010-0426 (25),
        # Ping scan, SQL injection (26), Login, Install tools,
        # Ping scan, CVE-2015-1427 (26), Login, Install Tools,
        strategy=[100, 109, 33, 104, 106, 107, 100, 165, 104, 58, 104, 331, 106, 100, 200, 104, 106, 100,
                  266, 104, 106],
        random_start=True, start_p=0.2, continue_action=372)
    env.env_config.attacker_prevented_stops_remaining = 1

    # Expert attacker
    # attacker_opponent = CustomAttackerBotAgent(
    #     env_config=env.env_config, env=env,
    #     # Continue, Ping Scan, SambaCry Exploit(1) with backdoor, Login, Install tools, Backdoor, Ping Scan
    #     # SQL Injection (25) with backdoor, Login, Install Tools, Ping Scan
    #     # CVE-2015-1427 (25) with backdoor, Login, Install Tools, Ping Scan
    #     # SambaCry Exploit(5) with backdoor, Login
    #     strategy=[100, 109, 104, 106, 100, 199, 104, 106,100, 265, 104, 106, 100, 113, 104],
    #     random_start=True, start_p=0.2, continue_action=372)
    # env.env_config.attacker_prevented_stops_remaining = 0

    env.env_config.attacker_static_opponent = attacker_opponent

    ManualDefenderAgent(env=env, env_config=env.env_config)




if __name__ == '__main__':
    manual_control()