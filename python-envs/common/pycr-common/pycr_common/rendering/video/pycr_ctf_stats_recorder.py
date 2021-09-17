import json
import os
import time

from gym import error
from gym.utils import atomic_write
from gym.utils.json_utils import json_encode_np


class StatsRecorder(object):
    """
    Helper class for recording statistics about video and gif recordings
    """
    def __init__(self, directory, file_prefix, autoreset=False, env_id=None):
        self.autoreset = autoreset
        self.env_id = env_id

        self.initial_reset_timestamp = None
        self.directory = directory
        self.file_prefix = file_prefix
        self.episode_lengths = []
        self.episode_rewards_1 = []
        self.episode_rewards_2 = []
        self.episode_types = [] # experimental addition
        self._type = 't'
        self.timestamps = []
        self.steps = None
        self.total_steps = 0
        self.rewards_1 = None
        self.rewards_2 = None

        self.done = None
        self.closed = False

        filename = '{}.stats.json'.format(self.file_prefix)
        self.path = os.path.join(self.directory, filename)

    @property
    def type(self):
        """
        :return: the type of the stats recorder
        """
        return self._type

    @type.setter
    def type(self, type) -> None:
        """
        Sets the type of the stats recorded

        :param type:  the type to set
        :return: None
        """
        if type not in ['t', 'e']:
            raise error.Error('Invalid episode type {}: must be t for training or e for evaluation', type)
        self._type = type

    def before_step(self, action) -> None:
        """
        Utility function called before each step
        :param action: the action of the step
        :return: None
        """
        assert not self.closed

        if self.done:
            raise error.ResetNeeded("Trying to step environment which is currently done. While the monitor "
                                    "is active for {}, you cannot step beyond the end of an episode. "
                                    "Call 'env.reset()' to start the next episode.".format(self.env_id))
        elif self.steps is None:
            raise error.ResetNeeded("Trying to step an environment before reset. While the monitor is active for {}, "
                                    "you must call 'env.reset()' before taking an initial step.".format(self.env_id))

    def after_step(self, observation, reward: float, done: bool, info: dict) -> None:
        """
        Function called after each step

        :param observation: the observation of the step
        :param reward: the reward of the step
        :param done: whether the interaction with the environment is done or not
        :param info: the info dict
        :return: None
        """
        self.steps += 1
        self.total_steps += 1
        if type(reward) == tuple:
            reward_1, reward_2 = reward
            self.rewards_1 += reward_1
            self.rewards_2 += reward_2
        elif type(reward) == list:
            reward_1 = reward[0]
            reward_2 = reward[1]
            self.rewards_1 += reward_1
            self.rewards_2 += reward_2
        else:
            self.rewards_1 += reward
        self.done = done

        if done:
            self.save_complete()

        if done:
            if self.autoreset:
                self.before_reset()
                self.after_reset(observation)

    def before_reset(self) -> None:
        """
        Function called before the reset of the environment

        :return: None
        """
        assert not self.closed

        # if self.done is not None and not self.done and self.steps > 0:
        #     raise error.Error("Tried to reset environment which is not done.
        #     While the monitor is active for {}, you cannot call reset()
        #     unless the episode is over.".format(self.env_id))

        self.done = False
        if self.initial_reset_timestamp is None:
            self.initial_reset_timestamp = time.time()

    def after_reset(self, observation) -> None:
        """
        Function called after the reset of the environment

        :param observation: the observation of the reset
        :return: None
        """
        self.steps = 0
        self.rewards_1 = 0
        self.rewards_2 = 0
        # We write the type at the beginning of the episode. If a user
        # changes the type, it's more natural for it to apply next
        # time the user calls reset().
        self.episode_types.append(self._type)

    def save_complete(self) -> None:
        """
        Completes the saving

        :return: None
        """
        if self.steps is not None:
            self.episode_lengths.append(self.steps)
            self.episode_rewards_1.append(float(self.rewards_1))
            self.episode_rewards_2.append(float(self.rewards_2))
            self.timestamps.append(time.time())

    def close(self) -> None:
        """
        Closes the environment

        :return: None
        """
        self.flush()
        self.closed = True

    def flush(self) -> None:
        """
        Flushes the environment
        :return:
        """
        if self.closed:
            return

        with atomic_write.atomic_write(self.path) as f:
            json.dump({
                'initial_reset_timestamp': self.initial_reset_timestamp,
                'timestamps': self.timestamps,
                'episode_lengths': self.episode_lengths,
                'episode_rewards': self.episode_rewards_1,
                'episode_rewards_2': self.episode_rewards_2,
                'episode_types': self.episode_types,
            }, f, default=json_encode_np)
