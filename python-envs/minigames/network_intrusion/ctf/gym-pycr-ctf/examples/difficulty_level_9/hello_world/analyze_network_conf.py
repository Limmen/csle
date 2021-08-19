from gym_pycr_ctf.dao.network.network_config import NetworkConfig

def merge_network_confs():
    conf1 = NetworkConfig.load(dir_path="/home/kim/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world",
                       file_name="network_conf.pickle")
    conf2 = NetworkConfig.load(
        dir_path="/home/kim/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world",
        file_name="network_conf2.pickle")
    conf1.merge(conf2)
    conf1.save(dir_path="/home/kim/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world",
               file_name="network_conf10.pickle")

if __name__ == '__main__':
    merge_network_confs()