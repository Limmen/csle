from csle_common.dao.network.trajectory import Trajectory
from typing import List

def analyze_taus():
    taus : List[Trajectory] = Trajectory.load_traces(
        traces_save_dir="/",
        traces_file="taus.json")

    Trajectory.save_traces(
        traces_save_dir="/",
        traces_file="one_tau_1.json",
        traces=taus[-1:]
    )

if __name__ == '__main__':
    analyze_taus()