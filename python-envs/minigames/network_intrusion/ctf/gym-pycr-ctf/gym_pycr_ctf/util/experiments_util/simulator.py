"""
A utility class for running simulations of pre-defined policies against each other (No training involved)
"""
import logging
import time
import numpy as np
from pycr_common.agents.bots.ppo_attacker_bot_agent import PPOAttackerBotAgent
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.dao.experiment.experiment_result import ExperimentResult
from gym_pycr_ctf.dao.experiment.simulation_config import SimulationConfig
from gym_pycr_ctf.rendering.video.pycr_ctf_monitor import PyCrCTFMonitor


class Simulator:

    """
    A class to orchestrate simulations of pre-defined policies against each other
    """

    def __init__(self, env: PyCRCTFEnv, config: SimulationConfig, attacker: PPOAttackerBotAgent):
        """
        Class constructor, initializes the class with a given environment and simulation config

        :param env: the openAIGym environment for the simulation
        :param config: the simulation configuration
        """
        self.config = config
        self.env = env
        self.experiment_result = ExperimentResult()
        if self.config.logger is None:
            self.config.logger = logging.getLogger('Simulation')
        self.attacker = attacker

    def simulate(self) -> ExperimentResult:
        """
        Runs a simulation using the defined config and environment

        :return: the simulation result
        """
        self.config.logger.info("Starting Simulation")
        time_str = str(time.time())

        if len(self.experiment_result.avg_episode_steps) > 0:
            self.config.logger.warning("starting simulation with a non-empty result object")
        if self.config.num_episodes < 1:
            return
        done = False

        # Video config
        if self.config.video:
            if self.config.video_dir is None:
                raise AssertionError("Video is set to True but no video_dir is provided, please specify "
                                     "the video_dir argument")
            self.env = PyCrCTFMonitor(self.env, self.config.video_dir + "/" + time_str, force=True,
                                      video_frequency=self.config.video_frequency)
            self.env.metadata["video.frames_per_second"] = self.config.video_fps

        # Tracking metrics
        episode_steps = []

        # Simulate
        obs = self.env.reset()
        for episode in range(self.config.num_episodes):
            i = 0
            episode_step = 0
            while not done:
                if self.config.render:
                    self.env.render()
                    time.sleep(self.config.sleep)
                i = i + 1
                action = self.attacker.action(self.env.env_state)
                obs, _, done, _ = self.env.step(action)
                episode_step += 1
            if self.config.render:
                self.env.render()
                time.sleep(self.config.sleep)

            self.config.logger.info("Simulation episode: {}, Game ended after {} steps".format(episode, i))
            episode_steps.append(episode_step)

            # Log average metrics every <self.config.eval_log_frequency> episodes
            if episode > 0 and episode % self.config.log_frequency == 0:
                self.log_metrics(self.experiment_result, episode_steps)
                episode_steps = []
                if self.config.gifs and self.config.video:
                    self.env.generate_gif(self.config.gif_dir + "episode_" + str(episode) + "_"
                                          + time_str + ".gif", self.config.video_fps)

            done = False
            obs = self.env.reset()

        self.env.close()
        self.config.logger.info("Simulation Complete")
        return self.experiment_result

    def log_metrics(self, result: ExperimentResult, episode_steps: list) -> None:
        """
        Logs average metrics for the last <self.config.log_frequency> episodes

        :param result: the result object to add the results to
        :param episode_steps: list of episode steps for the last <self.config.log_frequency> episodes
        :return: None
        """
        avg_episode_steps = np.mean(episode_steps)
        log_str = "avg_t:{:.2f}".format(avg_episode_steps)
        self.config.logger.info(log_str)
        result.avg_episode_steps.append(avg_episode_steps)
