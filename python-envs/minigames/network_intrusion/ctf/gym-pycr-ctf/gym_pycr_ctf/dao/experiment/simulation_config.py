import csv

class SimulationConfig:
    """
    Object representing the configuration of a simulation
    """

    def __init__(self, num_episodes: int = 10, video_fps=5,
                 video=False, gif_dir=None, video_dir=None, gifs=False, render=False, sleep=0.35,
                 log_frequency = 1, video_frequency = 100, domain_randomization: bool = False,
                 dr_max_num_nodes: int = 4, dr_min_num_nodes: int = 1,
                 dr_min_num_flags: int = 1, dr_max_num_flags: int = 1,
                 dr_min_num_users: int = 1, dr_max_num_users: int = 1,
                 dr_use_base: bool = False
                 ):
        """
        Initializes the object

        :param num_episodes: the number of episodes of the simulation
        :param video_fps: the video fps of the simulation
        :param video: whether to record video of the simulation
        :param gif_dir: the gif directory of the simulation
        :param video_dir: the video directory of the simulation
        :param gifs: whether to record gifs of the simulation
        :param render: whether to render the simulation
        :param sleep: sleeping time of the simulation
        :param log_frequency: the log frequency of the simulation
        :param video_frequency: the video frequency of the simulation
        :param domain_randomization: whether to use domain randomization
        :param dr_max_num_nodes: the maximum nodes for domain randomization of the simulation
        :param dr_min_num_nodes: the minimum nodes for domain randomization of the simulation
        :param dr_min_num_flags: the minimum flags for domain randomization of the simulation
        :param dr_max_num_flags: the maximum flags for domain randomization of the simulation
        :param dr_min_num_users: the minimum users for domain randomization of the simulation
        :param dr_max_num_users: the maximum users for domain randomization of the simulation
        :param dr_use_base: boolean flag whether to use the base randomization space for domain randomization
        """
        self.num_episodes = num_episodes
        self.video_fps = video_fps
        self.video = video
        self.gif_dir = gif_dir
        self.video_dir = video_dir
        self.gifs = gifs
        self.render = render
        self.sleep = sleep
        self.log_frequency = log_frequency
        self.logger = None
        self.video_frequency = video_frequency
        self.domain_randomization = domain_randomization
        self.dr_use_base = dr_use_base
        self.dr_max_num_nodes = dr_max_num_nodes
        self.dr_min_num_nodes = dr_min_num_nodes
        self.dr_min_num_flags = dr_min_num_flags
        self.dr_max_num_flags = dr_max_num_flags
        self.dr_min_num_users = dr_min_num_users
        self.dr_max_num_users = dr_max_num_users

    def to_str(self) -> str:
        """
        :return: a string with information about all of the parameters
        """
        return "Hyperparameters: render:{0},sleep:{1}," \
               "log_frequency:{2}," \
               "video:{3},video_fps:{4}," \
               "video_dir:{5},num_episodes:{6},gifs:{7}," \
               "gifdir:{8},video_frequency:{9},dr:{10}, dr_max_num_nodes:{11}," \
               "dr_min_num_nodes:{12},dr_max_num_flags:{13},dr_min_num_flags:{14}," \
               "dr_max_num_users:{15},dr_min_num_users:{16},dr_use_base:{17}".format(
            self.render, self.sleep, self.log_frequency, self.video, self.video_fps, self.video_dir, self.num_episodes,
            self.gifs, self.gif_dir, self.video_frequency, self.domain_randomization, self.dr_max_num_nodes,
            self.dr_min_num_nodes, self.dr_max_num_flags, self.dr_min_num_flags, self.dr_max_num_users,
            self.dr_min_num_users, self.dr_use_base)

    def to_csv(self, file_path: str) -> None:
        """
        Write parameters to csv file

        :param file_path: path to the file
        :return: None
        """
        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["parameter", "value"])
            writer.writerow(["render", str(self.render)])
            writer.writerow(["sleep", str(self.sleep)])
            writer.writerow(["log_frequency", str(self.log_frequency)])
            writer.writerow(["video", str(self.video)])
            writer.writerow(["video_fps", str(self.video_fps)])
            writer.writerow(["video_dir", str(self.video_dir)])
            writer.writerow(["num_episodes", str(self.num_episodes)])
            writer.writerow(["gifs", str(self.gifs)])
            writer.writerow(["gifdir", str(self.gif_dir)])
            writer.writerow(["video_frequency", str(self.video_frequency)])
            writer.writerow(["domain_randomization", str(self.domain_randomization)])
            writer.writerow(["dr_max_num_nodes", str(self.dr_max_num_nodes)])
            writer.writerow(["dr_min_num_nodes", str(self.dr_min_num_nodes)])
            writer.writerow(["dr_max_num_flags", str(self.dr_max_num_flags)])
            writer.writerow(["dr_min_num_flags", str(self.dr_min_num_flags)])
            writer.writerow(["dr_max_num_users", str(self.dr_max_num_users)])
            writer.writerow(["dr_min_num_users", str(self.dr_min_num_users)])
            writer.writerow(["dr_use_base", str(self.dr_use_base)])
