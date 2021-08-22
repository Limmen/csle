from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
from gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env import PyCrCTFLevel9Base
from gym_pycr_ctf.util.plots import plot_dynamics_model

def plot():
    print("reading model")
    path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world/defender_dynamics_model.json"
    defender_dynamics_model = plot_dynamics_model.read_model(path)
    print("model read")
    #plot_dynamics_model.plot_all(defender_dynamics_model)
    actions_conf = PyCrCTFLevel9Base.attacker_all_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                               subnet_mask="test", hacker_ip="test")
    plot_dynamics_model.plot_ids_infra_and_one_machine_2(defender_dynamics_model)

if __name__ == '__main__':
    plot()