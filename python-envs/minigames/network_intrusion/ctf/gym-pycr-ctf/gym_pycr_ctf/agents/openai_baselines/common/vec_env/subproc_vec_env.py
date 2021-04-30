import multiprocessing
from collections import OrderedDict
from typing import Sequence
import pickle
import gym
import numpy as np
import time
from gym_pycr_ctf.agents.openai_baselines.common.vec_env.base_vec_env import CloudpickleWrapper, VecEnv
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
import gym_pycr_ctf.constants.constants as constants

def _worker(remote, parent_remote, env_fn_wrapper):
    parent_remote.close()
    env = env_fn_wrapper.var()
    while True:
        try:
            cmd, data = remote.recv()
            if cmd == "step":
                observation, reward, done, info = env.step(data)
                attacker_actions = list(range(env.attacker_num_actions))
                defender_actions = list(range(env.defender_num_actions))
                if done:
                    # save final observation where user can get it, then reset
                    info["terminal_observation"] = observation
                    observation = env.reset()
                attacker_non_legal_actions = list(filter(lambda action: not PyCRCTFEnv.is_attack_action_legal(
                    action, env_config=env.env_config, env_state=env.env_state), attacker_actions))
                defender_non_legal_actions = list(filter(lambda action: not PyCRCTFEnv.is_defense_action_legal(
                    action, env_config=env.env_config, env_state=env.env_state), defender_actions))
                info["attacker_non_legal_actions"] = attacker_non_legal_actions
                info["defender_non_legal_actions"] = defender_non_legal_actions
                info["idx"] = env.idx
                remote.send((observation, reward, done, info))
            elif cmd == "seed":
                remote.send(env.seed(data))
            elif cmd == "reset":
                observation = env.reset()
                remote.send(observation)
            elif cmd == "render":
                remote.send(env.render(data))
            elif cmd == "close":
                env.close()
                remote.close()
                break
            elif cmd == "cleanup":
                env.cleanup()
                remote.send(1)
            elif cmd == "get_attacker_spaces":
                remote.send((env.attacker_observation_space, env.attacker_action_space))
            elif cmd == "get_defender_spaces":
                remote.send((env.defender_observation_space, env.defender_action_space))
            elif cmd == "attacker_initial_illegal_actions":
                remote.send(env.attacker_initial_illegal_actions)
            elif cmd == "defender_initial_illegal_actions":
                remote.send(env.defender_initial_illegal_actions)
            elif cmd == "network_conf":
                env.env_config.network_conf.defender_dynamics_model = None
                remote.send(env.env_config.network_conf)
            elif cmd == "pi_star_rew_attacker":
                id = env.idx
                if env.env_config.emulation_config is not None:
                    id = env.env_config.emulation_config.agent_ip
                # elif env.env_config.network_conf.hacker is not None:
                #     id = env.env_config.network_conf.hacker.ip
                remote.send((id, env.env_config.pi_star_rew_attacker, env.env_config.pi_star_rew_list_attacker))
                #env.env.env_config.pi_star_rew_list = [env.env.env_config.pi_star_rew]
            elif cmd == "set_randomization_space":
                env.randomization_space = data
                env.env.randomization_space = data
            elif cmd == "reset_pi_star_rew_attacker":
                env.env.env_config.pi_star_rew_list_attacker = [env.env.env_config.pi_star_rew_attacker]
            elif cmd == "set_domain_randomization_eval_env":
                env.env.env_config.domain_randomization = data
            elif cmd == "env_method":
                method = getattr(env, data[0])
                remote.send(method(*data[1], **data[2]))
            elif cmd == "get_attr":
                remote.send(getattr(env, data))
            elif cmd == "set_attr":
                remote.send(setattr(env, data[0], data[1]))
            elif cmd == "set_randomize_starting_state":
                env.env.env_config.randomize_attacker_starting_state = data
            elif cmd == "set_snort_baseline_simulate":
                env.env.env_config.snort_baseline_simulate = data
            elif cmd == "get_randomize_starting_state":
                remote.send(env.env.env_config.randomize_attacker_starting_state)
            elif cmd == "get_snort_baseline_simulate":
                remote.send(env.env.env_config.snort_baseline_simulate)
            elif cmd == "get_num_detections":
                remote.send(env.env.attacker_agent_state.num_detections)
            elif cmd == "get_all_flags":
                remote.send(env.env.attacker_agent_state.num_all_flags)
            else:
                raise NotImplementedError(f"`{cmd}` is not implemented in the worker")
        except EOFError:
            break


