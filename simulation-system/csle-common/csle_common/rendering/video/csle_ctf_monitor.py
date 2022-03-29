from typing import List
from gym import Wrapper
from gym import error, version, logger
import os, json, numpy as np, six
from gym.utils import atomic_write, closer
from gym.utils.json_utils import json_encode_np
import imageio
from csle_common.rendering.video.csle_ctf_stats_recorder import StatsRecorder
from csle_common.rendering.video.csle_ctf_video_recorder import CSLECTFVideoRecorder


FILE_PREFIX = 'openaigym'
MANIFEST_PREFIX = FILE_PREFIX + '.manifest'


class CSLECTFMonitor(Wrapper):
    """
    Helper class that sets up the openAIgym environment for recording videos and GIFs
    """
    def __init__(self, env, directory, video_callable=None, force=False, resume=False,
                 write_upon_reset=False, uid=None, mode=None, video_frequency = 1, openai_baseline = False):
        super(CSLECTFMonitor, self).__init__(env)

        self.videos = []

        self.stats_recorder = None
        self.video_recorder = None
        self.enabled = False
        self.episode_id = 0
        self._monitor_id = None
        self.openai_baseline_reset = True
        self.env_semantics_autoreset = env.metadata.get('semantics.autoreset')
        self._start(directory, video_callable, force, resume,
                            write_upon_reset, uid, mode)
        self.episode_frames = []
        self.video_frequency = video_frequency
        self.openai_baseline = openai_baseline

    def step(self, action):
        self._before_step(action)
        observation, reward, done, info = self.env.step(action)
        done = self._after_step(observation, reward, done, info)
        return observation, reward, done, info

    def reset(self, **kwargs):
        # if (self.openai_baseline and len(self.episode_frames) > 0) or (self.openai_baseline
        # and not self.openai_baseline_reset):
        #     return
        self._before_reset()
        observation = self.env.reset(**kwargs)
        self._after_reset(observation)
        self.openai_baseline_reset = False
        return observation

    def set_monitor_mode(self, mode):
        logger.info("Setting the monitor mode is deprecated and will be removed soon")
        self._set_mode(mode)


    def _start(self, directory, video_callable=None, force=False, resume=False,
              write_upon_reset=False, uid=None, mode=None):
        """
        Start monitoring.

        Args:
            directory (str): A per-training run directory where to record stats.
            video_callable (Optional[function, False]): function that takes in the index of the episode and outputs a boolean,
            indicating whether we should record a video on this episode. The default (for video_callable is None)
            is to take perfect cubes, capped at 1000. False disables video recording.
            force (bool): Clear out existing training data from this directory (by deleting
            every file prefixed with "openaigym.").
            resume (bool): Retain the training data already in this directory, which will be merged with our new data
            write_upon_reset (bool): Write the manifest file on each reset. (This is currently a JSON file,
            so writing it is somewhat expensive.)
            uid (Optional[str]): A unique id used as part of the suffix for the file. By default, uses os.getpid().
            mode (['evaluation', 'training']): Whether this is an evaluation or training episode.
        """
        if self.env.spec is None:
            logger.warn("Trying to monitor an environment which has no 'spec' set. This usually means you did not "
                        "create it via 'gym.make', and is recommended only for advanced users.")
            env_id = '(unknown)'
        else:
            env_id = self.env.spec.id

        if not os.path.exists(directory):
            logger.info('Creating monitor directory %s', directory)
            if six.PY3:
                os.makedirs(directory, exist_ok=True)
            else:
                os.makedirs(directory)

        if video_callable is None:
            video_callable = self.periodic_video_schedule
        elif video_callable == False:
            video_callable = disable_videos
        elif not callable(video_callable):
            raise error.Error('You must provide a function, None, or False for video_callable, '
                              'not {}: {}'.format(type(video_callable), video_callable))
        self.video_callable = video_callable

        # Check on whether we need to clear anything
        if force:
            clear_monitor_files(directory)
        elif not resume:
            training_manifests = detect_training_manifests(directory)
            if len(training_manifests) > 0:
                raise error.Error('''Trying to write to monitor directory {} with existing monitor files: {}.

 You should use a unique directory for each training run, or use 'force=True' to automatically clear 
 previous monitor files.'''.format(directory, ', '.join(training_manifests[:5])))

        self._monitor_id = monitor_closer.register(self)

        self.enabled = True
        self.directory = os.path.abspath(directory)
        # We use the 'openai-gym' prefix to determine if a file is
        # ours
        self.file_prefix = FILE_PREFIX
        self.file_infix = '{}.{}'.format(self._monitor_id, uid if uid else os.getpid())

        self.stats_recorder = StatsRecorder(
            directory, '{}.episode_batch.{}'.format(self.file_prefix, self.file_infix),
            autoreset=self.env_semantics_autoreset, env_id=env_id)

        if not os.path.exists(directory): os.mkdir(directory)
        self.write_upon_reset = write_upon_reset

        if mode is not None:
            self._set_mode(mode)

    def _flush(self, force=False):
        """Flush all relevant monitor information to disk."""
        if not self.write_upon_reset and not force:
            return

        self.stats_recorder.flush()

        # Give it a very distiguished name, since we need to pick it
        # up from the filesystem later.
        path = os.path.join(self.directory, '{}.manifest.{}.manifest.json'.format(self.file_prefix, self.file_infix))
        logger.debug('Writing training manifest file to %s', path)
        with atomic_write.atomic_write(path) as f:
            # We need to write relative paths here since people may
            # move the training_dir around. It would be cleaner to
            # already have the basenames rather than basename'ing
            # manually, but this works for now.
            json.dump({
                'stats': os.path.basename(self.stats_recorder.path),
                'videos': [(os.path.basename(v), os.path.basename(m))
                           for v, m in self.videos],
                'env_info': self._env_info(),
            }, f, default=json_encode_np)

    def close(self):
        """Flush all monitor data to disk and close any open rending windows."""
        super(CSLECTFMonitor, self).close()

        if not self.enabled:
            return
        self.stats_recorder.close()
        if self.video_recorder is not None:
            self._close_video_recorder()
        self._flush(force=True)

        # Stop tracking this for autoclose
        monitor_closer.unregister(self._monitor_id)
        self.enabled = False

        logger.info('''Finished writing results. You can upload them to the scoreboard via gym.upload(%r)''', self.directory)

    def _set_mode(self, mode: str) -> None:
        """
        Sets the mode of the monitoring

        :param mode: the mode to set
        :return: None
        """
        if mode == 'evaluation':
            type = 'e'
        elif mode == 'training':
            type = 't'
        else:
            raise error.Error('Invalid mode {}: must be "training" or "evaluation"', mode)
        self.stats_recorder.type = type

    def _before_step(self, action) -> None:
        """
        Method called before each action-step

        :param action: the action
        :return: None
        """
        if not self.enabled: return
        self.stats_recorder.before_step(action)

    def _after_step(self, observation: np.ndarray, reward: float, done: bool, info: dict) -> bool:
        """
        Method called after each step

        :param observation: the observation from the env
        :param reward: the reward
        :param done: whether the episode is done or not
        :param info: the info from the env
        :return: done
        """
        if not self.enabled: return done

        if done and self.env_semantics_autoreset:
            # For envs with BlockingReset wrapping VNCEnv, this observation will be the first one of the new episode
            self.reset_video_recorder()
            self.episode_id += 1
            self._flush()

        # Record stats
        self.stats_recorder.after_step(observation, reward, done, info)
        # Record video
        frames = self.video_recorder.capture_frame()
        if frames is not None:
            for frame in frames:
                self.episode_frames.append(frame)
        return done

    def generate_gif(self, path, fps = 55) -> None:
        """
        Utility method for generating gifs

        :param path: the path to save the gifs
        :param fps: the fps to use for generation
        :return: None
        """
        if (self.episode_frames is not None and len(self.episode_frames) > 0
                and (self.episode_id-1) % (self.video_frequency) == 0):
            imageio.mimsave(path, self.episode_frames, fps=fps)
        if self.openai_baseline:
            self.episode_frames = []
            self.openai_baseline_reset = True

    def _before_reset(self) -> None:
        """
        Method called before the reset of the environment

        :return: None
        """
        if not self.enabled: return
        self.stats_recorder.before_reset()

    def _after_reset(self, observation) -> None:
        """
        Method called after the reset of the environment

        :param observation: the observation from the reset of the env
        :return: None
        """
        if not self.enabled: return

        # Reset the stat count
        self.stats_recorder.after_reset(observation)

        self.reset_video_recorder()
        self.episode_frames = []

        # Record video
        if ((self.episode_id-1) % (self.video_frequency) == 0):
            frames = self.video_recorder.capture_frame()
            if frames is not None:
                for frame in frames:
                    self.episode_frames.append(frame)

        # Bump *after* all reset activity has finished
        self.episode_id += 1

        self._flush()

    def reset_video_recorder(self) -> None:
        """
        Resets the video recordder

        :return: None
        """
        # Close any existing video recorder
        if self.video_recorder:
            self._close_video_recorder()

        # Start recording the next video.
        #
        # TODO: calculate a more correct 'episode_id' upon merge
        self.video_recorder = CSLECTFVideoRecorder(
            env=self.env,
            base_path=os.path.join(self.directory, '{}.video.{}.video{:06}'.format(self.file_prefix, self.file_infix,
                                                                                   self.episode_id)),
            metadata={'episode_id': self.episode_id},
            enabled=True
            #enabled=self._video_enabled(),
        )
        frames = self.video_recorder.capture_frame()
        if frames is not None:
            for frame in frames:
                self.episode_frames.append(frame)

    def _close_video_recorder(self) -> None:
        """
        Closes the video recorder

        :return: None
        """
        self.video_recorder.close()
        if self.video_recorder.functional:
            self.videos.append((self.video_recorder.path, self.video_recorder.metadata_path))

    def _video_enabled(self) -> bool:
        """
        Checks whether video is enabled or not

        :return: True or False
        """
        return self.video_callable(self.episode_id)

    def _env_info(self) -> dict:
        """
        :return: environment information
        """
        env_info = {
            'gym_version': version.VERSION,
        }
        if self.env.spec:
            env_info['env_id'] = self.env.spec.id
        return env_info

    def __del__(self) -> None:
        """
        Deletes the object
        :return: None
        """
        # Make sure we've closed up shop when garbage collecting
        self.close()

    def get_total_steps(self) -> int:
        """
        :return: number of steps in the environment
        """
        return self.stats_recorder.total_steps

    def get_episode_rewards(self) -> float:
        """
        :return: rewards in the environment
        """
        return self.stats_recorder.episode_rewards

    def get_episode_lengths(self) -> int:
        """
        :return: length of the episodes
        """
        return self.stats_recorder.episode_lengths

    def periodic_video_schedule(self, episode_id) -> bool:
        """
        Checkes whether video should be recorded this episode or not

        :param episode_id: the episode id to check
        :return: True or False
        """
        if episode_id % self.video_frequency == 0:
            return True
        else:
            return False


