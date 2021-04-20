from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env import PyCRCTFLevel1Emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
import gym_pycr_ctf.constants.constants as constants
import gym
import time
import numpy as np
import os

def test_env(env_name : str, num_steps : int):
    # emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
                                   agent_username="agent", agent_pw="agent", server_connection=True,
                                   server_private_key_file="/home/kim/.ssh/id_rsa",
                                   server_username="kim")
    # emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
    #                                  server_connection=False)
    emulation_config.save_dynamics_model_dir = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/" \
                                               "gym-pycr-ctf/examples/difficulty_level_9/hello_world/"
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config)

    defender_dynamics_model = DefenderDynamicsModel()
    if env.env_config.emulation_config.save_dynamics_model_dir is not None:
        print("loading dynamics model")
        defender_dynamics_model.read_model(env.env_config)
        load_dir = env.env_config.emulation_config.save_dynamics_model_dir + "/" + \
                   constants.SYSTEM_IDENTIFICATION.NETWORK_CONF_FILE
        if os.path.exists(load_dir):
            env.env_config.network_conf = \
                env.env_config.network_conf.load(load_dir)

    print(defender_dynamics_model)
    print(defender_dynamics_model.num_new_alerts)
    for k,v in defender_dynamics_model.num_new_alerts.items():
        if int(k) == 85 or int(k) == 19:
            print("action:{}".format(k))
            for k2,v2 in v.items():
                for k3,v3 in v2.items():
                    print("value:{}".format(k3))
                    print("count:{}".format(v3))
    defender_dynamics_model.normalize()
    # print(defender_dynamics_model.norm_num_new_alerts)
    print("85:")
    print(defender_dynamics_model.norm_num_new_alerts[(85, '172.18.9.191')].mean())
    print(defender_dynamics_model.norm_num_new_alerts[(85, '172.18.9.191')].std())
    print(defender_dynamics_model.norm_num_new_alerts[(85, '172.18.9.191')].var())

    print("19:")
    print(defender_dynamics_model.norm_num_new_alerts[(19, '172.18.9.191')].mean())
    print(defender_dynamics_model.norm_num_new_alerts[(19, '172.18.9.191')].std())
    print(defender_dynamics_model.norm_num_new_alerts[(19, '172.18.9.191')].var())

    print(defender_dynamics_model.norm_num_new_alerts[(19, '172.18.9.191')].mean())

    # env.reset()
    # env.close()


def test_all():
    test_env("pycr-ctf-level-9-emulation-v5", num_steps=1000000000)

if __name__ == '__main__':
    test_all()