from pycr_common.dao.network.trajectory import Trajectory
from typing import List

def analyze_taus():
    taus : List[Trajectory] = Trajectory.load_trajectories(
        trajectories_save_dir="./",
        trajectories_file="taus.json")

    Trajectory.save_trajectories(
        trajectories_save_dir="./",
        trajectories_file="one_tau_1.json",
        trajectories = taus[-1:]
    )

if __name__ == '__main__':
    analyze_taus()