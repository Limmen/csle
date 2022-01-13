from csle_common.dao.network.trajectory import Trajectory
from typing import List

def analyze_taus():
    taus : List[Trajectory] = Trajectory.load_trajectories(
        trajectories_save_dir="/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world",
        trajectories_file="taus_backup19_aug.json")
    #
    filtered_taus = []
    for tau in taus:
        if (tau.attacker_actions[0] == -1
                and tau.attacker_actions[1] == 372
                and tau.attacker_actions[2] == 99
                and tau.attacker_actions[3] == 33
                and tau.attacker_actions[4] == 1
                and tau.attacker_actions[5] == 70
        ):
            filtered_taus.append(tau)
        elif (tau.attacker_actions[0] == -1
                and tau.attacker_actions[1] == 372
                and tau.attacker_actions[2] == 100
                and tau.attacker_actions[3] == 109
                and tau.attacker_actions[4] == 33
                and tau.attacker_actions[5] == 104
        ):
            x = 0
            if len(tau.defender_observations[0]) == 9:
                x = tau.defender_observations[2][2]
                y = tau.defender_observations[2][3]
                z = 0
            elif len(tau.defender_observations[0]) == 4:
                x = tau.defender_observations[2][0]
                y = tau.defender_observations[2][1]
                z = tau.defender_observations[2][2]
            # print(x)
            if x > 0:
                filtered_taus.append(tau)
                print(tau.defender_observations[2])
        elif (tau.attacker_actions[0] == -1
                and tau.attacker_actions[1] == 372
                and tau.attacker_actions[2] == 100
                and tau.attacker_actions[3] == 109
                and tau.attacker_actions[4] == 104
                and tau.attacker_actions[5] == 106
        ):
            x = 0
            if len(tau.defender_observations[0]) == 9:
                x = tau.defender_observations[2][2]
                y = tau.defender_observations[2][3]
                z = 0
            elif len(tau.defender_observations[0]) == 4:
                x = tau.defender_observations[2][0]
                y = tau.defender_observations[2][1]
                z = tau.defender_observations[2][2]
            # print(x)
            if x > 0:
                print(tau.defender_observations[2])
                filtered_taus.append(tau)
    Trajectory.save_trajectories(
        trajectories_save_dir="/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world",
        trajectories_file="filtered_taus.json",
        trajectories = filtered_taus
    )

if __name__ == '__main__':
    analyze_taus()