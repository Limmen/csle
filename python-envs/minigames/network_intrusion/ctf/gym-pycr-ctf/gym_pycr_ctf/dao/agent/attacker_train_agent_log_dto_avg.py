import numpy as np
import time
import pycr_common.envs_model.logic.common.util as pycr_util
from pycr_common import AgentConfig
from pycr_common import SubprocVecEnv
from pycr_common import BaseAttackerTrainAgentLogDTOAvg
from gym_pycr_ctf.dao.agent.tensorboard_data_dto import TensorboardDataDTO


class AttackerTrainAgentLogDTOAvg(BaseAttackerTrainAgentLogDTOAvg):
    """
    DTO with average metrics of the attacker for logging during training
    """

    def __init__(self, train_log_dto : "TrainAgentLogDTO", attacker_agent_config : AgentConfig = None,
                 env=None, env_2 = None, eval: bool = False):
        """
        Class constructor: Initializes the DTO with metrics

        :param train_log_dto: the DTO to use to intialize this dto with
        :param attacker_agent_config: the attacker agent configuration
        :param env: the environment
        :param env_2: the evaluation environment
        :param eval: boolean flag whether it is an evaluation or not
        """
        super(AttackerTrainAgentLogDTOAvg, self).__init__()
        if not eval:
            self.result = train_log_dto.train_result
        else:
            self.result = train_log_dto.eval_result
        self.train_log_dto = train_log_dto
        self.attacker_agent_config = attacker_agent_config
        self.env = env
        self.env_2 = env_2

        self.attacker_train_env_specific_regret = {}
        self.attacker_eval_env_specific_regret = {}
        self.attacker_eval_2_env_specific_regret = {}
        self.attacker_train_env_specific_opt_frac = {}
        self.attacker_eval_env_specific_opt_frac = {}
        self.attacker_eval_2_env_specific_opt_frac = {}

        self.attacker_training_time = time.time() - self.train_log_dto.start_time
        self.attacker_training_time_hours = self.attacker_training_time / 3600
        self.attacker_avg_episode_rewards = np.mean(self.train_log_dto.attacker_episode_rewards)
        self.attacker_avg_episode_flags = np.mean(self.train_log_dto.episode_flags)
        self.attacker_avg_episode_flags_percentage = np.mean(self.train_log_dto.episode_flags_percentage)
        self.attacker_avg_episode_steps = np.mean(self.train_log_dto.episode_steps)
        self.attacker_avg_episode_costs = np.mean(self.train_log_dto.attacker_action_costs)
        self.attacker_avg_episode_costs_norm = np.mean(self.train_log_dto.attacker_action_costs_norm)
        self.attacker_avg_episode_alerts = np.mean(self.train_log_dto.attacker_action_alerts)
        self.attacker_avg_episode_alerts_norm = np.mean(self.train_log_dto.attacker_action_alerts_norm)
        if self.train_log_dto.episode_caught is not None and self.train_log_dto.episode_early_stopped is not None \
                and self.train_log_dto.episode_successful_intrusion is not None:
            self.attacker_total_c_s_i = sum(list(map(lambda x: int(x), self.train_log_dto.episode_caught))) \
                                        + sum(list(map(lambda x: int(x), self.train_log_dto.episode_early_stopped))) \
                                        + sum(list(map(lambda x: int(x), self.train_log_dto.episode_successful_intrusion)))
        else:
            self.attacker_total_c_s_i = 1
        if self.train_log_dto.eval_episode_caught is not None and self.train_log_dto.eval_episode_early_stopped is not None \
                and self.train_log_dto.eval_episode_successful_intrusion is not None:
            self.attacker_eval_total_c_s_i = sum(list(map(lambda x: int(x), self.train_log_dto.eval_episode_caught))) \
                                             + sum(list(map(lambda x: int(x), self.train_log_dto.eval_episode_early_stopped))) \
                                             + sum(list(map(lambda x: int(x), self.train_log_dto.eval_episode_successful_intrusion)))
        else:
            self.attacker_eval_total_c_s_i = 1
        if self.train_log_dto.eval_2_episode_caught is not None and self.train_log_dto.eval_2_episode_early_stopped is not None \
                and self.train_log_dto.eval_2_episode_successful_intrusion is not None:
            self.eval_2_total_c_s_i = sum(list(map(lambda x: int(x), self.train_log_dto.eval_2_episode_caught))) \
                                 + sum(list(map(lambda x: int(x), self.train_log_dto.eval_2_episode_early_stopped))) \
                                 + sum(list(map(lambda x: int(x), self.train_log_dto.eval_2_episode_successful_intrusion)))
        else:
            self.eval_2_total_c_s_i = 1
        if self.train_log_dto.episode_caught is not None:
            self.attacker_episode_caught_frac = sum(list(map(lambda x: int(x), self.train_log_dto.episode_caught))) / max(1, self.attacker_total_c_s_i)
        else:
            self.attacker_episode_caught_frac = 0

        if self.train_log_dto.episode_early_stopped is not None:
            self.attacker_episode_early_stopped_frac = sum(list(map(lambda x: int(x),
                                                                    self.train_log_dto.episode_early_stopped))) / max(1, self.attacker_total_c_s_i)
        else:
            self.attacker_episode_early_stopped_frac = 0

        if self.train_log_dto.episode_successful_intrusion is not None:
            self.attacker_episode_successful_intrusion_frac = sum(list(map(lambda x: int(x),
                                                                           self.train_log_dto.episode_successful_intrusion))) / max(1,
                                                                                                                 self.attacker_total_c_s_i)
        else:
            self.attacker_episode_successful_intrusion_frac = 0

        if self.train_log_dto.eval_episode_caught is not None:
            self.attacker_eval_episode_caught_frac = sum(list(map(lambda x: int(x),
                                                                  self.train_log_dto.eval_episode_caught))) / max(1, self.attacker_eval_total_c_s_i)
        else:
            self.attacker_eval_episode_caught_frac = 0

        if self.train_log_dto.eval_episode_successful_intrusion is not None:
            self.attacker_eval_episode_successful_intrusion_frac = sum(
                list(map(lambda x: int(x), self.train_log_dto.eval_episode_successful_intrusion))) / max(
                1, self.attacker_eval_total_c_s_i)
        else:
            self.attacker_eval_episode_successful_intrusion_frac = 0

        if self.train_log_dto.eval_episode_early_stopped is not None:
            self.attacker_eval_episode_early_stopped_frac = sum(
                list(map(lambda x: int(x), self.train_log_dto.eval_episode_early_stopped))) / max(1, self.attacker_eval_total_c_s_i)
        else:
            self.attacker_eval_episode_early_stopped_frac = 0

        if self.train_log_dto.eval_2_episode_caught is not None:
            self.attacker_eval_2_episode_caught_frac = sum(
                list(map(lambda x: int(x), self.train_log_dto.eval_2_episode_caught))) / max(1, self.eval_2_total_c_s_i)
        else:
            self.attacker_eval_2_episode_caught_frac = 0

        if self.train_log_dto.eval_2_episode_successful_intrusion is not None:
            self.attacker_eval_2_episode_successful_intrusion_frac = sum(
                list(
                    map(lambda x: int(x),
                        self.train_log_dto.eval_2_episode_successful_intrusion))) / max(1, self.eval_2_total_c_s_i)
        else:
            self.attacker_eval_2_episode_successful_intrusion_frac = 0

        if self.train_log_dto.eval_2_episode_early_stopped is not None:
            self.attacker_eval_2_episode_early_stopped_frac = sum(
                list(map(
                    lambda x: int(x),self.train_log_dto.eval_2_episode_early_stopped))) / max(1,  self.eval_2_total_c_s_i)
        else:
            self.attacker_eval_2_episode_early_stopped_frac = 0


        if self.result.attacker_avg_episode_rewards is not None:
            self.attacker_rolling_avg_rewards = pycr_util.running_average(
                self.result.attacker_avg_episode_rewards + [self.attacker_avg_episode_rewards], self.attacker_agent_config.running_avg)
        else:
            self.attacker_rolling_avg_rewards = 0.0

        if self.result.avg_episode_steps is not None:
            self.attacker_rolling_avg_steps = pycr_util.running_average(
                self.result.avg_episode_steps + [self.attacker_avg_episode_steps], self.attacker_agent_config.running_avg)
        else:
            self.attacker_rolling_avg_steps = 0.0

        if self.train_log_dto.attacker_lr is None:
            self.attacker_lr = 0.0
        else:
            self.attacker_lr = self.train_log_dto.attacker_lr
        if not eval and self.train_log_dto.attacker_episode_avg_loss is not None:
            self.attacker_avg_episode_loss = np.mean(self.train_log_dto.attacker_episode_avg_loss)
        else:
            self.attacker_avg_episode_loss = 0.0

        if not eval and self.train_log_dto.attacker_eval_episode_rewards is not None:
            self.attacker_eval_avg_episode_rewards = np.mean(self.train_log_dto.attacker_eval_episode_rewards)
        else:
            self.attacker_eval_avg_episode_rewards = 0.0

        if not eval and self.train_log_dto.attacker_eval_2_episode_rewards is not None:
            self.attacker_eval_2_avg_episode_rewards = np.mean(self.train_log_dto.attacker_eval_2_episode_rewards)
        else:
            self.attacker_eval_2_avg_episode_rewards = 0.0

        if self.attacker_agent_config.log_regret:
            if self.env.env_config is not None:
                if len(self.env.envs[0].env_config.pi_star_rew_list_attacker) >= len(
                        self.train_log_dto.attacker_eval_episode_rewards):
                    pi_star_rews_attacker = self.env.envs[0].env_config.pi_star_rew_list_attacker[
                                            -len(self.train_log_dto.attacker_eval_episode_rewards):]
                    r = [AttackerTrainAgentLogDTOAvg.compute_regret(opt_r=pi_star_rews_attacker[i],
                                                                    r=self.train_log_dto.attacker_eval_episode_rewards[i]) for i in
                         range(len(self.train_log_dto.attacker_eval_episode_rewards))]
                    self.attacker_avg_regret = np.mean(np.array(r))
                else:
                    self.attacker_avg_regret = AttackerTrainAgentLogDTOAvg.compute_regret(r=self.attacker_avg_episode_rewards,
                                                                                          opt_r=self.env.envs[0].env_config.pi_star_rew_attacker)

                if self.train_log_dto.attacker_eval_episode_rewards is not None and self.train_log_dto.attacker_eval_env_specific_rewards != {}:
                    if len(self.env.envs[0].env_config.pi_star_rew_list_attacker) >= len(
                            self.train_log_dto.attacker_eval_episode_rewards):
                        pi_star_rews_attacker = self.env.envs[0].env_config.pi_star_rew_list_attacker[
                                                -len(self.train_log_dto.attacker_eval_episode_rewards):]
                        r = [AttackerTrainAgentLogDTOAvg.compute_regret(opt_r=pi_star_rews_attacker[i],
                                                                        r=self.train_log_dto.attacker_eval_episode_rewards[i])
                             for i in range(len(self.train_log_dto.attacker_eval_episode_rewards))]
                        self.attacker_avg_eval_regret = np.mean(np.array(r))
                    else:
                        self.attacker_avg_eval_regret = AttackerTrainAgentLogDTOAvg.compute_regret(
                            opt_r=self.env.envs[0].env_config.pi_star_rew_attacker,
                            r=self.attacker_eval_avg_episode_rewards)
                else:
                    self.attacker_avg_eval_regret = 0.0

            elif (self.train_log_dto.attacker_train_episode_env_specific_rewards is None
                  or self.train_log_dto.attacker_train_episode_env_specific_rewards == {}) and \
                    (self.train_log_dto.attacker_eval_env_specific_rewards is None
                     or self.train_log_dto.attacker_eval_env_specific_rewards == {}):
                env_regret = self.env.get_pi_star_rew_attacker()[0]
                ip = env_regret[0]

                if len(env_regret[2]) >= len(self.train_log_dto.attacker_episode_rewards):
                    pi_star_rews_attacker = env_regret[2][-len(self.train_log_dto.attacker_episode_rewards):]
                    r = [AttackerTrainAgentLogDTOAvg.compute_regret(
                        opt_r=pi_star_rews_attacker[i], r=self.train_log_dto.attacker_episode_rewards[i]) for i in
                         range(len(self.train_log_dto.attacker_episode_rewards))]
                    self.attacker_avg_regret = np.mean(np.array(r))
                else:
                    self.attacker_avg_regret = AttackerTrainAgentLogDTOAvg.compute_regret(
                        opt_r=env_regret[1], r=self.attacker_avg_episode_rewards)

                if self.train_log_dto.attacker_eval_episode_rewards is not None:
                    if len(env_regret[2]) >= len(self.train_log_dto.attacker_eval_episode_rewards):
                        pi_star_rews_attacker = env_regret[2][-len(self.train_log_dto.attacker_eval_episode_rewards):]
                        r = [AttackerTrainAgentLogDTOAvg.compute_regret(opt_r=pi_star_rews_attacker[i],
                                                                        r=self.train_log_dto.attacker_eval_episode_rewards[i])
                             for i in range(len(self.train_log_dto.attacker_eval_episode_rewards))]
                        self.attacker_avg_eval_regret = np.mean(np.array(r))
                    else:
                        self.attacker_avg_eval_regret = AttackerTrainAgentLogDTOAvg.compute_regret(opt_r=env_regret[1],
                                                                                                   r=self.attacker_eval_avg_episode_rewards)
                else:
                    self.attacker_avg_eval_regret = 0.0
            else:
                regrets = []
                eval_regrets = []
                pi_star_rew_per_env = self.env.get_pi_star_rew_attacker()
                for env_regret in pi_star_rew_per_env:
                    ip = env_regret[0]
                    pi_star_rew = env_regret[1]
                    if self.train_log_dto.attacker_train_episode_env_specific_rewards is not None \
                            and self.train_log_dto.attacker_train_episode_env_specific_rewards != {}:
                        if ip in self.train_log_dto.attacker_train_episode_env_specific_rewards:
                            rewards = self.train_log_dto.attacker_train_episode_env_specific_rewards[ip]
                            if len(env_regret[2]) >= len(rewards):
                                pi_star_rews_attacker = env_regret[2][-len(rewards):]
                                r = [AttackerTrainAgentLogDTOAvg.compute_regret(
                                    opt_r=pi_star_rews_attacker[i], r=rewards[i]) for i in
                                     range(len(rewards))]
                            else:
                                r = [AttackerTrainAgentLogDTOAvg.compute_regret(
                                    opt_r=env_regret[1], r=rewards[i]) for i in
                                     range(len(rewards))]
                            self.attacker_train_env_specific_regret[ip] = r
                            regrets = regrets + r
                    if self.train_log_dto.attacker_eval_env_specific_rewards is not None \
                            and self.train_log_dto.attacker_eval_env_specific_rewards != {}:
                        if ip in self.train_log_dto.attacker_eval_env_specific_rewards:
                            rewards = self.train_log_dto.attacker_eval_env_specific_rewards[ip]
                            if len(env_regret[2]) >= len(rewards):
                                pi_star_rews_attacker = env_regret[2][-len(rewards):]
                                rewards = [np.mean(rewards[i]) for i in range(len(rewards))]
                                r = [AttackerTrainAgentLogDTOAvg.compute_regret(
                                    opt_r=pi_star_rews_attacker[i], r=rewards[i]) for i in
                                     range(len(rewards))]
                            else:
                                rewards = [np.mean(rewards[i]) for i in range(len(rewards))]
                                r = list(map(lambda x: AttackerTrainAgentLogDTOAvg.compute_regret(opt_r=pi_star_rew, r=x),
                                             rewards))
                            self.attacker_eval_env_specific_regret[ip] = r
                            eval_regrets = eval_regrets + r

                self.attacker_avg_regret = np.mean(np.array(regrets))
                self.attacker_avg_eval_regret = np.mean(eval_regrets)

            if env_2 is not None:
                if self.env_2.env_config is not None:
                    if len(self.env_2.envs[0].env_config.pi_star_rew_list_attacker) >= len(
                            self.train_log_dto.attacker_eval_2_episode_rewards):
                        pi_star_rews_attacker = self.env_2.envs[0].env_config.pi_star_rew_list_attacker[
                                                -len(self.train_log_dto.attacker_eval_2_episode_rewards):]
                        r = [AttackerTrainAgentLogDTOAvg.compute_regret(
                            opt_r=pi_star_rews_attacker[i], r=self.train_log_dto.attacker_eval_2_episode_rewards[i])
                             for i in range(len(self.train_log_dto.attacker_eval_2_episode_rewards))]
                        self.attacker_avg_regret_2 = np.mean(np.array(r))

                        of = [AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                            r=self.train_log_dto.attacker_eval_2_episode_rewards[i], opt_r=pi_star_rews_attacker[i])
                              for i in range(len(self.train_log_dto.attacker_eval_2_episode_rewards))]
                        self.attacker_avg_opt_frac_2 = np.mean(np.array(of))
                    else:
                        self.attacker_avg_regret_2 = AttackerTrainAgentLogDTOAvg.compute_regret(
                            opt_r=self.env_2.envs[0].env_config.pi_star_rew_attacker,
                            r=self.attacker_eval_2_avg_episode_rewards)
                        self.attacker_avg_opt_frac_2 = AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                            r=self.attacker_eval_2_avg_episode_rewards,
                            opt_r=self.env_2.envs[0].env_config.pi_star_rew_attacker)
                else:
                    regrets_2 = []
                    pi_star_rew_per_env_2 = self.env_2.get_pi_star_rew_attacker()
                    for env_regret in pi_star_rew_per_env_2:
                        ip = env_regret[0]
                        pi_star_rew = env_regret[1]
                        if self.train_log_dto.attacker_eval_2_env_specific_rewards is not None \
                                and self.train_log_dto.attacker_eval_2_env_specific_rewards != {}:
                            rewards = self.train_log_dto.attacker_eval_2_env_specific_rewards[ip]
                            # print("len ip:{} reg:{}, rews:{}".format(ip, env_regret[2], rewards))
                            # pi_star_rews = env_regret[2][-len(rewards):]
                            rewards = [np.mean(rewards[i]) for i in range(len(rewards))]
                            r = [AttackerTrainAgentLogDTOAvg.compute_regret(opt_r=pi_star_rew, r=rewards[i])
                                 for i in range(len(rewards))]
                            # r = list(map(lambda x: pi_star_rew - x, rewards))
                            self.attacker_eval_2_env_specific_regret[ip] = r
                            regrets_2 = regrets_2 + r
                    if len(regrets_2) == 0:
                        self.attacker_avg_regret_2 = 0.0
                    else:
                        self.attacker_avg_regret_2 = np.mean(np.array(regrets_2))

                    opt_fracs = []
                    for env_pi_star in pi_star_rew_per_env_2:
                        ip = env_pi_star[0]
                        pi_star_rew = env_pi_star[1]
                        if self.train_log_dto.attacker_eval_2_env_specific_rewards is not None \
                                and self.train_log_dto.attacker_eval_2_env_specific_rewards != {}:
                            rewards = self.train_log_dto.attacker_eval_2_env_specific_rewards[ip]
                            rewards = [np.mean(rewards[i]) for i in range(len(rewards))]
                            # pi_star_rews = env_regret[2][-len(rewards):]
                            of = [AttackerTrainAgentLogDTOAvg.compute_opt_frac(r=rewards[i], opt_r=pi_star_rew) for i in
                                  range(len(rewards))]
                            # of = list(map(lambda x: x / pi_star_rew, rewards))
                            self.attacker_eval_2_env_specific_opt_frac[ip] = of
                            opt_fracs = opt_fracs + of
                    if len(opt_fracs) == 0:
                        self.attacker_avg_opt_frac_2 = 0.0
                    else:
                        self.attacker_avg_opt_frac_2 = np.mean(np.array(opt_fracs))
            else:
                self.attacker_avg_regret_2 = 0.0
                self.attacker_avg_opt_frac_2 = 0.0
            if self.env.env_config is not None:

                if len(self.env.envs[0].env_config.pi_star_rew_list_attacker) >= len(
                        self.train_log_dto.attacker_episode_rewards):
                    pi_star_rews_attacker = self.env.envs[0].env_config.pi_star_rew_list_attacker[-len(
                        self.train_log_dto.attacker_episode_rewards):]
                    of = [AttackerTrainAgentLogDTOAvg.compute_opt_frac(r=self.train_log_dto.attacker_episode_rewards[i],
                                                                       opt_r=pi_star_rews_attacker[i]) for i in range(len(
                        self.train_log_dto.attacker_episode_rewards))]
                    self.attacker_avg_opt_frac = np.mean(np.array(of))
                else:
                    self.attacker_avg_opt_frac = AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                        r=self.attacker_avg_episode_rewards,
                        opt_r=self.env.envs[0].env_config.pi_star_rew_attacker)

                if self.train_log_dto.attacker_eval_episode_rewards is not None:
                    if len(self.env.envs[0].env_config.pi_star_rew_list_attacker) >= len(
                            self.train_log_dto.attacker_eval_episode_rewards):
                        pi_star_rews_attacker = self.env.envs[0].env_config.pi_star_rew_list_attacker[
                                                -len(self.train_log_dto.attacker_eval_episode_rewards):]
                        of = [AttackerTrainAgentLogDTOAvg.compute_opt_frac(r=self.train_log_dto.attacker_eval_episode_rewards[i],
                                                                           opt_r=pi_star_rews_attacker[i])
                              for i in range(len(self.train_log_dto.attacker_eval_episode_rewards))]
                        self.attacker_eval_avg_opt_frac = np.mean(np.array(of))
                    else:
                        self.attacker_eval_avg_opt_frac = AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                            r=self.attacker_eval_avg_episode_rewards,
                            opt_r=self.env.envs[0].env_config.pi_star_rew_attacker)
                else:
                    self.attacker_eval_avg_opt_frac = 0.0
            elif (self.train_log_dto.attacker_train_episode_env_specific_rewards is None
                  or self.train_log_dto.attacker_train_episode_env_specific_rewards == {}) and \
                    (self.train_log_dto.attacker_eval_env_specific_rewards is None or
                     self.train_log_dto.attacker_eval_env_specific_rewards == {}):
                env_regret = self.env.get_pi_star_rew_attacker()[0]
                ip = env_regret[0]

                if len(env_regret[2]) >= len(self.train_log_dto.attacker_episode_rewards):
                    pi_star_rews_attacker = env_regret[2][-len(self.train_log_dto.attacker_episode_rewards):]
                    of = [AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                        r=self.train_log_dto.attacker_episode_rewards[i], opt_r=pi_star_rews_attacker[i])
                        for i in range(len(
                        self.train_log_dto.attacker_episode_rewards))]
                    self.attacker_avg_opt_frac = np.mean(np.array(of))
                else:
                    self.attacker_avg_opt_frac = AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                        r=self.attacker_avg_episode_rewards, opt_r=env_regret[1])

                if self.train_log_dto.attacker_eval_episode_rewards is not None:
                    if len(env_regret[2]) >= len(self.attacker_eval_avg_episode_rewards):
                        pi_star_rews_attacker = env_regret[2][-len(self.train_log_dto.attacker_eval_episode_rewards):]
                        of = [AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                            r=self.train_log_dto.attacker_eval_episode_rewards[i], opt_r=pi_star_rews_attacker[i])
                              for i in range(len(self.train_log_dto.attacker_eval_episode_rewards))]
                        self.attacker_eval_avg_opt_frac = np.mean(np.array(of))
                    else:
                        self.attacker_eval_avg_opt_frac = AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                            r=self.attacker_eval_avg_episode_rewards, opt_r=env_regret[1])
                else:
                    self.attacker_eval_avg_opt_frac = 0.0
            else:
                opt_fracs = []
                eval_opt_fracs = []
                pi_star_rew_per_env = self.env.get_pi_star_rew_attacker()
                for env_pi_star in pi_star_rew_per_env:
                    ip = env_pi_star[0]
                    pi_star_rew = env_pi_star[1]
                    if self.train_log_dto.attacker_train_episode_env_specific_rewards is not None \
                            and self.train_log_dto.attacker_train_episode_env_specific_rewards != {}:
                        if ip in self.train_log_dto.attacker_train_episode_env_specific_rewards:
                            rewards = self.train_log_dto.attacker_train_episode_env_specific_rewards[ip]
                            if len(env_pi_star[2]) >= len(rewards):
                                pi_star_rews_attacker = env_pi_star[2][-len(rewards):]
                                of = [AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                                    r=rewards[i], opt_r=pi_star_rews_attacker[i])
                                      for i in range(len(rewards))]
                            else:
                                of = list(map(lambda x: AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                                    r=x, opt_r=pi_star_rew), rewards))
                            self.attacker_train_env_specific_opt_frac[ip] = of
                            opt_fracs = opt_fracs + of
                    elif self.train_log_dto.attacker_eval_env_specific_rewards is not None \
                            and self.train_log_dto.attacker_eval_env_specific_rewards != {}:
                        if ip in self.train_log_dto.attacker_eval_env_specific_rewards:
                            rewards = self.train_log_dto.attacker_eval_env_specific_rewards[ip]
                            if len(env_pi_star[2]) >= len(rewards):
                                pi_star_rews_attacker = env_pi_star[2][-len(rewards):]
                                of = [AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                                    r=rewards[i], opt_r=pi_star_rews_attacker[i])
                                      for i in range(len(rewards))]
                            else:
                                of = list(map(lambda x: AttackerTrainAgentLogDTOAvg.compute_opt_frac(
                                    r=x, opt_r=pi_star_rew), rewards))
                            self.attacker_eval_env_specific_opt_frac[ip] = of
                            eval_opt_fracs = eval_opt_fracs + of
                if len(opt_fracs) == 0:
                    self.attacker_avg_opt_frac = 0.0
                else:
                    self.attacker_avg_opt_frac = np.mean(np.array(opt_fracs))
                if len(eval_opt_fracs) == 0.0:
                    self.attacker_eval_avg_opt_frac = 0.0
                else:
                    self.attacker_eval_avg_opt_frac = np.mean(eval_opt_fracs)
        else:
            self.attacker_avg_regret = 0.0
            self.attacker_avg_eval_regret = 0.0
            self.attacker_avg_eval2_regret = 0.0
            self.attacker_avg_opt_frac = 0.0
            self.attacker_eval_avg_opt_frac = 0.0
            self.attacker_avg_opt_frac_2 = 0.0
            self.attacker_avg_regret_2 = 0.0
            self.attacker_avg_opt_frac_2 = 0.0

        if not eval and self.train_log_dto.eval_episode_flags is not None:
            self.attacker_eval_avg_episode_flags = np.mean(self.train_log_dto.eval_episode_flags)
        else:
            self.attacker_eval_avg_episode_flags = 0.0
        if not eval and self.train_log_dto.eval_episode_flags_percentage is not None:
            self.attacker_eval_avg_episode_flags_percentage = np.mean(self.train_log_dto.eval_episode_flags_percentage)
        else:
            self.attacker_eval_avg_episode_flags_percentage = 0.0
        if not eval and self.train_log_dto.eval_episode_steps is not None:
            self.attacker_eval_avg_episode_steps = np.mean(self.train_log_dto.eval_episode_steps)
        else:
            self.attacker_eval_avg_episode_steps = 0.0

        if not eval and self.train_log_dto.eval_attacker_action_costs is not None:
            self.attacker_eval_avg_episode_costs = np.mean(self.train_log_dto.eval_attacker_action_costs)
        else:
            self.attacker_eval_avg_episode_costs = 0.0

        if not eval and self.train_log_dto.eval_attacker_action_costs_norm is not None:
            self.attacker_eval_avg_episode_costs_norm = np.mean(self.train_log_dto.eval_attacker_action_costs_norm)
        else:
            self.attacker_eval_avg_episode_costs_norm = 0.0

        if not eval and self.train_log_dto.eval_attacker_action_alerts is not None:
            self.attacker_eval_avg_episode_alerts = np.mean(self.train_log_dto.eval_attacker_action_alerts)
        else:
            self.attacker_eval_avg_episode_alerts = 0.0

        if not eval and self.train_log_dto.eval_attacker_action_alerts_norm is not None:
            self.attacker_eval_avg_episode_alerts_norm = np.mean(self.train_log_dto.eval_attacker_action_alerts_norm)
        else:
            self.attacker_eval_avg_episode_alerts_norm = 0.0

        if not eval and self.train_log_dto.eval_2_episode_flags is not None:
            self.attacker_eval_2_avg_episode_flags = np.mean(self.train_log_dto.eval_2_episode_flags)
        else:
            self.attacker_eval_2_avg_episode_flags = 0.0
        if not eval and self.train_log_dto.eval_2_episode_flags_percentage is not None:
            self.attacker_eval_2_avg_episode_flags_percentage = np.mean(self.train_log_dto.eval_2_episode_flags_percentage)
        else:
            self.attacker_eval_2_avg_episode_flags_percentage = 0.0
        if not eval and self.train_log_dto.eval_2_episode_steps is not None:
            self.attacker_eval_2_avg_episode_steps = np.mean(self.train_log_dto.eval_2_episode_steps)
        else:
            self.attacker_eval_2_avg_episode_steps = 0.0

        if not eval and self.train_log_dto.eval_2_attacker_action_costs is not None:
            self.attacker_eval_2_avg_episode_costs = np.mean(self.train_log_dto.eval_2_attacker_action_costs)
        else:
            self.attacker_eval_2_avg_episode_costs = 0.0
        if not eval and self.train_log_dto.eval_2_attacker_action_costs_norm is not None:
            self.attacker_eval_2_avg_episode_costs_norm = np.mean(self.train_log_dto.eval_2_attacker_action_costs_norm)
        else:
            self.attacker_eval_2_avg_episode_costs_norm = 0.0
        if not eval and self.train_log_dto.eval_2_attacker_action_alerts is not None:
            self.attacker_eval_2_avg_episode_alerts = np.mean(self.train_log_dto.eval_2_attacker_action_alerts)
        else:
            self.attacker_eval_2_avg_episode_alerts = 0.0
        if not eval and self.train_log_dto.eval_2_attacker_action_alerts_norm is not None:
            self.attacker_eval_2_avg_episode_alerts_norm = np.mean(self.train_log_dto.eval_2_attacker_action_alerts_norm)
        else:
            self.attacker_eval_2_avg_episode_alerts_norm = 0.0

        if self.train_log_dto.rollout_times is not None:
            if len(self.train_log_dto.rollout_times) > 0:
                self.attacker_avg_rollout_times = np.mean(self.train_log_dto.rollout_times)
            else:
                self.attacker_avg_rollout_times = 0.0
        else:
            self.attacker_avg_rollout_times = 0.0
        if self.train_log_dto.env_response_times is not None and len(self.train_log_dto.env_response_times) > 0:
            if len(self.train_log_dto.env_response_times) > 0:
                self.attacker_avg_env_response_times = np.mean(self.train_log_dto.env_response_times)
            else:
                self.attacker_avg_env_response_times = 0.0
        else:
            self.attacker_avg_env_response_times = 0.0
        if self.train_log_dto.action_pred_times is not None and len(self.train_log_dto.action_pred_times) > 0:
            if len(self.train_log_dto.action_pred_times) > 0:
                self.attacker_avg_action_pred_times = np.mean(self.train_log_dto.action_pred_times)
            else:
                self.attacker_avg_action_pred_times = 0.0
        else:
            self.attacker_avg_action_pred_times = 0.0
        if self.train_log_dto.grad_comp_times is not None and len(self.train_log_dto.grad_comp_times) > 0:
            if len(self.train_log_dto.grad_comp_times) > 0:
                self.attacker_avg_grad_comp_times = np.mean(self.train_log_dto.grad_comp_times)
            else:
                self.attacker_avg_grad_comp_times = 0.0
        else:
            self.attacker_avg_grad_comp_times = 0.0
        if self.train_log_dto.weight_update_times is not None and len(self.train_log_dto.weight_update_times) > 0:
            if len(self.train_log_dto.weight_update_times):
                self.attacker_avg_weight_update_times = np.mean(self.train_log_dto.weight_update_times)
            else:
                self.attacker_avg_weight_update_times = 0.0
        else:
            self.attacker_avg_weight_update_times = 0.0

    def update_result(self) -> "TrainAgentLogDTO":
        """
        Updates the experiment result with new data

        :return: the updated train_log_dto which includes the updated experiment results
        """
        self.result.avg_episode_steps.append(self.attacker_avg_episode_steps)
        self.result.attacker_avg_episode_rewards.append(self.attacker_avg_episode_rewards)
        self.result.epsilon_values.append(self.attacker_agent_config.epsilon)
        self.result.attacker_avg_episode_loss.append(self.attacker_avg_episode_loss)
        self.result.avg_episode_flags.append(self.attacker_avg_episode_flags)
        self.result.avg_episode_flags_percentage.append(self.attacker_avg_episode_flags_percentage)
        self.result.attacker_eval_avg_episode_rewards.append(self.attacker_eval_avg_episode_rewards)
        self.result.eval_avg_episode_steps.append(self.attacker_eval_avg_episode_steps)
        self.result.eval_avg_episode_flags.append(self.attacker_eval_avg_episode_flags)
        self.result.eval_avg_episode_flags_percentage.append(self.attacker_eval_avg_episode_flags_percentage)
        self.result.attacker_eval_2_avg_episode_rewards.append(self.attacker_eval_2_avg_episode_rewards)
        self.result.eval_2_avg_episode_steps.append(self.attacker_eval_2_avg_episode_steps)
        self.result.eval_2_avg_episode_flags.append(self.attacker_eval_2_avg_episode_flags)
        self.result.eval_2_avg_episode_flags_percentage.append(self.attacker_eval_2_avg_episode_flags_percentage)
        self.result.lr_list.append(self.train_log_dto.attacker_lr)
        self.result.rollout_times.append(self.attacker_avg_rollout_times)
        self.result.env_response_times.append(self.attacker_avg_env_response_times)
        self.result.action_pred_times.append(self.attacker_avg_action_pred_times)
        self.result.grad_comp_times.append(self.attacker_avg_grad_comp_times)
        self.result.weight_update_times.append(self.attacker_avg_weight_update_times)
        self.result.attacker_avg_regret.append(self.attacker_avg_regret)
        self.result.attacker_avg_opt_frac.append(self.attacker_avg_opt_frac)
        self.result.attacker_eval_avg_regret.append(self.attacker_avg_eval_regret)
        self.result.attacker_eval_avg_opt_frac.append(self.attacker_eval_avg_opt_frac)
        self.result.attacker_eval_2_avg_regret.append(self.attacker_avg_regret_2)
        self.result.attacker_eval_2_avg_opt_frac.append(self.attacker_avg_opt_frac_2)
        self.result.caught_frac.append(self.attacker_episode_caught_frac)
        self.result.early_stopping_frac.append(self.attacker_episode_early_stopped_frac)
        self.result.intrusion_frac.append(self.attacker_episode_successful_intrusion_frac)
        self.result.eval_caught_frac.append(self.attacker_eval_episode_caught_frac)
        self.result.eval_early_stopping_frac.append(self.attacker_eval_episode_early_stopped_frac)
        self.result.eval_intrusion_frac.append(self.attacker_eval_episode_successful_intrusion_frac)
        self.result.eval_2_caught_frac.append(self.attacker_eval_2_episode_caught_frac)
        self.result.eval_2_early_stopping_frac.append(self.attacker_eval_2_episode_early_stopped_frac)
        self.result.eval_2_intrusion_frac.append(self.attacker_eval_2_episode_successful_intrusion_frac)
        self.result.attacker_action_costs.append(self.attacker_avg_episode_costs)
        self.result.attacker_action_costs_norm.append(self.attacker_avg_episode_costs_norm)
        self.result.attacker_action_alerts.append(self.attacker_avg_episode_alerts)
        self.result.attacker_action_alerts_norm.append(self.attacker_avg_episode_alerts_norm)
        self.result.eval_attacker_action_costs.append(self.attacker_eval_avg_episode_costs)
        self.result.eval_attacker_action_costs_norm.append(self.attacker_eval_avg_episode_costs_norm)
        self.result.eval_attacker_action_alerts.append(self.attacker_eval_avg_episode_alerts)
        self.result.eval_attacker_action_alerts_norm.append(self.attacker_eval_avg_episode_alerts_norm)
        self.result.eval_2_attacker_action_costs.append(self.attacker_eval_2_avg_episode_costs)
        self.result.eval_2_attacker_action_costs_norm.append(self.attacker_eval_2_avg_episode_costs_norm)
        self.result.eval_2_attacker_action_alerts.append(self.attacker_eval_2_avg_episode_alerts)
        self.result.eval_2_attacker_action_alerts_norm.append(self.attacker_eval_2_avg_episode_alerts_norm)
        self.result.time_elapsed.append(self.attacker_training_time)

        if self.train_log_dto.attacker_train_episode_env_specific_rewards is not None:
            for key in self.train_log_dto.attacker_train_episode_env_specific_rewards.keys():
                avg = np.mean(self.train_log_dto.attacker_train_episode_env_specific_rewards[key])
                if key in self.result.attacker_train_env_specific_rewards:
                    self.result.attacker_train_env_specific_rewards[key].append(avg)
                else:
                    self.result.attacker_train_env_specific_rewards[key] = [avg]
        if self.attacker_train_env_specific_regret is not None:
            for key in self.attacker_train_env_specific_regret.keys():
                avg = np.mean(self.attacker_train_env_specific_regret[key])
                if key in self.result.attacker_train_env_specific_regrets:
                    self.result.attacker_train_env_specific_regrets[key].append(avg)
                else:
                    self.result.attacker_train_env_specific_regrets[key] = [avg]
        if self.attacker_train_env_specific_opt_frac is not None:
            for key in self.tattacker_rain_env_specific_opt_frac.keys():
                avg = np.mean(self.attacker_train_env_specific_opt_frac[key])
                if key in self.result.attacker_train_env_specific_opt_fracs:
                    self.result.attacker_train_env_specific_opt_fracs[key].append(avg)
                else:
                    self.result.attacker_train_env_specific_opt_fracs[key] = [avg]
        if self.train_log_dto.train_env_specific_steps is not None:
            for key in self.train_log_dto.train_env_specific_steps.keys():
                avg = np.mean(self.train_log_dto.train_env_specific_steps[key])
                if key in self.result.train_env_specific_steps:
                    self.result.train_env_specific_steps[key].append(avg)
                else:
                    self.result.train_env_specific_steps[key] = [avg]
        if self.train_log_dto.train_env_specific_flags is not None:
            for key in self.train_log_dto.train_env_specific_flags.keys():
                avg = np.mean(self.train_log_dto.train_env_specific_flags[key])
                if key in self.result.train_env_specific_flags:
                    self.result.train_env_specific_flags[key].append(avg)
                else:
                    self.result.train_env_specific_flags[key] = [avg]
        if self.train_log_dto.train_env_specific_flags_percentage is not None:
            for key in self.train_log_dto.train_env_specific_flags_percentage.keys():
                avg = np.mean(self.train_log_dto.train_env_specific_flags_percentage[key])
                if key in self.result.train_env_specific_flags_percentage:
                    self.result.train_env_specific_flags_percentage[key].append(avg)
                else:
                    self.result.train_env_specific_flags_percentage[key] = [avg]

        if self.train_log_dto.attacker_eval_env_specific_rewards is not None:
            for key in self.train_log_dto.attacker_eval_env_specific_rewards.keys():
                avg = np.mean(self.train_log_dto.attacker_eval_env_specific_rewards[key])
                if key in self.result.attacker_eval_env_specific_rewards:
                    self.result.attacker_eval_env_specific_rewards[key].append(avg)
                else:
                    self.result.attacker_eval_env_specific_rewards[key] = [avg]
        if self.attacker_eval_env_specific_regret is not None:
            for key in self.attacker_eval_env_specific_regret.keys():
                avg = np.mean(self.attacker_eval_env_specific_regret[key])
                if key in self.result.attacker_eval_env_specific_regrets:
                    self.result.attacker_eval_env_specific_regrets[key].append(avg)
                else:
                    self.result.attacker_eval_env_specific_regrets[key] = [avg]
        if self.attacker_eval_env_specific_opt_frac is not None:
            for key in self.attacker_eval_env_specific_opt_frac.keys():
                avg = np.mean(self.attacker_eval_env_specific_opt_frac[key])
                if key in self.result.attacker_eval_env_specific_opt_fracs:
                    self.result.attacker_eval_env_specific_opt_fracs[key].append(avg)
                else:
                    self.result.attacker_eval_env_specific_opt_fracs[key] = [avg]
        if self.train_log_dto.eval_env_specific_steps is not None:
            for key in self.train_log_dto.eval_env_specific_steps.keys():
                avg = np.mean(self.train_log_dto.eval_env_specific_steps[key])
                if key in self.result.eval_env_specific_steps:
                    self.result.eval_env_specific_steps[key].append(avg)
                else:
                    self.result.eval_env_specific_steps[key] = [avg]
        if self.train_log_dto.eval_env_specific_flags is not None:
            for key in self.train_log_dto.eval_env_specific_flags.keys():
                avg = np.mean(self.train_log_dto.eval_env_specific_flags[key])
                if key in self.result.eval_env_specific_flags:
                    self.result.eval_env_specific_flags[key].append(avg)
                else:
                    self.result.eval_env_specific_flags[key] = [avg]
        if self.train_log_dto.eval_env_specific_flags_percentage is not None:
            for key in self.train_log_dto.eval_env_specific_flags_percentage.keys():
                avg = np.mean(self.train_log_dto.eval_env_specific_flags_percentage[key])
                if key in self.result.eval_env_specific_flags_percentage:
                    self.result.eval_env_specific_flags_percentage[key].append(avg)
                else:
                    self.result.eval_env_specific_flags_percentage[key] = [avg]

        if self.train_log_dto.attacker_eval_2_env_specific_rewards is not None:
            for key in self.train_log_dto.attacker_eval_2_env_specific_rewards.keys():
                avg = np.mean(self.train_log_dto.attacker_eval_2_env_specific_rewards[key])
                if key in self.result.attacker_eval_2_env_specific_rewards:
                    self.result.attacker_eval_2_env_specific_rewards[key].append(avg)
                else:
                    self.result.attacker_eval_2_env_specific_rewards[key] = [avg]
        if self.attacker_eval_2_env_specific_regret is not None:
            for key in self.attacker_eval_2_env_specific_regret.keys():
                avg = np.mean(self.attacker_eval_2_env_specific_regret[key])
                if key in self.result.attacker_eval_2_env_specific_regrets:
                    self.result.attacker_eval_2_env_specific_regrets[key].append(avg)
                else:
                    self.result.attacker_eval_2_env_specific_regrets[key] = [avg]
        if self.attacker_eval_2_env_specific_opt_frac is not None:
            for key in self.attacker_eval_2_env_specific_opt_frac.keys():
                avg = np.mean(self.attacker_eval_2_env_specific_opt_frac[key])
                if key in self.result.attacker_eval_2_env_specific_opt_fracs:
                    self.result.attacker_eval_2_env_specific_opt_fracs[key].append(avg)
                else:
                    self.result.attacker_eval_2_env_specific_opt_fracs[key] = [avg]
        if self.train_log_dto.eval_2_env_specific_steps is not None:
            for key in self.train_log_dto.eval_2_env_specific_steps.keys():
                avg = np.mean(self.train_log_dto.eval_2_env_specific_steps[key])
                if key in self.result.eval_2_env_specific_steps:
                    self.result.eval_2_env_specific_steps[key].append(avg)
                else:
                    self.result.eval_2_env_specific_steps[key] = [avg]
        if self.train_log_dto.eval_2_env_specific_flags is not None:
            for key in self.train_log_dto.eval_2_env_specific_flags.keys():
                avg = np.mean(self.train_log_dto.eval_2_env_specific_flags[key])
                if key in self.result.eval_2_env_specific_flags:
                    self.result.eval_2_env_specific_flags[key].append(avg)
                else:
                    self.result.eval_2_env_specific_flags[key] = [avg]
        if self.train_log_dto.eval_2_env_specific_flags_percentage is not None:
            for key in self.train_log_dto.eval_2_env_specific_flags_percentage.keys():
                avg = np.mean(self.train_log_dto.eval_2_env_specific_flags_percentage[key])
                if key in self.result.eval_2_env_specific_flags_percentage:
                    self.result.eval_2_env_specific_flags_percentage[key].append(avg)
                else:
                    self.result.eval_2_env_specific_flags_percentage[key] = [avg]
        if isinstance(self.env, SubprocVecEnv):
            if not eval:
                self.env.reset_pi_star_rew_attacker()
        else:
            if not eval:
                self.env.envs[0].env_config.pi_star_rew_list_attacker = [
                    self.env.envs[0].env_config.pi_star_rew_attacker]

        if self.env_2 is not None:
            if not eval:
                if isinstance(self.env_2, SubprocVecEnv):
                    self.env_2.reset_pi_star_rew_attacker()
                else:
                    self.env_2.envs[0].env_config.pi_star_rew_list_attacker = [
                        self.env_2.envs[0].env_config.pi_star_rew_attacker]
        if not eval:
            self.train_log_dto.train_result = self.result
        else:
            self.train_log_dto.eval_result = self.result
        return self.train_log_dto

    @staticmethod
    def compute_opt_frac(r: float, opt_r: float) -> float:
        """
        Utility function for computing fraction of optimal reward

        :param r: reward
        :param opt_r: optimal reward
        :return: fraction of optimal reward
        """
        abs_difference = abs(opt_r - r)
        if (r >= 0 and opt_r >= 0) or (r <= 0 and opt_r <= 0):
            return r / opt_r
        elif r < 0 and opt_r > 0:
            return 1 / abs_difference
        else:
            return 1 / abs_difference

    @staticmethod
    def compute_regret(r: float, opt_r: float) -> float:
        """
        Utility function for computing the regret

        :param r: the reward
        :param opt_r: the optimal reward
        :return: the regret
        """
        return abs(opt_r - r)

    @staticmethod
    def to_tensorboard_dto(avg_log_dto : "AttackerTrainAgentLogDTOAvg", eps: float,
                           tensorboard_writer) -> TensorboardDataDTO:
        """
        Converts the DTO into a tensorboard DTO

        :param avg_log_dto: the DTO to convert
        :param eps: the epsilon value
        :param tensorboard_writer: the tensorboard writer
        :return: the created tensorboard DTO
        """
        if eps is None:
            eps = 0.0
        tensorboard_data_dto = TensorboardDataDTO(
            iteration=avg_log_dto.train_log_dto.iteration,
            avg_episode_rewards=avg_log_dto.attacker_avg_episode_rewards,
            avg_episode_steps=avg_log_dto.attacker_avg_episode_steps,
            avg_episode_loss=avg_log_dto.attacker_avg_episode_loss, eps=eps,
            lr=avg_log_dto.attacker_lr, eval=avg_log_dto.eval,
            avg_flags_catched=avg_log_dto.attacker_avg_episode_flags,
            avg_episode_flags_percentage=avg_log_dto.attacker_avg_episode_flags_percentage,
            eval_avg_episode_rewards=avg_log_dto.attacker_eval_avg_episode_rewards,
            eval_avg_episode_steps=avg_log_dto.attacker_eval_avg_episode_steps,
            eval_avg_episode_flags=avg_log_dto.attacker_eval_avg_episode_flags,
            eval_avg_episode_flags_percentage=avg_log_dto.attacker_eval_avg_episode_flags_percentage,
            eval_2_avg_episode_rewards=avg_log_dto.attacker_eval_2_avg_episode_rewards,
            eval_2_avg_episode_steps=avg_log_dto.attacker_eval_2_avg_episode_steps,
            eval_2_avg_episode_flags=avg_log_dto.attacker_eval_2_avg_episode_flags,
            eval_2_avg_episode_flags_percentage=avg_log_dto.attacker_eval_2_avg_episode_flags_percentage,
            rolling_avg_episode_rewards=avg_log_dto.attacker_rolling_avg_rewards,
            rolling_avg_episode_steps=avg_log_dto.attacker_rolling_avg_steps,
            tensorboard_writer=tensorboard_writer,
            episode_caught_frac=avg_log_dto.attacker_episode_caught_frac,
            episode_early_stopped_frac=avg_log_dto.attacker_episode_early_stopped_frac,
            episode_successful_intrusion_frac=avg_log_dto.attacker_episode_successful_intrusion_frac,
            eval_episode_caught_frac=avg_log_dto.attacker_eval_episode_caught_frac,
            eval_episode_early_stopped_frac=avg_log_dto.attacker_eval_episode_early_stopped_frac,
            eval_episode_successful_intrusion_frac=avg_log_dto.attacker_eval_episode_successful_intrusion_frac,
            eval_2_episode_caught_frac=avg_log_dto.attacker_eval_2_episode_caught_frac,
            eval_2_episode_early_stopped_frac=avg_log_dto.attacker_eval_2_episode_early_stopped_frac,
            eval_2_episode_successful_intrusion_frac=avg_log_dto.attacker_eval_2_episode_successful_intrusion_frac,
            avg_regret=avg_log_dto.attacker_avg_regret, avg_opt_frac=avg_log_dto.attacker_avg_opt_frac,
            rolling_avg_rewards=avg_log_dto.attacker_rolling_avg_rewards,
            rolling_avg_steps=avg_log_dto.attacker_rolling_avg_steps,
            avg_episode_flags=avg_log_dto.attacker_avg_episode_flags,
            n_af=avg_log_dto.train_log_dto.n_af, n_d=avg_log_dto.train_log_dto.n_d,
            avg_episode_costs=avg_log_dto.attacker_avg_episode_costs,
            avg_episode_costs_norm=avg_log_dto.attacker_avg_episode_costs_norm,
            avg_episode_alerts=avg_log_dto.attacker_avg_episode_alerts,
            avg_episode_alerts_norm=avg_log_dto.attacker_avg_episode_alerts_norm,
            eval_avg_episode_costs=avg_log_dto.attacker_eval_avg_episode_costs,
            eval_avg_episode_costs_norm=avg_log_dto.attacker_eval_avg_episode_costs_norm,
            eval_avg_episode_alerts=avg_log_dto.attacker_eval_avg_episode_alerts,
            eval_avg_episode_alerts_norm=avg_log_dto.attacker_eval_avg_episode_alerts_norm,
            eval_2_avg_episode_costs=avg_log_dto.attacker_eval_2_avg_episode_costs,
            eval_2_avg_episode_costs_norm=avg_log_dto.attacker_eval_2_avg_episode_costs_norm,
            eval_2_avg_episode_alerts=avg_log_dto.attacker_eval_2_avg_episode_alerts,
            eval_2_avg_episode_alerts_norm=avg_log_dto.attacker_eval_2_avg_episode_alerts_norm,
            total_num_episodes=avg_log_dto.train_log_dto.total_num_episodes,
            avg_eval_regret=avg_log_dto.attacker_avg_eval_regret,
            eval_avg_opt_frac=avg_log_dto.attacker_eval_avg_opt_frac, avg_regret_2=avg_log_dto.attacker_avg_regret_2,
            avg_opt_frac_2=avg_log_dto.attacker_avg_opt_frac_2, epsilon=avg_log_dto.attacker_agent_config.epsilon,
            training_time_hours=avg_log_dto.attacker_training_time_hours)
        return tensorboard_data_dto

