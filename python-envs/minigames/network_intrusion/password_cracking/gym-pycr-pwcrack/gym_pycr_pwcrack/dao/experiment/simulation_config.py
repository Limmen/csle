import csv

class SimulationConfig:

    def __init__(self, num_episodes: int = 10, video_fps=5,
                 video=False, gif_dir=None, video_dir=None, gifs=False, render=False, sleep=0.35,
                 log_frequency = 1, video_frequency = 100):
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

    def to_str(self) -> str:
        """
        :return: a string with information about all of the parameters
        """
        return "Hyperparameters: render:{0},sleep:{1}," \
               "log_frequency:{2}," \
               "video:{3},video_fps:{4}," \
               "video_dir:{5},num_episodes:{6},gifs:{7}," \
               "gifdir:{8},video_frequency:{9}".format(
            self.render, self.sleep,
            self.log_frequency, self.video,
            self.video_fps, self.video_dir, self.num_episodes, self.gifs, self.gif_dir, self.video_frequency)

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
