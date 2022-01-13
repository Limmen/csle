from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
import csle_common.constants.constants as constants
import gym
import os

def test_env(env_name : str, num_steps : int):
    # emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim")
    # emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(agent_ip="172.18.4.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False)
    emulation_config.save_dynamics_model_dir = "/home/kim/csle/simulation-system/use_cases/intrusion_prevention/minigames/ctf/" \
                                               "gym-csle-ctf/examples/difficulty_level_4/hello_world/"
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config)

    defender_dynamics_model = DefenderDynamicsModel()
    if env.env_config.emulation_config.save_dynamics_model_dir is not None:
        defender_dynamics_model.read_model(env.env_config.emulation_config.save_dynamics_model_dir)
        load_dir = env.env_config.emulation_config.save_dynamics_model_dir + "/" + \
                   constants.SYSTEM_IDENTIFICATION.NETWORK_CONF_FILE
        if os.path.exists(load_dir):
            env.env_config.network_conf = \
                env.env_config.network_conf.load(load_dir)

    print(defender_dynamics_model)
    defender_dynamics_model.normalize()
    print(defender_dynamics_model.norm_num_new_alerts)
    print(defender_dynamics_model.norm_num_new_alerts[(85, '172.18.4.191')].mean())
    print(defender_dynamics_model.norm_num_new_alerts[(85, '172.18.4.191')].std())
    print(defender_dynamics_model.norm_num_new_alerts[(85, '172.18.4.191')].var())

    # env.reset()
    # env.close()


def test_all():
    #test_env("csle-ctf-level-4-emulation-v1", num_steps=1000000000)
    #test_env("csle-ctf-level-4-generated-sim-v1", num_steps=1000000000)
    #test_env("csle-ctf-level-4-emulation-v2", num_steps=1000000000)
    #test_env("csle-ctf-level-4-emulation-v3", num_steps=1000000000)
    #test_env("csle-ctf-level-4-emulation-v4", num_steps=1000000000)
    test_env("csle-ctf-level-4-emulation-v5", num_steps=1000000000)
    #test_env("csle-ctf-level-4-generated-sim-v5", num_steps=1000000000)
    #

if __name__ == '__main__':
    test_all()