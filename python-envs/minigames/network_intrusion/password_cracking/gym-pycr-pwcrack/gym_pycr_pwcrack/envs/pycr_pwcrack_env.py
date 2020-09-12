import gym
from abc import ABC
import numpy as np

class PyCRPwCrackEnv(gym.Env, ABC):
    """
    TODO
    """

    def __init__(self):
        self.observation_space = gym.spaces.Box(low=0, high=10, dtype=np.int32, shape=(10, 10,))
        self.action_space = gym.spaces.Discrete(1)
        self.viewer = None
        self.steps_beyond_done = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }
        self.reward_range = (float(0), float(1))
        self.num_states = 100
        self.score = 0
        self.step_outcome = None

    # -------- API ------------
    def step(self) -> np.ndarray:
        pass


    def reset(self) -> np.ndarray:
        pass

    def render(self, mode: str = 'human'):
        """
        Renders the environment
        Supported rendering modes:
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        pass
        # if mode not in self.metadata["render.modes"]:
        #     raise NotImplemented("mode: {} is not supported".format(mode))
        # if self.viewer is None:
        #     self.__setup_viewer()
        # self.viewer.mainframe.set_state(self.state)
        # arr = self.viewer.render(return_rgb_array=mode == 'rgb_array', step_outcome = self.step_outcome)
        # return arr

    def close(self) -> None:
        """
        Closes the viewer (cleanup)
        :return: None
        """
        # if self.viewer:
        #     self.viewer.close()
        #     self.viewer = None
        #     self.config.render_config.new_window()
        pass

    # -------- Private methods ------------
    def __setup_viewer(self):
        """
        Setup for the viewer to use for rendering
        :return: None
        """
        # from gym_cgc_bta.envs.rendering.viewer import Viewer
        # script_dir = os.path.dirname(__file__)
        # resource_path = os.path.join(script_dir, './rendering/', constants.RENDERING.RESOURCES_DIR)
        # self.config.render_config.resources_dir = resource_path
        # self.viewer = Viewer(config=self.config, state=self.state)
        # self.viewer.start()
        pass

# -------- Concrete envs ------------

# -------- Difficulty 1 (Simple) ------------

# -------- Version 1 ------------
class PyCRPwCrackSimple1Env(PyCRPwCrackEnv):
    def __init__(self):
        pass

# -------- Difficulty 2 (Medium) ------------

# -------- Difficulty 3 (Hard) ------------