def detect_training_manifests(training_dir, files=None) -> List[str]:
    """
    Utility method for detecting training manifests

    :param training_dir: the training directory
    :param files: the files in the training directory
    :return: The list of files
    """
    if files is None:
        files = os.listdir(training_dir)
    return [os.path.join(training_dir, f) for f in files if f.startswith(MANIFEST_PREFIX + '.')]


def detect_monitor_files(training_dir) -> List[str]:
    """
    Utility method for detecting monitoring files

    :param training_dir: the training directory
    :return: List of monitoring files
    """
    return [os.path.join(training_dir, f) for f in os.listdir(training_dir) if f.startswith(FILE_PREFIX + '.')]


def clear_monitor_files(training_dir) -> None:
    """
    Clears the monitoring files

    :param training_dir: the directory where the files are stored
    :return: None
    """
    files = detect_monitor_files(training_dir)
    if len(files) == 0:
        return

    logger.info('Clearing %d monitor files from previous run (because force=True was provided)', len(files))
    for file in files:
        os.unlink(file)


def capped_cubic_video_schedule(episode_id) -> bool:
    """
    Utility function to check if the capped cubic schedule matches this episode

    :param episode_id: the episode id to check
    :return: True or False
    """
    if episode_id < 1000:
        return int(round(episode_id ** (1. / 3))) ** 3 == episode_id
    else:
        return episode_id % 1000 == 0