class SubprocVecEnv(VecEnv):
    """
    Creates a multiprocess vectorized wrapper for multiple environments, distributing each environment to its own
    process, allowing significant speed up when the environment is computationally complex.

    For performance reasons, if your environment is not IO bound, the number of environments should not exceed the
    number of logical cores on your CPU.

    .. warning::

        Only 'forkserver' and 'spawn' start methods are thread-safe,
        which is important when TensorFlow sessions or other non thread-safe
        libraries are used in the parent (see issue #217). However, compared to
        'fork' they incur a small start-up cost and have restrictions on
        global variables. With those methods, users must wrap the code in an
        ``if __name__ == "__main__":`` block.
        For more information, see the multiprocessing documentation.

    :param env_fns: ([Gym Environment]) Environments to run in subprocesses
    :param start_method: (str) method used to start the subprocesses.
           Must be one of the methods returned by multiprocessing.get_all_start_methods().
           Defaults to 'forkserver' on available platforms, and 'spawn' otherwise.
    """

    def __init__(self, env_fns, start_method=None, env_config = None):
        self.waiting = False
        self.closed = False
        self.env_config = None
        n_envs = len(env_fns)


        if start_method is None:
            # Fork is not a thread safe method (see issue #217)
            # but is more user friendly (does not require to wrap the code in
            # a `if __name__ == "__main__":`)
            forkserver_available = "forkserver" in multiprocessing.get_all_start_methods()
            start_method = "forkserver" if forkserver_available else "spawn"
        ctx = multiprocessing.get_context(start_method)

        self.remotes, self.work_remotes = zip(*[ctx.Pipe() for _ in range(n_envs)])
        self.processes = []
        for work_remote, remote, env_fn in zip(self.work_remotes, self.remotes, env_fns):
            print("sleeping")
            time.sleep(constants.SUB_PROC_ENV.SLEEP_TIME_STARTUP)
            print("sleep finished")
            args = (work_remote, remote, CloudpickleWrapper(env_fn))
            # daemon=True: if the main process crashes, we should not cause things to hang
            process = ctx.Process(target=_worker, args=args, daemon=True)  # pytype:disable=attribute-error
            process.start()
            self.processes.append(process)
            work_remote.close()

        self.remotes[0].send(("get_attacker_spaces", None))
        attacker_observation_space, attacker_action_space = self.remotes[0].recv()

        self.remotes[0].send(("get_defender_spaces", None))
        defender_observation_space, defender_action_space = self.remotes[0].recv()

        self.remotes[0].send(("attacker_initial_illegal_actions", None))
        attacker_initial_illegal_actions = self.remotes[0].recv()
        self.attacker_initial_illegal_actions = attacker_initial_illegal_actions

        self.remotes[0].send(("defender_initial_illegal_actions", None))
        defender_initial_illegal_actions = self.remotes[0].recv()
        self.defender_initial_illegal_actions = defender_initial_illegal_actions

        self.get_network_confs()
        VecEnv.__init__(self, len(env_fns), attacker_observation_space, attacker_action_space,
                        defender_observation_space, defender_action_space)

    def step_async(self, actions):
        for remote, action in zip(self.remotes, actions):
            remote.send(("step", action))
        self.waiting = True

    def step_wait(self):
        results = [remote.recv() for remote in self.remotes]
        self.waiting = False
        obs, rews, dones, infos = zip(*results)
        if isinstance(obs, tuple) and isinstance(obs[0], tuple):
            attacker_obs = []
            defender_obs = []
            for i in range(len(obs)):
                attacker_obs.append(obs[i][0])
                defender_obs.append(obs[i][1])
            attacker_obs = np.array(attacker_obs)
            defender_obs = np.array(defender_obs)
            attacker_obs = attacker_obs.astype("float64")
            defender_obs = defender_obs.astype("float64")
            obs = (attacker_obs, defender_obs)
        return obs, np.stack(rews), np.stack(dones), infos

    def seed(self, seed=None):
        for idx, remote in enumerate(self.remotes):
            remote.send(("seed", seed + idx))
        return [remote.recv() for remote in self.remotes]

    def reset(self):
        for remote in self.remotes:
            remote.send(("reset", None))
        obs = [remote.recv() for remote in self.remotes]
        return obs

    def eval_reset(self, idx : int):
        self.remotes[idx].send(("reset", None))
        obs = self.remotes[idx].recv()
        obs = [obs]
        return obs

    def get_network_confs(self):
        network_confs = []
        for remote in self.remotes:
            remote.send(("network_conf", "test"))
        for remote in self.remotes:
            network_confs.append(remote.recv())
        self.network_confs = network_confs
        return self.network_confs

    def get_pi_star_rew_attacker(self):
        pi_star_rews_attacker = []
        for remote in self.remotes:
            remote.send(("pi_star_rew_attacker", None))
        for remote in self.remotes:
            pi_star_rews_attacker.append(remote.recv())
        self.pi_star_rews_attacker = pi_star_rews_attacker
        return self.pi_star_rews_attacker

    def get_randomize_starting_state(self):
        randomize_starting_states = []
        for remote in self.remotes:
            remote.send(("get_randomize_starting_state", None))
        for remote in self.remotes:
            randomize_starting_states.append(remote.recv())
        self.randomize_starting_states = randomize_starting_states
        return self.randomize_starting_states

    def get_snort_baseline_simulate(self):
        snort_baseline_simulates = []
        for remote in self.remotes:
            remote.send(("get_snort_baseline_simulate", None))
        for remote in self.remotes:
            snort_baseline_simulates.append(remote.recv())
        self.snort_baseline_simulates = snort_baseline_simulates
        return self.snort_baseline_simulates

    def get_num_detections(self):
        num_detections = 0
        for remote in self.remotes:
            remote.send(("get_num_detections", None))
        for remote in self.remotes:
            num_detections += remote.recv()
        self.num_detections = num_detections
        return self.num_detections

    def get_num_all_flags(self):
        num_all_flags = 0
        for remote in self.remotes:
            remote.send(("get_all_flags", None))
        for remote in self.remotes:
            num_all_flags += remote.recv()
        self.num_all_flags = num_all_flags
        return self.num_all_flags

    def set_randomization_space(self, randomization_space):
        for remote in self.remotes:
            remote.send(("set_randomization_space", randomization_space))


    def set_randomize_starting_state(self, randomize_starting_state):
        for remote in self.remotes:
            remote.send(("set_randomize_starting_state", randomize_starting_state))

    def set_snort_baseline_simulate(self, snort_baseline_simulate):
        for remote in self.remotes:
            remote.send(("set_snort_baseline_simulate", snort_baseline_simulate))

    def reset_pi_star_rew_attacker(self):
        for remote in self.remotes:
            remote.send(("reset_pi_star_rew_attacker", None))

    def set_domain_randomization(self, domain_randomization):
        for remote in self.remotes:
            remote.send(("set_domain_randomization_eval_env", domain_randomization))

    def eval_step(self, action, idx: int):
        self.remotes[idx].send(("step", action))
        result = self.remotes[idx].recv()
        obs, rews, dones, infos = result
        return [obs], rews, dones, infos

    def close(self):
        if self.closed:
            return
        if self.waiting:
            for remote in self.remotes:
                remote.recv()
        for remote in self.remotes:
            remote.send(("close", None))
        for process in self.processes:
            process.join()
        self.closed = True

    def cleanup(self):
        for remote in self.remotes:
            remote.send(("cleanup", None))
        res = [remote.recv() for remote in self.remotes]
        return res

    def get_images(self) -> Sequence[np.ndarray]:
        for pipe in self.remotes:
            # gather images from subprocesses
            # `mode` will be taken into account later
            pipe.send(("render", "rgb_array"))
        imgs = [pipe.recv() for pipe in self.remotes]
        return imgs

    def get_attr(self, attr_name, indices=None):
        """Return attribute from vectorized environment (see base class)."""
        target_remotes = self._get_target_remotes(indices)
        for remote in target_remotes:
            remote.send(("get_attr", attr_name))
        return [remote.recv() for remote in target_remotes]

    def set_attr(self, attr_name, value, indices=None):
        """Set attribute inside vectorized environments (see base class)."""
        target_remotes = self._get_target_remotes(indices)
        for remote in target_remotes:
            remote.send(("set_attr", (attr_name, value)))
        for remote in target_remotes:
            remote.recv()

    def env_method(self, method_name, *method_args, indices=None, **method_kwargs):
        """Call instance methods of vectorized environments."""
        target_remotes = self._get_target_remotes(indices)
        for remote in target_remotes:
            remote.send(("env_method", (method_name, method_args, method_kwargs)))
        return [remote.recv() for remote in target_remotes]

    def _get_target_remotes(self, indices):
        """
        Get the connection object needed to communicate with the wanted
        envs that are in subprocesses.

        :param indices: (None,int,Iterable) refers to indices of envs.
        :return: ([multiprocessing.Connection]) Connection object to communicate between processes.
        """
        indices = self._get_indices(indices)
        return [self.remotes[i] for i in indices]


