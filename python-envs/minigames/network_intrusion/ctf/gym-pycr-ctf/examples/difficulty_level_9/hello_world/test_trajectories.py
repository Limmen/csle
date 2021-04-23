from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env import PyCRCTFLevel1Emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
from gym_pycr_ctf.dao.network.trajectory import Trajectory

def test_trajectories():
    # save_dynamics_model_dir = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/" \
    #                                            "gym-pycr-ctf/examples/difficulty_level_9/hello_world/"
    save_dynamics_model_dir = "/home/kim/pycr/python-envs/minigames/network_intrusion/ctf/" \
                              "gym-pycr-ctf/examples/difficulty_level_9/hello_world/"
    trajectories = Trajectory.load_trajectories(save_dynamics_model_dir, trajectories_file="taus6.json")
    print(len(trajectories))
    # print(trajectories)
    for j in range(5):
        for i in range(10):
            print("a:{}, new alerts:{}".format(trajectories[j].attacker_actions[i], trajectories[j].defender_observations[i][0]))


def test_all():
    test_trajectories()

if __name__ == '__main__':
    test_all()