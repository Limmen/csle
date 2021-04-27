from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent
from gym_pycr_ctf.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from gym_pycr_ctf.envs_model.logic.common.domain_randomizer import DomainRandomizer
import gym

def manual_control():
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/storage/workspace/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_train/")
    flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/storage/workspace/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_train/")
    # eval_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/storage/workspace/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_2/")
    # eval_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/storage/workspace/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_2/")
    max_num_nodes_train = max(list(map(lambda x: len(x.containers), containers_configs)))
    #max_num_nodes_eval = max(list(map(lambda x: len(x.containers), eval_containers_configs)))
    #max_num_nodes = max(max_num_nodes_train, max_num_nodes_eval)
    max_num_nodes = max_num_nodes_train
    idx = 2
    emulation_config = EmulationConfig(agent_ip=containers_configs[idx].agent_ip, agent_username="agent", agent_pw="agent",
                                   server_connection=False, port_forward_next_port=9800)
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip=containers_configs[idx].agent_ip,
    #                                  agent_username="agent", agent_pw="agent", server_connection=True,
    #                                  server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                  server_username="kim")
    #env_name = "pycr-ctf-random-many-generated-sim-v1"
    env_name = "pycr-ctf-random-many-emulation-v1"
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config,
                   containers_configs=containers_configs, flags_configs=flags_configs, idx=idx,
                   num_nodes=max_num_nodes)

    env.reset()
    # randomization_space = DomainRandomizer.generate_randomization_space([env.env_config.network_conf])
    # randomized_network_conf, env_config = DomainRandomizer.randomize(subnet_prefix="172.18.",
    #                                                                  network_ids=list(range(1, 254)),
    #                                                                  r_space=randomization_space,
    #                                                                  env_config=env.env_config)
    #env.env_config = env_config


    ManualAttackerAgent(env=env, env_config=env.env_config,render=True)




if __name__ == '__main__':
    manual_control()