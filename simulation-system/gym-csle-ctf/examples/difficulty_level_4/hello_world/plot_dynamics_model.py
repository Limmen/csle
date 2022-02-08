from gym_csle_ctf.util.plots import plot_dynamics_model

def plot():
    print("reading model")
    path = "/Users/kimham/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_4/hello_world/defender_dynamics_model.json"
    defender_dynamics_model = plot_dynamics_model.read_model(path)
    print("model read")
    #plot_dynamics_model.plot_all(defender_dynamics_model)
    plot_dynamics_model.plot_ids_infra_and_one_machine(defender_dynamics_model)

if __name__ == '__main__':
    plot()