def _flatten_obs(obs, space):
    """
    Flatten observations, depending on the observation space.

    :param obs: (list<X> or tuple<X> where X is dict<ndarray>, tuple<ndarray> or ndarray) observations.
                A list or tuple of observations, one per environment.
                Each environment observation may be a NumPy array, or a dict or tuple of NumPy arrays.
    :return (OrderedDict<ndarray>, tuple<ndarray> or ndarray) flattened observations.
            A flattened NumPy array or an OrderedDict or tuple of flattened numpy arrays.
            Each NumPy array has the environment index as its first axis.
    """
    assert isinstance(obs, (list, tuple)), "expected list or tuple of observations per environment"
    assert len(obs) > 0, "need observations from at least one environment"

    if isinstance(space, gym.spaces.Dict):
        assert isinstance(space.spaces, OrderedDict), "Dict space must have ordered subspaces"
        assert isinstance(obs[0], dict), "non-dict observation for environment with Dict observation space"
        return OrderedDict([(k, np.stack([o[k] for o in obs])) for k in space.spaces.keys()])
    elif isinstance(space, gym.spaces.Tuple):
        assert isinstance(obs[0], tuple), "non-tuple observation for environment with Tuple observation space"
        obs_len = len(space.spaces)
        return tuple((np.stack([o[i] for o in obs]) for i in range(obs_len)))
    else:
        return np.stack(obs)