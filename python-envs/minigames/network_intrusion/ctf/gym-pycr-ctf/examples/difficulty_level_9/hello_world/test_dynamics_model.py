from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env import PyCRCTFLevel1Emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
import gym_pycr_ctf.constants.constants as constants
import gym
import time
import numpy as np
import os
import json

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
    save_dynamics_model_dir = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/" \
                                               "gym-pycr-ctf/examples/difficulty_level_9/hello_world/"
    #env = gym.make(env_name, env_config=None, emulation_config=emulation_config)

    defender_dynamics_model = DefenderDynamicsModel()
    new_model = DefenderDynamicsModel()
    if save_dynamics_model_dir is not None:
        print("loading dynamics model")
        defender_dynamics_model.read_model(save_dynamics_model_dir, model_name="defender_dynamics_model.json")
        new_model.read_model(save_dynamics_model_dir, model_name="defender_dynamics_model.json")
        print("model loaded")
        # if os.path.exists(load_dir):
        #     env.env_config.network_conf = \
        #         env.env_config.network_conf.load(load_dir)

    #print(defender_dynamics_model)
    #print(defender_dynamics_model.num_new_alerts)
    for k,v in defender_dynamics_model.num_new_alerts.items():
        for k2,v2 in v.items():
            #print("action:{}, state:{}".format(k, k2))
            for k3,v3 in v2.items():
                if int(k) == 85 and int(k3) > 0:
                    if int(k3) > 50:
                        new_model.num_new_alerts[k][k2][str(50)] = new_model.num_new_alerts[k][k2][k3]
                        del new_model.num_new_alerts[k][k2][k3]
                elif (int(k) == 19 or int(k) == 11 or int(k) == 12 or int(k) == 10 or int(k) == 54 or int(k) == 55 or int(k) == 59 or int(k) == 57 or int(k) == 53):
                    if k3 in new_model.num_new_alerts[k][k2]:
                        if int(k3) > 200:
                            new_model.num_new_alerts[k][k2][str(200)] = new_model.num_new_alerts[k][k2][k3]
                            del new_model.num_new_alerts[k][k2][k3]
                        elif int(k3) < 60 and int(k3) > 20:
                            new_model.num_new_alerts[k][k2][str(int(k3)*3)] = new_model.num_new_alerts[k][k2][k3]
                            del new_model.num_new_alerts[k][k2][k3]
                        elif int(k3) <= 20:
                            new_model.num_new_alerts[k][k2][str(int(k3) * 10)] = new_model.num_new_alerts[k][k2][k3]
                            del new_model.num_new_alerts[k][k2][k3]
                    if 0 in new_model.num_new_alerts[k][k2]:
                        del new_model.num_new_alerts[k][k2][0]
                    if 0.0 in new_model.num_new_alerts[k][k2]:
                        del new_model.num_new_alerts[k][k2][0.0]
                    if "0" in new_model.num_new_alerts[k][k2]:
                        del new_model.num_new_alerts[k][k2]["0"]
                    if "0.0" in new_model.num_new_alerts[k][k2]:
                        del new_model.num_new_alerts[k][k2]["0.0"]

    for k, v in defender_dynamics_model.num_new_priority.items():
        for k2, v2 in v.items():
            # print("action:{}, state:{}".format(k, k2))
            for k3, v3 in v2.items():
                if int(k) == 85 and int(k3) > 0:
                    if int(k3) > 50:
                        new_model.num_new_priority[k][k2][str(50)] = new_model.num_new_priority[k][k2][k3]
                        del new_model.num_new_priority[k][k2][k3]
                elif (int(k) == 19 or int(k) == 11 or int(k) == 12 or int(k) == 10 or int(k) == 54 or int(
                        k) == 55 or int(k) == 59 or int(k) == 57 or int(k) == 53):
                    if k3 in new_model.num_new_priority[k][k2]:
                        if int(k3) > 200:
                            new_model.num_new_priority[k][k2][str(200)] = new_model.num_new_priority[k][k2][k3]
                            del new_model.num_new_priority[k][k2][k3]
                        elif int(k3) < 60 and int(k3) > 20:
                            new_model.num_new_priority[k][k2][str(int(k3) * 3)] = new_model.num_new_priority[k][k2][k3]
                            del new_model.num_new_priority[k][k2][k3]
                        elif int(k3) <= 20:
                            new_model.num_new_priority[k][k2][str(int(k3) * 10)] = new_model.num_new_priority[k][k2][k3]
                            del new_model.num_new_priority[k][k2][k3]
                    if 0 in new_model.num_new_priority[k][k2]:
                        del new_model.num_new_priority[k][k2][0]
                    if 0.0 in new_model.num_new_priority[k][k2]:
                        del new_model.num_new_priority[k][k2][0.0]
                    if "0" in new_model.num_new_priority[k][k2]:
                        del new_model.num_new_priority[k][k2]["0"]

    for k, v in defender_dynamics_model.num_new_severe_alerts.items():
        for k2, v2 in v.items():
            # print("action:{}, state:{}".format(k, k2))
            for k3, v3 in v2.items():
                if int(k) == 85 and int(k3) > 0:
                    if int(k3) > 50:
                        new_model.num_new_severe_alerts[k][k2][str(50)] = new_model.num_new_severe_alerts[k][k2][k3]
                        del new_model.num_new_severe_alerts[k][k2][k3]
                elif (int(k) == 19 or int(k) == 11 or int(k) == 12 or int(k) == 10 or int(k) == 54 or int(
                        k) == 55 or int(k) == 59 or int(k) == 57 or int(k) == 53):
                    if k3 in new_model.num_new_severe_alerts[k][k2]:
                        if int(k3) > 200:
                            new_model.num_new_severe_alerts[k][k2][str(200)] = new_model.num_new_severe_alerts[k][k2][k3]
                            del new_model.num_new_severe_alerts[k][k2][k3]
                        elif int(k3) < 60 and int(k3) > 20:
                            new_model.num_new_severe_alerts[k][k2][str(int(k3) * 3)] = new_model.num_new_severe_alerts[k][k2][k3]
                            del new_model.num_new_severe_alerts[k][k2][k3]
                        elif int(k3) <= 20:
                            new_model.num_new_severe_alerts[k][k2][str(int(k3) * 10)] = new_model.num_new_severe_alerts[k][k2][k3]
                            del new_model.num_new_severe_alerts[k][k2][k3]
                    if 0 in new_model.num_new_severe_alerts[k][k2]:
                        del new_model.num_new_severe_alerts[k][k2][0]
                    if 0.0 in new_model.num_new_severe_alerts[k][k2]:
                        del new_model.num_new_severe_alerts[k][k2][0.0]
                    if "0" in new_model.num_new_severe_alerts[k][k2]:
                        del new_model.num_new_severe_alerts[k][k2]["0"]

    for k, v in defender_dynamics_model.num_new_warning_alerts.items():
        for k2, v2 in v.items():
            # print("action:{}, state:{}".format(k, k2))
            for k3, v3 in v2.items():
                if int(k) == 85 and int(k3) > 0:
                    if int(k3) > 50:
                        new_model.num_new_warning_alerts[k][k2][str(50)] = new_model.num_new_warning_alerts[k][k2][k3]
                        del new_model.num_new_warning_alerts[k][k2][k3]
                elif (int(k) == 19 or int(k) == 11 or int(k) == 12 or int(k) == 10 or int(k) == 54 or int(
                        k) == 55 or int(k) == 59 or int(k) == 57 or int(k) == 53):
                    if k3 in new_model.num_new_warning_alerts[k][k2]:
                        if int(k3) > 200:
                            new_model.num_new_warning_alerts[k][k2][str(200)] = new_model.num_new_warning_alerts[k][k2][k3]
                            del new_model.num_new_warning_alerts[k][k2][k3]
                        elif int(k3) < 60 and int(k3) > 20:
                            new_model.num_new_warning_alerts[k][k2][str(int(k3) * 3)] = new_model.num_new_warning_alerts[k][k2][k3]
                            del new_model.num_new_warning_alerts[k][k2][k3]
                        elif int(k3) <= 20:
                            new_model.num_new_warning_alerts[k][k2][str(int(k3) * 10)] = new_model.num_new_warning_alerts[k][k2][k3]
                            del new_model.num_new_warning_alerts[k][k2][k3]
                    if 0 in new_model.num_new_warning_alerts[k][k2]:
                        del new_model.num_new_warning_alerts[k][k2][0]
                    if 0.0 in new_model.num_new_warning_alerts[k][k2]:
                        del new_model.num_new_warning_alerts[k][k2][0.0]
                    if "0" in new_model.num_new_warning_alerts[k][k2]:
                        del new_model.num_new_warning_alerts[k][k2]["0"]

    print("normalizing model counts")
    new_model.normalize()
    print("model counts normalized")
    # print(defender_dynamics_model.norm_num_new_alerts)
    print("85:")
    print(new_model.norm_num_new_alerts[(85, '172.18.9.191')].mean())
    print(new_model.norm_num_new_alerts[(85, '172.18.9.191')].std())
    print(new_model.norm_num_new_alerts[(85, '172.18.9.191')].var())

    print("19:")
    print(new_model.norm_num_new_alerts[(19, '172.18.9.191')].mean())
    print(new_model.norm_num_new_alerts[(19, '172.18.9.191')].std())
    print(new_model.norm_num_new_alerts[(19, '172.18.9.191')].var())
    #
    print("11:")
    print(new_model.norm_num_new_alerts[(11, '172.18.9.191')].mean())
    print(new_model.norm_num_new_alerts[(11, '172.18.9.191')].std())
    print(new_model.norm_num_new_alerts[(11, '172.18.9.191')].var())

    # print("12:")
    # print(defender_dynamics_model.norm_num_new_alerts[(12, '172.18.9.191')].mean())
    # print(defender_dynamics_model.norm_num_new_alerts[(12, '172.18.9.191')].std())
    # print(defender_dynamics_model.norm_num_new_alerts[(12, '172.18.9.191')].var())


    # env.reset()
    # env.close()
    d = new_model.to_dict()
    with open("defender_dynamics_model.json", 'w') as fp:
        json.dump(d, fp)


def test_all():
    test_env("pycr-ctf-level-9-emulation-v5", num_steps=1000000000)

if __name__ == '__main__':
    test_all()