def disable_videos(episode_id) -> bool:
    """
    Utility function for disabling videos

    :param episode_id:  the episode id
    :return: False
    """
    return False

monitor_closer = closer.Closer()

# This method gets used for a sanity check in scoreboard/api.py. It's
# not intended for use outside of the gym codebase.
def _open_monitors():
    """
    Opens the monitors
    :return: list of monitors
    """
    return list(monitor_closer.closeables.values())

def load_env_info_from_manifests(manifests, training_dir) -> dict:
    """
    Loads the environment info from a list of manifests

    :param manifests: the manifests
    :param training_dir: the training directory
    :return: the environment info
    """
    env_infos = []
    for manifest in manifests:
        with open(manifest) as f:
            contents = json.load(f)
            env_infos.append(contents['env_info'])

    env_info = collapse_env_infos(env_infos, training_dir)
    return env_info


def load_results(training_dir):
    """
    Loads results from a training directory

    :param training_dir: the training directory
    :return: None
    """
    if not os.path.exists(training_dir):
        logger.error('Training directory %s not found', training_dir)
        return

    manifests = detect_training_manifests(training_dir)
    if not manifests:
        logger.error('No manifests found in training directory %s', training_dir)
        return

    logger.debug('Uploading data from manifest %s', ', '.join(manifests))

    # Load up stats + video files
    stats_files = []
    videos = []
    env_infos = []

    for manifest in manifests:
        with open(manifest) as f:
            contents = json.load(f)
            # Make these paths absolute again
            stats_files.append(os.path.join(training_dir, contents['stats']))
            videos += [(os.path.join(training_dir, v), os.path.join(training_dir, m))
                       for v, m in contents['videos']]
            env_infos.append(contents['env_info'])

    env_info = collapse_env_infos(env_infos, training_dir)
    data_sources, initial_reset_timestamps, timestamps, episode_lengths, episode_rewards, episode_types, \
    initial_reset_timestamp = merge_stats_files(stats_files)

    return {
        'manifests': manifests,
        'env_info': env_info,
        'data_sources': data_sources,
        'timestamps': timestamps,
        'episode_lengths': episode_lengths,
        'episode_rewards': episode_rewards,
        'episode_types': episode_types,
        'initial_reset_timestamps': initial_reset_timestamps,
        'initial_reset_timestamp': initial_reset_timestamp,
        'videos': videos,
    }


def merge_stats_files(stats_files):
    """
    Merges statistics files

    :param stats_files: the statistics files
    :return: the merged files
    """
    timestamps = []
    episode_lengths = []
    episode_rewards = []
    episode_types = []
    initial_reset_timestamps = []
    data_sources = []

    for i, path in enumerate(stats_files):
        with open(path) as f:
            content = json.load(f)
            # so empty file doesn't mess up results, due to null initial_reset_timestamp
            if len(content['timestamps'])==0: continue
            data_sources += [i] * len(content['timestamps'])
            timestamps += content['timestamps']
            episode_lengths += content['episode_lengths']
            episode_rewards += content['episode_rewards']
            # Recent addition
            episode_types += content.get('episode_types', [])
            # Keep track of where each episode came from.
            initial_reset_timestamps.append(content['initial_reset_timestamp'])

    idxs = np.argsort(timestamps)
    timestamps = np.array(timestamps)[idxs].tolist()
    episode_lengths = np.array(episode_lengths)[idxs].tolist()
    episode_rewards = np.array(episode_rewards)[idxs].tolist()
    data_sources = np.array(data_sources)[idxs].tolist()

    if episode_types:
        episode_types = np.array(episode_types)[idxs].tolist()
    else:
        episode_types = None

    if len(initial_reset_timestamps) > 0:
        initial_reset_timestamp = min(initial_reset_timestamps)
    else:
        initial_reset_timestamp = 0

    return data_sources, initial_reset_timestamps, timestamps, episode_lengths, episode_rewards, episode_types, \
           initial_reset_timestamp


# TODO training_dir isn't used except for error messages, clean up the layering
def collapse_env_infos(env_infos, training_dir):
    """
    Collapses environment informations into one

    :param env_infos: the list of environment infos
    :param training_dir: the training directory
    :return: the collapsed environment info
    """
    assert len(env_infos) > 0

    first = env_infos[0]
    for other in env_infos[1:]:
        if first != other:
            raise error.Error('Found two unequal env_infos: {} and {}. This usually indicates that your training '
                              'directory {} has commingled results from multiple runs.'.format(first, other, training_dir))

    for key in ['env_id', 'gym_version']:
        if key not in first:
            raise error.Error("env_info {} from training directory {} is missing expected key {}. "
                              "This is unexpected and likely indicates a bug in gym.".format(first, training_dir, key))
    return first
