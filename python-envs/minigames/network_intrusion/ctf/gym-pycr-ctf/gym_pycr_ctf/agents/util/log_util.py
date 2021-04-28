import numpy as np
import sys
import time
from gym_pycr_ctf.agents.openai_baselines.common.vec_env import SubprocVecEnv
import gym_pycr_ctf.envs_model.logic.common.util as pycr_util
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.dao.agent.train_mode import TrainMode
from gym_pycr_ctf.dao.agent.train_agent_log_dto import TrainAgentLogDTO
from gym_pycr_ctf.dao.agent.tensorboard_data_dto import TensorboardDataDTO


class LogUtil:
    """
    Utility class for logging training progress
    """

    @staticmethod
    def log_metrics_attacker(train_log_dto: TrainAgentLogDTO, eps: float = None, eval: bool = False,
                             env=None, env_2 = None, attacker_agent_config : AgentConfig = None,
                             tensorboard_writer = None) -> TrainAgentLogDTO:
        """
        Logs average metrics for the last <self.config.log_frequency> episodes

        :param train_log_dto: DTO with the information to log
        :param eps: machine eps
        :param eval: flag whether it is evaluation or not
        :param env: the training env
        :param env_2: the evaluation env
        :param attacker_agent_config: the agent config of the attacker
        :param tensorboard_writer: the tensorobard writer
        :return: updated train log dto
        """
        if eps is None:
            eps = 0.0

        if not eval:
            result = train_log_dto.train_result
        else:
            result = train_log_dto.eval_result

        training_time = time.time() - train_log_dto.start_time
        training_time_hours = training_time/3600
        avg_episode_rewards = np.mean(train_log_dto.attacker_episode_rewards)
        avg_episode_flags = np.mean(train_log_dto.episode_flags)
        avg_episode_flags_percentage = np.mean(train_log_dto.episode_flags_percentage)
        avg_episode_steps = np.mean(train_log_dto.episode_steps)
        avg_episode_costs = np.mean(train_log_dto.attacker_action_costs)
        avg_episode_costs_norm = np.mean(train_log_dto.attacker_action_costs_norm)
        avg_episode_alerts = np.mean(train_log_dto.attacker_action_alerts)
        avg_episode_alerts_norm = np.mean(train_log_dto.attacker_action_alerts_norm)

        train_env_specific_regret = {}
        eval_env_specific_regret = {}
        eval_2_env_specific_regret = {}
        train_env_specific_opt_frac = {}
        eval_env_specific_opt_frac = {}
        eval_2_env_specific_opt_frac = {}

        if train_log_dto.episode_caught is not None and train_log_dto.episode_early_stopped is not None \
                and train_log_dto.episode_successful_intrusion is not None:
            total_c_s_i = sum(list(map(lambda x: int(x), train_log_dto.episode_caught))) \
                          + sum(list(map(lambda x: int(x), train_log_dto.episode_early_stopped))) \
                          + sum(list(map(lambda x: int(x), train_log_dto.episode_successful_intrusion)))
        else:
            total_c_s_i = 1
        if train_log_dto.eval_episode_caught is not None and train_log_dto.eval_episode_early_stopped is not None \
                and train_log_dto.eval_episode_successful_intrusion is not None:
            eval_total_c_s_i = sum(list(map(lambda x: int(x), train_log_dto.eval_episode_caught))) \
                               + sum(list(map(lambda x: int(x), train_log_dto.eval_episode_early_stopped))) \
                               + sum(list(map(lambda x: int(x), train_log_dto.eval_episode_successful_intrusion)))
        else:
            eval_total_c_s_i = 1
        if train_log_dto.eval_2_episode_caught is not None and train_log_dto.eval_2_episode_early_stopped is not None \
                and train_log_dto.eval_2_episode_successful_intrusion is not None:
            eval_2_total_c_s_i = sum(list(map(lambda x: int(x), train_log_dto.eval_2_episode_caught))) \
                                 + sum(list(map(lambda x: int(x), train_log_dto.eval_2_episode_early_stopped))) \
                                 + sum(list(map(lambda x: int(x), train_log_dto.eval_2_episode_successful_intrusion)))
        else:
            eval_2_total_c_s_i = 1
        if train_log_dto.episode_caught is not None:
            episode_caught_frac = sum(list(map(lambda x: int(x), train_log_dto.episode_caught))) / max(1, total_c_s_i)
        else:
            episode_caught_frac = 0

        if train_log_dto.episode_early_stopped is not None:
            episode_early_stopped_frac = sum(list(map(lambda x: int(x),
                                                      train_log_dto.episode_early_stopped))) / max(1, total_c_s_i)
        else:
            episode_early_stopped_frac = 0

        if train_log_dto.episode_successful_intrusion is not None:
            episode_successful_intrusion_frac = sum(list(map(lambda x: int(x),
                                                             train_log_dto.episode_successful_intrusion))) / max(1,
                                                                                                                 total_c_s_i)
        else:
            episode_successful_intrusion_frac = 0

        if train_log_dto.eval_episode_caught is not None:
            eval_episode_caught_frac = sum(list(map(lambda x: int(x),
                                                    train_log_dto.eval_episode_caught))) / max(1, eval_total_c_s_i)
        else:
            eval_episode_caught_frac = 0

        if train_log_dto.eval_episode_successful_intrusion is not None:
            eval_episode_successful_intrusion_frac = sum(list(map(lambda x: int(x),
                                                                  train_log_dto.eval_episode_successful_intrusion))) / max(
                1, eval_total_c_s_i)
        else:
            eval_episode_successful_intrusion_frac = 0

        if train_log_dto.eval_episode_early_stopped is not None:
            eval_episode_early_stopped_frac = sum(list(map(lambda x: int(x),
                                                           train_log_dto.eval_episode_early_stopped))) / max(1,
                                                                                                             eval_total_c_s_i)
        else:
            eval_episode_early_stopped_frac = 0

        if train_log_dto.eval_2_episode_caught is not None:
            eval_2_episode_caught_frac = sum(list(map(lambda x: int(x),
                                                      train_log_dto.eval_2_episode_caught))) / max(1,
                                                                                                   eval_2_total_c_s_i)
        else:
            eval_2_episode_caught_frac = 0

        if train_log_dto.eval_2_episode_successful_intrusion is not None:
            eval_2_episode_successful_intrusion_frac = sum(list(map(lambda x: int(x),
                                                                    train_log_dto.eval_2_episode_successful_intrusion))) / max(
                1, eval_2_total_c_s_i)
        else:
            eval_2_episode_successful_intrusion_frac = 0

        if train_log_dto.eval_2_episode_early_stopped is not None:
            eval_2_episode_early_stopped_frac = sum(list(map(lambda x: int(x),
                                                             train_log_dto.eval_2_episode_early_stopped))) / max(1,
                                                                                                                 eval_2_total_c_s_i)
        else:
            eval_2_episode_early_stopped_frac = 0


        if result.attacker_avg_episode_rewards is not None:
            rolling_avg_rewards = pycr_util.running_average(result.attacker_avg_episode_rewards + [avg_episode_rewards],
                                                            attacker_agent_config.running_avg)
        else:
            rolling_avg_rewards = 0.0

        if result.avg_episode_steps is not None:
            rolling_avg_steps = pycr_util.running_average(result.avg_episode_steps + [avg_episode_steps],
                                                          attacker_agent_config.running_avg)
        else:
            rolling_avg_steps = 0.0

        if train_log_dto.attacker_lr is None:
            lr = 0.0
        else:
            lr = train_log_dto.attacker_lr
        if not eval and train_log_dto.attacker_episode_avg_loss is not None:
            avg_episode_loss = np.mean(train_log_dto.attacker_episode_avg_loss)
        else:
            avg_episode_loss = 0.0

        if not eval and train_log_dto.attacker_eval_episode_rewards is not None:
            eval_avg_episode_rewards = np.mean(train_log_dto.attacker_eval_episode_rewards)
        else:
            eval_avg_episode_rewards = 0.0

        if not eval and train_log_dto.attacker_eval_2_episode_rewards is not None:
            eval_2_avg_episode_rewards = np.mean(train_log_dto.attacker_eval_2_episode_rewards)
        else:
            eval_2_avg_episode_rewards = 0.0
        if attacker_agent_config.log_regret:
            if env.env_config is not None:
                if len(env.envs[0].env_config.pi_star_rew_list_attacker) >= len(
                        train_log_dto.attacker_eval_episode_rewards):
                    pi_star_rews_attacker = env.envs[0].env_config.pi_star_rew_list_attacker[
                                            -len(train_log_dto.attacker_eval_episode_rewards):]
                    r = [LogUtil.compute_regret(opt_r=pi_star_rews_attacker[i], r=train_log_dto.attacker_eval_episode_rewards[i]) for i in
                         range(len(train_log_dto.attacker_eval_episode_rewards))]
                    avg_regret = np.mean(np.array(r))
                else:
                    avg_regret = LogUtil.compute_regret(r=avg_episode_rewards, opt_r=env.envs[0].env_config.pi_star_rew_attacker)

                if train_log_dto.attacker_eval_episode_rewards is not None and train_log_dto.attacker_eval_env_specific_rewards != {}:
                    if len(env.envs[0].env_config.pi_star_rew_list_attacker) >= len(
                            train_log_dto.attacker_eval_episode_rewards):
                        pi_star_rews_attacker = env.envs[0].env_config.pi_star_rew_list_attacker[
                                                -len(train_log_dto.attacker_eval_episode_rewards):]
                        r = [LogUtil.compute_regret(opt_r=pi_star_rews_attacker[i], r=train_log_dto.attacker_eval_episode_rewards[i])
                             for i in range(len(train_log_dto.attacker_eval_episode_rewards))]
                        avg_eval_regret = np.mean(np.array(r))
                    else:
                        avg_eval_regret = LogUtil.compute_regret(opt_r=env.envs[0].env_config.pi_star_rew_attacker,
                                                                 r=eval_avg_episode_rewards)
                else:
                    avg_eval_regret = 0.0

            elif (train_log_dto.attacker_train_episode_env_specific_rewards is None
                  or train_log_dto.attacker_train_episode_env_specific_rewards == {}) and \
                    (train_log_dto.attacker_eval_env_specific_rewards is None
                     or train_log_dto.attacker_eval_env_specific_rewards == {}):
                env_regret = env.get_pi_star_rew_attacker()[0]
                ip = env_regret[0]

                if len(env_regret[2]) >= len(train_log_dto.attacker_episode_rewards):
                    pi_star_rews_attacker = env_regret[2][-len(train_log_dto.attacker_episode_rewards):]
                    r = [LogUtil.compute_regret(opt_r=pi_star_rews_attacker[i], r=train_log_dto.attacker_episode_rewards[i]) for i in
                         range(len(train_log_dto.attacker_episode_rewards))]
                    avg_regret = np.mean(np.array(r))
                else:
                    avg_regret = LogUtil.compute_regret(opt_r=env_regret[1],r=avg_episode_rewards)

                if train_log_dto.attacker_eval_episode_rewards is not None:
                    if len(env_regret[2]) >= len(train_log_dto.attacker_eval_episode_rewards):
                        pi_star_rews_attacker = env_regret[2][-len(train_log_dto.attacker_eval_episode_rewards):]
                        r = [LogUtil.compute_regret(opt_r=pi_star_rews_attacker[i], r=train_log_dto.attacker_eval_episode_rewards[i])
                             for i in range(len(train_log_dto.attacker_eval_episode_rewards))]
                        avg_eval_regret = np.mean(np.array(r))
                    else:
                        avg_eval_regret = LogUtil.compute_regret(opt_r=env_regret[1],r=eval_avg_episode_rewards)
                else:
                    avg_eval_regret = 0.0
            else:
                regrets = []
                eval_regrets = []
                pi_star_rew_per_env = env.get_pi_star_rew_attacker()
                for env_regret in pi_star_rew_per_env:
                    ip = env_regret[0]
                    pi_star_rew = env_regret[1]
                    if train_log_dto.attacker_train_episode_env_specific_rewards is not None \
                            and train_log_dto.attacker_train_episode_env_specific_rewards != {}:
                        rewards = train_log_dto.attacker_train_episode_env_specific_rewards[ip]
                        if len(env_regret[2]) >= len(rewards):
                            pi_star_rews_attacker = env_regret[2][-len(rewards):]
                            r = [LogUtil.compute_regret(opt_r=pi_star_rews_attacker[i], r=rewards[i]) for i in range(len(rewards))]
                        else:
                            r = [LogUtil.compute_regret(opt_r=env_regret[1], r=rewards[i]) for i in range(len(rewards))]
                        train_env_specific_regret[ip] = r
                        regrets = regrets + r
                    if train_log_dto.attacker_eval_env_specific_rewards is not None and train_log_dto.attacker_eval_env_specific_rewards != {}:
                        rewards = train_log_dto.attacker_eval_env_specific_rewards[ip]
                        if len(env_regret[2]) >= len(rewards):
                            pi_star_rews_attacker = env_regret[2][-len(rewards):]
                            rewards = [np.mean(rewards[i]) for i in range(len(rewards))]
                            r = [LogUtil.compute_regret(opt_r=pi_star_rews_attacker[i], r=rewards[i]) for i in range(len(rewards))]
                        else:
                            rewards = [np.mean(rewards[i]) for i in range(len(rewards))]
                            r = list(map(lambda x: LogUtil.compute_regret(opt_r=pi_star_rew, r=x), rewards))
                        eval_env_specific_regret[ip] = r
                        eval_regrets = eval_regrets + r

                avg_regret = np.mean(np.array(regrets))
                avg_eval_regret = np.mean(eval_regrets)

            if env_2 is not None:
                if env_2.env_config is not None:
                    if len(env_2.envs[0].env_config.pi_star_rew_list_attacker) >= len(
                            train_log_dto.attacker_eval_2_episode_rewards):
                        pi_star_rews_attacker = env_2.envs[0].env_config.pi_star_rew_list_attacker[
                                                -len(train_log_dto.attacker_eval_2_episode_rewards):]
                        r = [LogUtil.compute_regret(opt_r=pi_star_rews_attacker[i],
                                                    r=train_log_dto.attacker_eval_2_episode_rewards[i])
                             for i in range(len(train_log_dto.attacker_eval_2_episode_rewards))]
                        avg_regret_2 = np.mean(np.array(r))

                        of = [LogUtil.compute_opt_frac(r=train_log_dto.attacker_eval_2_episode_rewards[i],
                                                       opt_r=pi_star_rews_attacker[i])
                              for i in range(len(train_log_dto.attacker_eval_2_episode_rewards))]
                        avg_opt_frac_2 = np.mean(np.array(of))
                    else:
                        avg_regret_2 = LogUtil.compute_regret(opt_r=env_2.envs[0].env_config.pi_star_rew_attacker,
                                                                 r=eval_2_avg_episode_rewards)
                        avg_opt_frac_2 = LogUtil.compute_opt_frac(r=eval_2_avg_episode_rewards,
                                                                  opt_r=env_2.envs[0].env_config.pi_star_rew_attacker)
                else:
                    regrets_2 = []
                    pi_star_rew_per_env_2 = env_2.get_pi_star_rew_attacker()
                    for env_regret in pi_star_rew_per_env_2:
                        ip = env_regret[0]
                        pi_star_rew = env_regret[1]
                        if train_log_dto.attacker_eval_2_env_specific_rewards is not None \
                                and train_log_dto.attacker_eval_2_env_specific_rewards != {}:
                            rewards = train_log_dto.attacker_eval_2_env_specific_rewards[ip]
                            # print("len ip:{} reg:{}, rews:{}".format(ip, env_regret[2], rewards))
                            # pi_star_rews = env_regret[2][-len(rewards):]
                            rewards = [np.mean(rewards[i]) for i in range(len(rewards))]
                            r = [LogUtil.compute_regret(opt_r=pi_star_rew, r=rewards[i]) for i in range(len(rewards))]
                            # r = list(map(lambda x: pi_star_rew - x, rewards))
                            eval_2_env_specific_regret[ip] = r
                            regrets_2 = regrets_2 + r
                    if len(regrets_2) == 0:
                        avg_regret_2 = 0.0
                    else:
                        avg_regret_2 = np.mean(np.array(regrets_2))

                    opt_fracs = []
                    for env_pi_star in pi_star_rew_per_env_2:
                        ip = env_pi_star[0]
                        pi_star_rew = env_pi_star[1]
                        if train_log_dto.attacker_eval_2_env_specific_rewards is not None \
                                and train_log_dto.attacker_eval_2_env_specific_rewards != {}:
                            rewards = train_log_dto.attacker_eval_2_env_specific_rewards[ip]
                            rewards = [np.mean(rewards[i]) for i in range(len(rewards))]
                            # pi_star_rews = env_regret[2][-len(rewards):]
                            of = [LogUtil.compute_opt_frac(r=rewards[i], opt_r=pi_star_rew) for i in range(len(rewards))]
                            # of = list(map(lambda x: x / pi_star_rew, rewards))
                            eval_2_env_specific_opt_frac[ip] = of
                            opt_fracs = opt_fracs + of
                    if len(opt_fracs) == 0:
                        avg_opt_frac_2 = 0.0
                    else:
                        avg_opt_frac_2 = np.mean(np.array(opt_fracs))
            else:
                avg_regret_2 = 0.0
                avg_opt_frac_2 = 0.0
            if env.env_config is not None:

                if len(env.envs[0].env_config.pi_star_rew_list_attacker) >= len(
                        train_log_dto.attacker_episode_rewards):
                    pi_star_rews_attacker = env.envs[0].env_config.pi_star_rew_list_attacker[-len(
                        train_log_dto.attacker_episode_rewards):]
                    of = [LogUtil.compute_opt_frac(r=train_log_dto.attacker_episode_rewards[i],
                                                   opt_r=pi_star_rews_attacker[i]) for i in range(len(
                        train_log_dto.attacker_episode_rewards))]
                    avg_opt_frac = np.mean(np.array(of))
                else:
                    avg_opt_frac = LogUtil.compute_opt_frac(r=avg_episode_rewards,
                                                            opt_r=env.envs[0].env_config.pi_star_rew_attacker)

                if train_log_dto.attacker_eval_episode_rewards is not None:
                    if len(env.envs[0].env_config.pi_star_rew_list_attacker) >= len(
                            train_log_dto.attacker_eval_episode_rewards):
                        pi_star_rews_attacker = env.envs[0].env_config.pi_star_rew_list_attacker[
                                                -len(train_log_dto.attacker_eval_episode_rewards):]
                        of = [LogUtil.compute_opt_frac(r=train_log_dto.attacker_eval_episode_rewards[i],
                                                       opt_r=pi_star_rews_attacker[i])
                              for i in range(len(train_log_dto.attacker_eval_episode_rewards))]
                        eval_avg_opt_frac = np.mean(np.array(of))
                    else:
                        eval_avg_opt_frac = LogUtil.compute_opt_frac(r=eval_avg_episode_rewards,
                                                                     opt_r=env.envs[0].env_config.pi_star_rew_attacker)
                else:
                    eval_avg_opt_frac = 0.0
            elif (train_log_dto.attacker_train_episode_env_specific_rewards is None
                  or train_log_dto.attacker_train_episode_env_specific_rewards == {}) and \
                    (train_log_dto.attacker_eval_env_specific_rewards is None or
                     train_log_dto.attacker_eval_env_specific_rewards == {}):
                env_regret = env.get_pi_star_rew_attacker()[0]
                ip = env_regret[0]

                if len(env_regret[2]) >= len(train_log_dto.attacker_episode_rewards):
                    pi_star_rews_attacker = env_regret[2][-len(train_log_dto.attacker_episode_rewards):]
                    of = [LogUtil.compute_opt_frac(r=train_log_dto.attacker_episode_rewards[i],
                                                   opt_r=pi_star_rews_attacker[i]) for i in range(len(
                        train_log_dto.attacker_episode_rewards))]
                    avg_opt_frac = np.mean(np.array(of))
                else:
                    avg_opt_frac = LogUtil.compute_opt_frac(r=avg_episode_rewards, opt_r=env_regret[1])

                if train_log_dto.attacker_eval_episode_rewards is not None:
                    if len(env_regret[2]) >= len(eval_avg_episode_rewards):
                        pi_star_rews_attacker = env_regret[2][-len(train_log_dto.attacker_eval_episode_rewards):]
                        of = [LogUtil.compute_opt_frac(r=train_log_dto.attacker_eval_episode_rewards[i],
                                                       opt_r=pi_star_rews_attacker[i])
                              for i in range(len(train_log_dto.attacker_eval_episode_rewards))]
                        eval_avg_opt_frac = np.mean(np.array(of))
                    else:
                        eval_avg_opt_frac = LogUtil.compute_opt_frac(r=eval_avg_episode_rewards,opt_r=env_regret[1])
                else:
                    eval_avg_opt_frac = 0.0
            else:
                opt_fracs = []
                eval_opt_fracs = []
                pi_star_rew_per_env = env.get_pi_star_rew_attacker()
                for env_pi_star in pi_star_rew_per_env:
                    ip = env_pi_star[0]
                    pi_star_rew = env_pi_star[1]
                    if train_log_dto.attacker_train_episode_env_specific_rewards is not None \
                            and train_log_dto.attacker_train_episode_env_specific_rewards != {}:
                        rewards = train_log_dto.attacker_train_episode_env_specific_rewards[ip]
                        if len(env_pi_star[2]) >= len(rewards):
                            pi_star_rews_attacker = env_pi_star[2][-len(rewards):]
                            of = [LogUtil.compute_opt_frac(r=rewards[i],opt_r=pi_star_rews_attacker[i])
                                  for i in range(len(rewards))]
                        else:
                            of = list(map(lambda x: LogUtil.compute_opt_frac(r=x, opt_r=pi_star_rew), rewards))
                        train_env_specific_opt_frac[ip] = of
                        opt_fracs = opt_fracs + of
                    elif train_log_dto.attacker_eval_env_specific_rewards is not None \
                            and train_log_dto.attacker_eval_env_specific_rewards != {}:
                        rewards = train_log_dto.attacker_eval_env_specific_rewards[ip]
                        if len(env_pi_star[2]) >= len(rewards):
                            pi_star_rews_attacker = env_pi_star[2][-len(rewards):]
                            of = [LogUtil.compute_opt_frac(r=rewards[i], opt_r=pi_star_rews_attacker[i])
                                  for i in range(len(rewards))]
                        else:
                            of = list(map(lambda x: LogUtil.compute_opt_frac(r=x, opt_r=pi_star_rew), rewards))
                        eval_env_specific_opt_frac[ip] = of
                        eval_opt_fracs = eval_opt_fracs + of
                if len(opt_fracs) == 0:
                    avg_opt_frac = 0.0
                else:
                    avg_opt_frac = np.mean(np.array(opt_fracs))
                if len(eval_opt_fracs) == 0.0:
                    eval_avg_opt_frac = 0.0
                else:
                    eval_avg_opt_frac = np.mean(eval_opt_fracs)
        else:
            avg_regret = 0.0
            avg_eval_regret = 0.0
            avg_eval2_regret = 0.0
            avg_opt_frac = 0.0
            eval_avg_opt_frac = 0.0
            avg_opt_frac_2 = 0.0
            avg_regret_2 = 0.0
            avg_opt_frac_2 = 0.0
        if not eval and train_log_dto.eval_episode_flags is not None:
            eval_avg_episode_flags = np.mean(train_log_dto.eval_episode_flags)
        else:
            eval_avg_episode_flags = 0.0
        if not eval and train_log_dto.eval_episode_flags_percentage is not None:
            eval_avg_episode_flags_percentage = np.mean(train_log_dto.eval_episode_flags_percentage)
        else:
            eval_avg_episode_flags_percentage = 0.0
        if not eval and train_log_dto.eval_episode_steps is not None:
            eval_avg_episode_steps = np.mean(train_log_dto.eval_episode_steps)
        else:
            eval_avg_episode_steps = 0.0

        if not eval and train_log_dto.eval_attacker_action_costs is not None:
            eval_avg_episode_costs = np.mean(train_log_dto.eval_attacker_action_costs)
        else:
            eval_avg_episode_costs = 0.0

        if not eval and train_log_dto.eval_attacker_action_costs_norm is not None:
            eval_avg_episode_costs_norm = np.mean(train_log_dto.eval_attacker_action_costs_norm)
        else:
            eval_avg_episode_costs_norm = 0.0

        if not eval and train_log_dto.eval_attacker_action_alerts is not None:
            eval_avg_episode_alerts = np.mean(train_log_dto.eval_attacker_action_alerts)
        else:
            eval_avg_episode_alerts = 0.0

        if not eval and train_log_dto.eval_attacker_action_alerts_norm is not None:
            eval_avg_episode_alerts_norm = np.mean(train_log_dto.eval_attacker_action_alerts_norm)
        else:
            eval_avg_episode_alerts_norm = 0.0

        if not eval and train_log_dto.eval_2_episode_flags is not None:
            eval_2_avg_episode_flags = np.mean(train_log_dto.eval_2_episode_flags)
        else:
            eval_2_avg_episode_flags = 0.0
        if not eval and train_log_dto.eval_2_episode_flags_percentage is not None:
            eval_2_avg_episode_flags_percentage = np.mean(train_log_dto.eval_2_episode_flags_percentage)
        else:
            eval_2_avg_episode_flags_percentage = 0.0
        if not eval and train_log_dto.eval_2_episode_steps is not None:
            eval_2_avg_episode_steps = np.mean(train_log_dto.eval_2_episode_steps)
        else:
            eval_2_avg_episode_steps = 0.0

        if not eval and train_log_dto.eval_2_attacker_action_costs is not None:
            eval_2_avg_episode_costs = np.mean(train_log_dto.eval_2_attacker_action_costs)
        else:
            eval_2_avg_episode_costs = 0.0
        if not eval and train_log_dto.eval_2_attacker_action_costs_norm is not None:
            eval_2_avg_episode_costs_norm = np.mean(train_log_dto.eval_2_attacker_action_costs_norm)
        else:
            eval_2_avg_episode_costs_norm = 0.0
        if not eval and train_log_dto.eval_2_attacker_action_alerts is not None:
            eval_2_avg_episode_alerts = np.mean(train_log_dto.eval_2_attacker_action_alerts)
        else:
            eval_2_avg_episode_alerts = 0.0
        if not eval and train_log_dto.eval_2_attacker_action_alerts_norm is not None:
            eval_2_avg_episode_alerts_norm = np.mean(train_log_dto.eval_2_attacker_action_alerts_norm)
        else:
            eval_2_avg_episode_alerts_norm = 0.0

        if train_log_dto.rollout_times is not None:
            if len(train_log_dto.rollout_times) > 0:
                avg_rollout_times = np.mean(train_log_dto.rollout_times)
            else:
                avg_rollout_times = 0.0
        else:
            avg_rollout_times = 0.0
        if train_log_dto.env_response_times is not None and len(train_log_dto.env_response_times) > 0:
            if len(train_log_dto.env_response_times) > 0:
                avg_env_response_times = np.mean(train_log_dto.env_response_times)
            else:
                avg_env_response_times = 0.0
        else:
            avg_env_response_times = 0.0
        if train_log_dto.action_pred_times is not None and len(train_log_dto.action_pred_times) > 0:
            if len(train_log_dto.action_pred_times) > 0:
                avg_action_pred_times = np.mean(train_log_dto.action_pred_times)
            else:
                avg_action_pred_times = 0.0
        else:
            avg_action_pred_times = 0.0
        if train_log_dto.grad_comp_times is not None and len(train_log_dto.grad_comp_times) > 0:
            if len(train_log_dto.grad_comp_times) > 0:
                avg_grad_comp_times = np.mean(train_log_dto.grad_comp_times)
            else:
                avg_grad_comp_times = 0.0
        else:
            avg_grad_comp_times = 0.0
        if train_log_dto.weight_update_times is not None and len(train_log_dto.weight_update_times) > 0:
            if len(train_log_dto.weight_update_times):
                avg_weight_update_times = np.mean(train_log_dto.weight_update_times)
            else:
                avg_weight_update_times = 0.0
        else:
            avg_weight_update_times = 0.0

        tensorboard_data_dto = TensorboardDataDTO(
            iteration=train_log_dto.iteration, avg_episode_rewards=avg_episode_rewards,
            avg_episode_steps=avg_episode_steps,
            avg_episode_loss=avg_episode_loss, eps=eps, lr=lr, eval=eval,
            avg_flags_catched=avg_episode_flags, avg_episode_flags_percentage=avg_episode_flags_percentage,
            eval_avg_episode_rewards=eval_avg_episode_rewards, eval_avg_episode_steps=eval_avg_episode_steps,
            eval_avg_episode_flags=eval_avg_episode_flags,
            eval_avg_episode_flags_percentage=eval_avg_episode_flags_percentage,
            eval_2_avg_episode_rewards=eval_2_avg_episode_rewards,
            eval_2_avg_episode_steps=eval_2_avg_episode_steps,
            eval_2_avg_episode_flags=eval_2_avg_episode_flags,
            eval_2_avg_episode_flags_percentage=eval_2_avg_episode_flags_percentage,
            rolling_avg_episode_rewards=rolling_avg_rewards,
            rolling_avg_episode_steps=rolling_avg_steps,
            tensorboard_writer=tensorboard_writer,
            episode_caught_frac=episode_caught_frac,
            episode_early_stopped_frac=episode_early_stopped_frac,
            episode_successful_intrusion_frac=episode_successful_intrusion_frac,
            eval_episode_caught_frac=eval_episode_caught_frac,
            eval_episode_early_stopped_frac=eval_episode_early_stopped_frac,
            eval_episode_successful_intrusion_frac=eval_episode_successful_intrusion_frac,
            eval_2_episode_caught_frac=eval_2_episode_caught_frac,
            eval_2_episode_early_stopped_frac=eval_2_episode_early_stopped_frac,
            eval_2_episode_successful_intrusion_frac=eval_2_episode_successful_intrusion_frac,
            avg_regret=avg_regret, avg_opt_frac=avg_opt_frac, rolling_avg_rewards=rolling_avg_rewards,
            rolling_avg_steps=rolling_avg_steps, avg_episode_flags=avg_episode_flags,
            n_af=train_log_dto.n_af, n_d=train_log_dto.n_d, avg_episode_costs=avg_episode_costs,
            avg_episode_costs_norm=avg_episode_costs_norm,
            avg_episode_alerts=avg_episode_alerts, avg_episode_alerts_norm=avg_episode_alerts_norm,
            eval_avg_episode_costs=eval_avg_episode_costs, eval_avg_episode_costs_norm=eval_avg_episode_costs_norm,
            eval_avg_episode_alerts=eval_avg_episode_alerts, eval_avg_episode_alerts_norm=eval_avg_episode_alerts_norm,
            eval_2_avg_episode_costs=eval_2_avg_episode_costs,
            eval_2_avg_episode_costs_norm=eval_2_avg_episode_costs_norm,
            eval_2_avg_episode_alerts=eval_2_avg_episode_alerts,
            eval_2_avg_episode_alerts_norm=eval_2_avg_episode_alerts_norm,
            total_num_episodes=train_log_dto.total_num_episodes, avg_eval_regret=avg_eval_regret,
            eval_avg_opt_frac=eval_avg_opt_frac,avg_regret_2=avg_regret_2,
            avg_opt_frac_2=avg_opt_frac_2, epsilon=attacker_agent_config.epsilon,
            training_time_hours=training_time_hours)
        log_str = tensorboard_data_dto.log_str_attacker()
        attacker_agent_config.logger.info(log_str)
        print(log_str)
        sys.stdout.flush()
        if attacker_agent_config.tensorboard:
            tensorboard_data_dto.log_tensorboard_attacker()

        result.avg_episode_steps.append(avg_episode_steps)
        result.attacker_avg_episode_rewards.append(avg_episode_rewards)
        result.epsilon_values.append(attacker_agent_config.epsilon)
        result.attacker_avg_episode_loss.append(avg_episode_loss)
        result.avg_episode_flags.append(avg_episode_flags)
        result.avg_episode_flags_percentage.append(avg_episode_flags_percentage)
        result.attacker_eval_avg_episode_rewards.append(eval_avg_episode_rewards)
        result.eval_avg_episode_steps.append(eval_avg_episode_steps)
        result.eval_avg_episode_flags.append(eval_avg_episode_flags)
        result.eval_avg_episode_flags_percentage.append(eval_avg_episode_flags_percentage)
        result.attacker_eval_2_avg_episode_rewards.append(eval_2_avg_episode_rewards)
        result.eval_2_avg_episode_steps.append(eval_2_avg_episode_steps)
        result.eval_2_avg_episode_flags.append(eval_2_avg_episode_flags)
        result.eval_2_avg_episode_flags_percentage.append(eval_2_avg_episode_flags_percentage)
        result.lr_list.append(train_log_dto.attacker_lr)
        result.rollout_times.append(avg_rollout_times)
        result.env_response_times.append(avg_env_response_times)
        result.action_pred_times.append(avg_action_pred_times)
        result.grad_comp_times.append(avg_grad_comp_times)
        result.weight_update_times.append(avg_weight_update_times)
        result.attacker_avg_regret.append(avg_regret)
        result.attacker_avg_opt_frac.append(avg_opt_frac)
        result.attacker_eval_avg_regret.append(avg_eval_regret)
        result.attacker_eval_avg_opt_frac.append(eval_avg_opt_frac)
        result.attacker_eval_2_avg_regret.append(avg_regret_2)
        result.attacker_eval_2_avg_opt_frac.append(avg_opt_frac_2)
        result.caught_frac.append(episode_caught_frac)
        result.early_stopping_frac.append(episode_early_stopped_frac)
        result.intrusion_frac.append(episode_successful_intrusion_frac)
        result.eval_caught_frac.append(eval_episode_caught_frac)
        result.eval_early_stopping_frac.append(eval_episode_early_stopped_frac)
        result.eval_intrusion_frac.append(eval_episode_successful_intrusion_frac)
        result.eval_2_caught_frac.append(eval_2_episode_caught_frac)
        result.eval_2_early_stopping_frac.append(eval_2_episode_early_stopped_frac)
        result.eval_2_intrusion_frac.append(eval_2_episode_successful_intrusion_frac)
        result.attacker_action_costs.append(avg_episode_costs)
        result.attacker_action_costs_norm.append(avg_episode_costs_norm)
        result.attacker_action_alerts.append(avg_episode_alerts)
        result.attacker_action_alerts_norm.append(avg_episode_alerts_norm)
        result.eval_attacker_action_costs.append(eval_avg_episode_costs)
        result.eval_attacker_action_costs_norm.append(eval_avg_episode_costs_norm)
        result.eval_attacker_action_alerts.append(eval_avg_episode_alerts)
        result.eval_attacker_action_alerts_norm.append(eval_avg_episode_alerts_norm)
        result.eval_2_attacker_action_costs.append(eval_2_avg_episode_costs)
        result.eval_2_attacker_action_costs_norm.append(eval_2_avg_episode_costs_norm)
        result.eval_2_attacker_action_alerts.append(eval_2_avg_episode_alerts)
        result.eval_2_attacker_action_alerts_norm.append(eval_2_avg_episode_alerts_norm)
        result.time_elapsed.append(training_time)

        if train_log_dto.attacker_train_episode_env_specific_rewards is not None:
            for key in train_log_dto.attacker_train_episode_env_specific_rewards.keys():
                avg = np.mean(train_log_dto.attacker_train_episode_env_specific_rewards[key])
                if key in result.attacker_train_env_specific_rewards:
                    result.attacker_train_env_specific_rewards[key].append(avg)
                else:
                    result.attacker_train_env_specific_rewards[key] = [avg]
        if train_env_specific_regret is not None:
            for key in train_env_specific_regret.keys():
                avg = np.mean(train_env_specific_regret[key])
                if key in result.attacker_train_env_specific_regrets:
                    result.attacker_train_env_specific_regrets[key].append(avg)
                else:
                    result.attacker_train_env_specific_regrets[key] = [avg]
        if train_env_specific_opt_frac is not None:
            for key in train_env_specific_opt_frac.keys():
                avg = np.mean(train_env_specific_opt_frac[key])
                if key in result.attacker_train_env_specific_opt_fracs:
                    result.attacker_train_env_specific_opt_fracs[key].append(avg)
                else:
                    result.attacker_train_env_specific_opt_fracs[key] = [avg]
        if train_log_dto.train_env_specific_steps is not None:
            for key in train_log_dto.train_env_specific_steps.keys():
                avg = np.mean(train_log_dto.train_env_specific_steps[key])
                if key in result.train_env_specific_steps:
                    result.train_env_specific_steps[key].append(avg)
                else:
                    result.train_env_specific_steps[key] = [avg]
        if train_log_dto.train_env_specific_flags is not None:
            for key in train_log_dto.train_env_specific_flags.keys():
                avg = np.mean(train_log_dto.train_env_specific_flags[key])
                if key in result.train_env_specific_flags:
                    result.train_env_specific_flags[key].append(avg)
                else:
                    result.train_env_specific_flags[key] = [avg]
        if train_log_dto.train_env_specific_flags_percentage is not None:
            for key in train_log_dto.train_env_specific_flags_percentage.keys():
                avg = np.mean(train_log_dto.train_env_specific_flags_percentage[key])
                if key in result.train_env_specific_flags_percentage:
                    result.train_env_specific_flags_percentage[key].append(avg)
                else:
                    result.train_env_specific_flags_percentage[key] = [avg]

        if train_log_dto.attacker_eval_env_specific_rewards is not None:
            for key in train_log_dto.attacker_eval_env_specific_rewards.keys():
                avg = np.mean(train_log_dto.attacker_eval_env_specific_rewards[key])
                if key in result.attacker_eval_env_specific_rewards:
                    result.attacker_eval_env_specific_rewards[key].append(avg)
                else:
                    result.attacker_eval_env_specific_rewards[key] = [avg]
        if eval_env_specific_regret is not None:
            for key in eval_env_specific_regret.keys():
                avg = np.mean(eval_env_specific_regret[key])
                if key in result.attacker_eval_env_specific_regrets:
                    result.attacker_eval_env_specific_regrets[key].append(avg)
                else:
                    result.attacker_eval_env_specific_regrets[key] = [avg]
        if eval_env_specific_opt_frac is not None:
            for key in eval_env_specific_opt_frac.keys():
                avg = np.mean(eval_env_specific_opt_frac[key])
                if key in result.attacker_eval_env_specific_opt_fracs:
                    result.attacker_eval_env_specific_opt_fracs[key].append(avg)
                else:
                    result.attacker_eval_env_specific_opt_fracs[key] = [avg]
        if train_log_dto.eval_env_specific_steps is not None:
            for key in train_log_dto.eval_env_specific_steps.keys():
                avg = np.mean(train_log_dto.eval_env_specific_steps[key])
                if key in result.eval_env_specific_steps:
                    result.eval_env_specific_steps[key].append(avg)
                else:
                    result.eval_env_specific_steps[key] = [avg]
        if train_log_dto.eval_env_specific_flags is not None:
            for key in train_log_dto.eval_env_specific_flags.keys():
                avg = np.mean(train_log_dto.eval_env_specific_flags[key])
                if key in result.eval_env_specific_flags:
                    result.eval_env_specific_flags[key].append(avg)
                else:
                    result.eval_env_specific_flags[key] = [avg]
        if train_log_dto.eval_env_specific_flags_percentage is not None:
            for key in train_log_dto.eval_env_specific_flags_percentage.keys():
                avg = np.mean(train_log_dto.eval_env_specific_flags_percentage[key])
                if key in result.eval_env_specific_flags_percentage:
                    result.eval_env_specific_flags_percentage[key].append(avg)
                else:
                    result.eval_env_specific_flags_percentage[key] = [avg]

        if train_log_dto.attacker_eval_2_env_specific_rewards is not None:
            for key in train_log_dto.attacker_eval_2_env_specific_rewards.keys():
                avg = np.mean(train_log_dto.attacker_eval_2_env_specific_rewards[key])
                if key in result.attacker_eval_2_env_specific_rewards:
                    result.attacker_eval_2_env_specific_rewards[key].append(avg)
                else:
                    result.attacker_eval_2_env_specific_rewards[key] = [avg]
        if eval_2_env_specific_regret is not None:
            for key in eval_2_env_specific_regret.keys():
                avg = np.mean(eval_2_env_specific_regret[key])
                if key in result.attacker_eval_2_env_specific_regrets:
                    result.attacker_eval_2_env_specific_regrets[key].append(avg)
                else:
                    result.attacker_eval_2_env_specific_regrets[key] = [avg]
        if eval_2_env_specific_opt_frac is not None:
            for key in eval_2_env_specific_opt_frac.keys():
                avg = np.mean(eval_2_env_specific_opt_frac[key])
                if key in result.attacker_eval_2_env_specific_opt_fracs:
                    result.attacker_eval_2_env_specific_opt_fracs[key].append(avg)
                else:
                    result.attacker_eval_2_env_specific_opt_fracs[key] = [avg]
        if train_log_dto.eval_2_env_specific_steps is not None:
            for key in train_log_dto.eval_2_env_specific_steps.keys():
                avg = np.mean(train_log_dto.eval_2_env_specific_steps[key])
                if key in result.eval_2_env_specific_steps:
                    result.eval_2_env_specific_steps[key].append(avg)
                else:
                    result.eval_2_env_specific_steps[key] = [avg]
        if train_log_dto.eval_2_env_specific_flags is not None:
            for key in train_log_dto.eval_2_env_specific_flags.keys():
                avg = np.mean(train_log_dto.eval_2_env_specific_flags[key])
                if key in result.eval_2_env_specific_flags:
                    result.eval_2_env_specific_flags[key].append(avg)
                else:
                    result.eval_2_env_specific_flags[key] = [avg]
        if train_log_dto.eval_2_env_specific_flags_percentage is not None:
            for key in train_log_dto.eval_2_env_specific_flags_percentage.keys():
                avg = np.mean(train_log_dto.eval_2_env_specific_flags_percentage[key])
                if key in result.eval_2_env_specific_flags_percentage:
                    result.eval_2_env_specific_flags_percentage[key].append(avg)
                else:
                    result.eval_2_env_specific_flags_percentage[key] = [avg]
        if isinstance(env, SubprocVecEnv):
            if not eval:
                env.reset_pi_star_rew_attacker()
        else:
            if not eval:
                env.envs[0].env_config.pi_star_rew_list_attacker = [
                    env.envs[0].env_config.pi_star_rew_attacker]

        if env_2 is not None:
            if not eval:
                if isinstance(env_2, SubprocVecEnv):
                    env_2.reset_pi_star_rew_attacker()
                else:
                    env_2.envs[0].env_config.pi_star_rew_list_attacker = [
                        env_2.envs[0].env_config.pi_star_rew_attacker]
        if not eval:
            train_log_dto.train_result = result
        else:
            train_log_dto.eval_result = result
        return train_log_dto


    @staticmethod
    def log_metrics_defender(train_log_dto: TrainAgentLogDTO, eps: float = None, eval: bool = False,
                             env=None, env_2 = None, defender_agent_config : AgentConfig = None,
                             tensorboard_writer = None, train_mode: TrainMode = TrainMode.TRAIN_ATTACKER) \
            -> TrainAgentLogDTO:
        """
        Logs average metrics for the last <self.config.log_frequency> episodes

        :param train_log_dto: DTO with the information to log
        :param eps: machine eps
        :param eval: flag whether it is evaluation or not
        :param env: the training env
        :param env_2: the eval env
        :param defender_agent_config: the agent config of the defender
        :param tensorboard_writer: the tensorboard writer
        :param train_mode: the training mode
        :return: updated train logs dto
        """
        if eps is None:
            eps = 0.0

        if not eval:
            result = train_log_dto.train_result
        else:
            result = train_log_dto.eval_result

        training_time = time.time() - train_log_dto.start_time
        training_time_hours = training_time / 3600

        avg_episode_rewards = np.mean(train_log_dto.defender_episode_rewards)
        avg_episode_steps = np.mean(train_log_dto.episode_steps)
        avg_episode_snort_severe_baseline_rewards = np.mean(train_log_dto.episode_snort_severe_baseline_rewards)
        avg_episode_snort_warning_baseline_rewards = np.mean(train_log_dto.episode_snort_warning_baseline_rewards)
        avg_episode_snort_critical_baseline_rewards = np.mean(train_log_dto.episode_snort_critical_baseline_rewards)
        avg_episode_var_log_baseline_rewards = np.mean(train_log_dto.episode_var_log_baseline_rewards)
        avg_episode_costs = np.mean(train_log_dto.attacker_action_costs)
        avg_episode_costs_norm = np.mean(train_log_dto.attacker_action_costs_norm)
        avg_episode_alerts = np.mean(train_log_dto.attacker_action_alerts)
        avg_episode_alerts_norm = np.mean(train_log_dto.attacker_action_alerts_norm)

        avg_episode_flags = np.mean(train_log_dto.episode_flags)
        avg_episode_flags_percentage = np.mean(train_log_dto.episode_flags_percentage)

        if train_log_dto.episode_caught is not None and train_log_dto.episode_early_stopped is not None \
                and train_log_dto.episode_successful_intrusion is not None:
            total_c_s_i = sum(list(map(lambda x: int(x), train_log_dto.episode_caught))) \
                          + sum(list(map(lambda x: int(x), train_log_dto.episode_early_stopped))) \
                          + sum(list(map(lambda x: int(x), train_log_dto.episode_successful_intrusion)))
        else:
            total_c_s_i = 1
        if train_log_dto.eval_episode_caught is not None and train_log_dto.eval_episode_early_stopped is not None \
                and train_log_dto.eval_episode_successful_intrusion is not None:
            eval_total_c_s_i = sum(list(map(lambda x: int(x), train_log_dto.eval_episode_caught))) \
                               + sum(list(map(lambda x: int(x), train_log_dto.eval_episode_early_stopped))) \
                               + sum(list(map(lambda x: int(x), train_log_dto.eval_episode_successful_intrusion)))
        else:
            eval_total_c_s_i = 1
        if train_log_dto.eval_2_episode_caught is not None and train_log_dto.eval_2_episode_early_stopped is not None \
                and train_log_dto.eval_2_episode_successful_intrusion is not None:
            eval_2_total_c_s_i = sum(list(map(lambda x: int(x), train_log_dto.eval_2_episode_caught))) \
                                 + sum(list(map(lambda x: int(x), train_log_dto.eval_2_episode_early_stopped))) \
                                 + sum(list(map(lambda x: int(x), train_log_dto.eval_2_episode_successful_intrusion)))
        else:
            eval_2_total_c_s_i = 1
        if train_log_dto.episode_caught is not None:
            episode_caught_frac = sum(list(map(lambda x: int(x), train_log_dto.episode_caught))) / max(1, total_c_s_i)
        else:
            episode_caught_frac = 0

        if train_log_dto.episode_early_stopped is not None:
            episode_early_stopped_frac = sum(list(map(lambda x: int(x),
                                                      train_log_dto.episode_early_stopped))) / max(1, total_c_s_i)
        else:
            episode_early_stopped_frac = 0

        if train_log_dto.episode_successful_intrusion is not None:
            episode_successful_intrusion_frac = sum(list(map(lambda x: int(x),
                                                             train_log_dto.episode_successful_intrusion))) / max(1,
                                                                                                                 total_c_s_i)
        else:
            episode_successful_intrusion_frac = 0

        if train_log_dto.eval_episode_caught is not None:
            eval_episode_caught_frac = sum(list(map(lambda x: int(x),
                                                    train_log_dto.eval_episode_caught))) / max(1, eval_total_c_s_i)
        else:
            eval_episode_caught_frac = 0

        if train_log_dto.eval_episode_successful_intrusion is not None:
            eval_episode_successful_intrusion_frac = sum(list(map(lambda x: int(x),
                                                                  train_log_dto.eval_episode_successful_intrusion))) / max(
                1, eval_total_c_s_i)
        else:
            eval_episode_successful_intrusion_frac = 0

        if train_log_dto.eval_episode_early_stopped is not None:
            eval_episode_early_stopped_frac = sum(list(map(lambda x: int(x),
                                                           train_log_dto.eval_episode_early_stopped))) / max(1,
                                                                                                             eval_total_c_s_i)
        else:
            eval_episode_early_stopped_frac = 0

        if train_log_dto.eval_2_episode_caught is not None:
            eval_2_episode_caught_frac = sum(list(map(lambda x: int(x),
                                                      train_log_dto.eval_2_episode_caught))) / max(1,
                                                                                                   eval_2_total_c_s_i)
        else:
            eval_2_episode_caught_frac = 0

        if train_log_dto.eval_2_episode_successful_intrusion is not None:
            eval_2_episode_successful_intrusion_frac = sum(list(map(lambda x: int(x),
                                                                    train_log_dto.eval_2_episode_successful_intrusion))) / max(
                1, eval_2_total_c_s_i)
        else:
            eval_2_episode_successful_intrusion_frac = 0

        if train_log_dto.eval_2_episode_early_stopped is not None:
            eval_2_episode_early_stopped_frac = sum(list(map(lambda x: int(x),
                                                             train_log_dto.eval_2_episode_early_stopped))) / max(1,
                                                                                                                 eval_2_total_c_s_i)
        else:
            eval_2_episode_early_stopped_frac = 0

        if not eval and train_log_dto.eval_episode_flags is not None:
            eval_avg_episode_flags = np.mean(train_log_dto.eval_episode_flags)
        else:
            eval_avg_episode_flags = 0.0
        if not eval and train_log_dto.eval_episode_flags_percentage is not None:
            eval_avg_episode_flags_percentage = np.mean(train_log_dto.eval_episode_flags_percentage)
        else:
            eval_avg_episode_flags_percentage = 0.0

        if not eval and train_log_dto.eval_2_episode_flags is not None:
            eval_2_avg_episode_flags = np.mean(train_log_dto.eval_2_episode_flags)
        else:
            eval_2_avg_episode_flags = 0.0
        if not eval and train_log_dto.eval_2_episode_flags_percentage is not None:
            eval_2_avg_episode_flags_percentage = np.mean(train_log_dto.eval_2_episode_flags_percentage)
        else:
            eval_2_avg_episode_flags_percentage = 0.0

        if not eval and train_log_dto.eval_episode_steps is not None:
            eval_avg_episode_steps = np.mean(train_log_dto.eval_episode_steps)
        else:
            eval_avg_episode_steps = 0.0

        if not eval and train_log_dto.eval_attacker_action_costs is not None:
            eval_avg_episode_costs = np.mean(train_log_dto.eval_attacker_action_costs)
        else:
            eval_avg_episode_costs = 0.0

        if not eval and train_log_dto.eval_attacker_action_costs_norm is not None:
            eval_avg_episode_costs_norm = np.mean(train_log_dto.eval_attacker_action_costs_norm)
        else:
            eval_avg_episode_costs_norm = 0.0

        if not eval and train_log_dto.eval_attacker_action_alerts is not None:
            eval_avg_episode_alerts = np.mean(train_log_dto.eval_attacker_action_alerts)
        else:
            eval_avg_episode_alerts = 0.0

        if not eval and train_log_dto.eval_attacker_action_alerts_norm is not None:
            eval_avg_episode_alerts_norm = np.mean(train_log_dto.eval_attacker_action_alerts_norm)
        else:
            eval_avg_episode_alerts_norm = 0.0

        if not eval and train_log_dto.defender_eval_2_episode_rewards is not None:
            eval_2_avg_episode_rewards = np.mean(train_log_dto.defender_eval_2_episode_rewards)
        else:
            eval_2_avg_episode_rewards = 0.0

        if not eval and train_log_dto.eval_2_episode_snort_severe_baseline_rewards is not None:
            eval_2_avg_episode_snort_severe_baseline_rewards = np.mean(
                train_log_dto.eval_2_episode_snort_severe_baseline_rewards)
        else:
            eval_2_avg_episode_snort_severe_baseline_rewards = 0.0

        if not eval and train_log_dto.eval_2_episode_snort_warning_baseline_rewards is not None:
            eval_2_avg_episode_snort_warning_baseline_rewards = np.mean(
                train_log_dto.eval_2_episode_snort_warning_baseline_rewards)
        else:
            eval_2_avg_episode_snort_warning_baseline_rewards = 0.0

        if not eval and train_log_dto.eval_2_episode_snort_critical_baseline_rewards is not None:
            eval_2_avg_episode_snort_critical_baseline_rewards = np.mean(
                train_log_dto.eval_2_episode_snort_critical_baseline_rewards)
        else:
            eval_2_avg_episode_snort_critical_baseline_rewards = 0.0

        if not eval and train_log_dto.eval_2_episode_var_log_baseline_rewards is not None:
            eval_2_avg_episode_var_log_baseline_rewards = np.mean(train_log_dto.eval_2_episode_var_log_baseline_rewards)
        else:
            eval_2_avg_episode_var_log_baseline_rewards = 0.0

        if not eval and train_log_dto.eval_2_episode_steps is not None:
            eval_2_avg_episode_steps = np.mean(train_log_dto.eval_2_episode_steps)
        else:
            eval_2_avg_episode_steps = 0.0

        if not eval and train_log_dto.eval_2_attacker_action_costs is not None:
            eval_2_avg_episode_costs = np.mean(train_log_dto.eval_2_attacker_action_costs)
        else:
            eval_2_avg_episode_costs = 0.0
        if not eval and train_log_dto.eval_2_attacker_action_costs_norm is not None:
            eval_2_avg_episode_costs_norm = np.mean(train_log_dto.eval_2_attacker_action_costs_norm)
        else:
            eval_2_avg_episode_costs_norm = 0.0
        if not eval and train_log_dto.eval_2_attacker_action_alerts is not None:
            eval_2_avg_episode_alerts = np.mean(train_log_dto.eval_2_attacker_action_alerts)
        else:
            eval_2_avg_episode_alerts = 0.0
        if not eval and train_log_dto.eval_2_attacker_action_alerts_norm is not None:
            eval_2_avg_episode_alerts_norm = np.mean(train_log_dto.eval_2_attacker_action_alerts_norm)
        else:
            eval_2_avg_episode_alerts_norm = 0.0

        if train_log_dto.rollout_times is not None:
            if len(train_log_dto.rollout_times) > 0:
                avg_rollout_times = np.mean(train_log_dto.rollout_times)
            else:
                avg_rollout_times = 0.0
        else:
            avg_rollout_times = 0.0
        if train_log_dto.env_response_times is not None and len(train_log_dto.env_response_times) > 0:
            if len(train_log_dto.env_response_times) > 0:
                avg_env_response_times = np.mean(train_log_dto.env_response_times)
            else:
                avg_env_response_times = 0.0
        else:
            avg_env_response_times = 0.0
        if train_log_dto.action_pred_times is not None and len(train_log_dto.action_pred_times) > 0:
            if len(train_log_dto.action_pred_times) > 0:
                avg_action_pred_times = np.mean(train_log_dto.action_pred_times)
            else:
                avg_action_pred_times = 0.0
        else:
            avg_action_pred_times = 0.0
        if train_log_dto.grad_comp_times is not None and len(train_log_dto.grad_comp_times) > 0:
            if len(train_log_dto.grad_comp_times) > 0:
                avg_grad_comp_times = np.mean(train_log_dto.grad_comp_times)
            else:
                avg_grad_comp_times = 0.0
        else:
            avg_grad_comp_times = 0.0
        if train_log_dto.weight_update_times is not None and len(train_log_dto.weight_update_times) > 0:
            if len(train_log_dto.weight_update_times):
                avg_weight_update_times = np.mean(train_log_dto.weight_update_times)
            else:
                avg_weight_update_times = 0.0
        else:
            avg_weight_update_times = 0.0

        if result.defender_avg_episode_rewards is not None:
            rolling_avg_rewards = pycr_util.running_average(result.defender_avg_episode_rewards + [avg_episode_rewards],
                                                            defender_agent_config.running_avg)
        else:
            rolling_avg_rewards = 0.0

        if result.avg_episode_steps is not None:
            rolling_avg_steps = pycr_util.running_average(result.avg_episode_steps + [avg_episode_steps],
                                                          defender_agent_config.running_avg)
        else:
            rolling_avg_steps = 0.0

        if train_log_dto.defender_lr is None:
            lr = 0.0
        else:
            lr = train_log_dto.defender_lr
        if not eval and train_log_dto.defender_episode_avg_loss is not None:
            avg_episode_loss = np.mean(train_log_dto.defender_episode_avg_loss)
        else:
            avg_episode_loss = 0.0

        if not eval and train_log_dto.defender_eval_episode_rewards is not None:
            eval_avg_episode_rewards = np.mean(train_log_dto.defender_eval_episode_rewards)
        else:
            eval_avg_episode_rewards = 0.0

        if not eval and train_log_dto.eval_episode_snort_severe_baseline_rewards is not None:
            eval_avg_episode_snort_severe_baseline_rewards = np.mean(
                train_log_dto.eval_episode_snort_severe_baseline_rewards)
        else:
            eval_avg_episode_snort_severe_baseline_rewards = 0.0

        if not eval and train_log_dto.eval_episode_snort_warning_baseline_rewards is not None:
            eval_avg_episode_snort_warning_baseline_rewards = np.mean(
                train_log_dto.eval_episode_snort_warning_baseline_rewards)
        else:
            eval_avg_episode_snort_warning_baseline_rewards = 0.0

        if not eval and train_log_dto.eval_episode_snort_critical_baseline_rewards is not None:
            eval_avg_episode_snort_critical_baseline_rewards = np.mean(
                train_log_dto.eval_episode_snort_critical_baseline_rewards)
        else:
            eval_avg_episode_snort_critical_baseline_rewards = 0.0

        if not eval and train_log_dto.eval_episode_var_log_baseline_rewards is not None:
            eval_avg_episode_var_log_baseline_rewards = np.mean(
                train_log_dto.eval_episode_var_log_baseline_rewards)
        else:
            eval_avg_episode_var_log_baseline_rewards = 0.0

        # Regret & Pi* Metrics
        if defender_agent_config.log_regret:

            # Regret
            if env.env_config is not None:
                avg_regret = LogUtil.compute_regret(opt_r=env.envs[0].env_config.pi_star_rew_defender,
                                                    r=avg_episode_rewards)
            else:
                avg_regret = 0.0

            if train_log_dto.defender_eval_episode_rewards is not None \
                    and train_log_dto.defender_eval_env_specific_rewards != {}:
                avg_eval_regret = LogUtil.compute_regret(opt_r=env.envs[0].env_config.pi_star_rew_defender,
                                                         r=eval_avg_episode_rewards)
            else:
                avg_eval_regret = 0.0

            if train_log_dto.defender_eval_2_episode_rewards is not None \
                    and train_log_dto.defender_eval_2_env_specific_rewards != {}:
                avg_eval_2_regret = LogUtil.compute_regret(opt_r=env.envs[0].env_config.pi_star_rew_defender,
                                                         r=eval_2_avg_episode_rewards)
            else:
                avg_eval_2_regret = 0.0

            # Opt frac
            if env.env_config is not None:
                avg_opt_frac = LogUtil.compute_opt_frac(r=avg_episode_rewards,
                                                        opt_r=env.envs[0].env_config.pi_star_rew_defender)
            else:
                avg_opt_frac = 0.0

            if train_log_dto.defender_eval_episode_rewards is not None:
                eval_avg_opt_frac = eval_avg_episode_rewards / env.envs[0].env_config.pi_star_rew_defender
            else:
                eval_avg_opt_frac = 0.0

            if train_log_dto.defender_eval_2_episode_rewards is not None:
                eval_2_avg_opt_frac = eval_2_avg_episode_rewards / env.envs[0].env_config.pi_star_rew_defender
            else:
                eval_2_avg_opt_frac = 0.0

            # if self.env_2 is not None:
            #     if self.env_2.env_config is not None:

        tensorboard_data_dto = TensorboardDataDTO(
            iteration=train_log_dto.iteration, avg_episode_rewards=avg_episode_rewards,
            avg_episode_steps=avg_episode_steps,
            avg_episode_loss=avg_episode_loss, eps=eps, lr=lr, eval=eval,
            eval_avg_episode_rewards=eval_avg_episode_rewards, eval_avg_episode_steps=eval_avg_episode_steps,
            eval_2_avg_episode_rewards=eval_2_avg_episode_rewards,
            eval_2_avg_episode_steps=eval_2_avg_episode_steps,
            rolling_avg_episode_rewards=rolling_avg_rewards,
            rolling_avg_episode_steps=rolling_avg_steps,
            tensorboard_writer=tensorboard_writer,
            episode_caught_frac=episode_caught_frac,
            episode_early_stopped_frac=episode_early_stopped_frac,
            episode_successful_intrusion_frac=episode_successful_intrusion_frac,
            eval_episode_caught_frac=eval_episode_caught_frac,
            eval_episode_early_stopped_frac=eval_episode_early_stopped_frac,
            eval_episode_successful_intrusion_frac=eval_episode_successful_intrusion_frac,
            eval_2_episode_caught_frac=eval_2_episode_caught_frac,
            eval_2_episode_early_stopped_frac=eval_2_episode_early_stopped_frac,
            eval_2_episode_successful_intrusion_frac=eval_2_episode_successful_intrusion_frac,
            avg_regret=avg_regret, avg_opt_frac=avg_opt_frac, rolling_avg_rewards=rolling_avg_rewards,
            rolling_avg_steps=rolling_avg_steps,
            n_af=train_log_dto.n_af, n_d=train_log_dto.n_d, avg_episode_costs=avg_episode_costs,
            avg_episode_costs_norm=avg_episode_costs_norm,
            avg_episode_alerts=avg_episode_alerts, avg_episode_alerts_norm=avg_episode_alerts_norm,
            eval_avg_episode_costs=eval_avg_episode_costs, eval_avg_episode_costs_norm=eval_avg_episode_costs_norm,
            eval_avg_episode_alerts=eval_avg_episode_alerts, eval_avg_episode_alerts_norm=eval_avg_episode_alerts_norm,
            eval_2_avg_episode_costs=eval_2_avg_episode_costs,
            eval_2_avg_episode_costs_norm=eval_2_avg_episode_costs_norm,
            eval_2_avg_episode_alerts=eval_2_avg_episode_alerts,
            eval_2_avg_episode_alerts_norm=eval_2_avg_episode_alerts_norm,
            total_num_episodes=train_log_dto.total_num_episodes, avg_eval_regret=avg_eval_regret,
            eval_avg_opt_frac=eval_avg_opt_frac,
            epsilon=defender_agent_config.epsilon, training_time_hours=training_time_hours,
            avg_episode_snort_severe_baseline_rewards=avg_episode_snort_severe_baseline_rewards,
            avg_episode_snort_warning_baseline_rewards=avg_episode_snort_warning_baseline_rewards,
            eval_avg_episode_snort_severe_baseline_rewards=eval_avg_episode_snort_severe_baseline_rewards,
            eval_avg_episode_snort_warning_baseline_rewards=eval_avg_episode_snort_warning_baseline_rewards,
            eval_avg_2_episode_snort_severe_baseline_rewards=eval_2_avg_episode_snort_severe_baseline_rewards,
            eval_avg_2_episode_snort_warning_baseline_rewards=eval_2_avg_episode_snort_warning_baseline_rewards,
            avg_episode_snort_critical_baseline_rewards=avg_episode_snort_critical_baseline_rewards,
            avg_episode_var_log_baseline_rewards=avg_episode_var_log_baseline_rewards,
            eval_avg_episode_snort_critical_baseline_rewards=eval_avg_episode_snort_critical_baseline_rewards,
            eval_avg_episode_var_log_baseline_rewards=eval_avg_episode_var_log_baseline_rewards,
            eval_avg_2_episode_snort_critical_baseline_rewards=eval_2_avg_episode_snort_critical_baseline_rewards,
            eval_avg_2_episode_var_log_baseline_rewards=eval_2_avg_episode_var_log_baseline_rewards,
            avg_flags_catched=avg_episode_flags, avg_episode_flags_percentage=avg_episode_flags_percentage,
            eval_avg_episode_flags=eval_avg_episode_flags,
            eval_avg_episode_flags_percentage=eval_avg_episode_flags_percentage,
            eval_2_avg_episode_flags=eval_2_avg_episode_flags,
            eval_2_avg_episode_flags_percentage=eval_2_avg_episode_flags_percentage
        )
        log_str = tensorboard_data_dto.log_str_defender()
        defender_agent_config.logger.info(log_str)
        print(log_str)
        sys.stdout.flush()
        if defender_agent_config.tensorboard:
            tensorboard_data_dto.log_tensorboard_defender()

        # Defender specific metrics
        result.defender_avg_episode_rewards.append(avg_episode_rewards)
        result.defender_avg_episode_loss.append(avg_episode_loss)
        result.defender_eval_avg_episode_rewards.append(eval_avg_episode_rewards)
        result.defender_eval_2_avg_episode_rewards.append(eval_2_avg_episode_rewards)
        result.defender_avg_regret.append(avg_regret)
        result.defender_avg_opt_frac.append(avg_opt_frac)
        result.defender_eval_avg_regret.append(avg_eval_regret)
        result.defender_eval_avg_opt_frac.append(eval_avg_opt_frac)
        result.snort_severe_baseline_rewards.append(avg_episode_snort_severe_baseline_rewards)
        result.snort_warning_baseline_rewards.append(avg_episode_snort_warning_baseline_rewards)
        result.eval_snort_severe_baseline_rewards.append(eval_avg_episode_snort_severe_baseline_rewards)
        result.eval_snort_warning_baseline_rewards.append(eval_avg_episode_snort_warning_baseline_rewards)
        result.eval_2_snort_severe_baseline_rewards.append(eval_2_avg_episode_snort_severe_baseline_rewards)
        result.eval_2_snort_warning_baseline_rewards.append(eval_2_avg_episode_snort_warning_baseline_rewards)
        result.snort_critical_baseline_rewards.append(avg_episode_snort_critical_baseline_rewards)
        result.var_log_baseline_rewards.append(avg_episode_var_log_baseline_rewards)
        result.eval_snort_critical_baseline_rewards.append(eval_avg_episode_snort_critical_baseline_rewards)
        result.eval_var_log_baseline_rewards.append(eval_avg_episode_var_log_baseline_rewards)
        result.eval_2_snort_critical_baseline_rewards.append(eval_2_avg_episode_snort_critical_baseline_rewards)
        result.eval_2_var_log_baseline_rewards.append(eval_2_avg_episode_var_log_baseline_rewards)
        result.defender_eval_2_avg_regret.append(avg_eval_2_regret)
        result.defender_eval_2_avg_opt_frac.append(eval_2_avg_opt_frac)

        if train_log_dto.defender_train_episode_env_specific_rewards is not None:
            for key in train_log_dto.defender_train_episode_env_specific_rewards.keys():
                avg = np.mean(train_log_dto.defender_train_episode_env_specific_rewards[key])
                if key in result.defender_train_env_specific_rewards:
                    result.defender_train_env_specific_rewards[key].append(avg)
                else:
                    result.defender_train_env_specific_rewards[key] = [avg]

        if train_log_dto.defender_eval_env_specific_rewards is not None:
            for key in train_log_dto.defender_eval_env_specific_rewards.keys():
                avg = np.mean(train_log_dto.defender_eval_env_specific_rewards[key])
                if key in result.defender_eval_env_specific_rewards:
                    result.defender_eval_env_specific_rewards[key].append(avg)
                else:
                    result.defender_eval_env_specific_rewards[key] = [avg]

        if train_log_dto.defender_eval_2_env_specific_rewards is not None:
            for key in train_log_dto.defender_eval_2_env_specific_rewards.keys():
                avg = np.mean(train_log_dto.defender_eval_2_env_specific_rewards[key])
                if key in result.defender_eval_2_env_specific_rewards:
                    result.defender_eval_2_env_specific_rewards[key].append(avg)
                else:
                    result.defender_eval_2_env_specific_rewards[key] = [avg]

        # General metrics
        if not train_mode == TrainMode.SELF_PLAY:
            result.avg_episode_steps.append(avg_episode_steps)
            result.epsilon_values.append(defender_agent_config.epsilon)
            result.eval_avg_episode_steps.append(eval_avg_episode_steps)
            result.eval_2_avg_episode_steps.append(eval_2_avg_episode_steps)
            result.lr_list.append(train_log_dto.defender_lr)
            result.rollout_times.append(avg_rollout_times)
            result.env_response_times.append(avg_env_response_times)
            result.action_pred_times.append(avg_action_pred_times)
            result.grad_comp_times.append(avg_grad_comp_times)
            result.weight_update_times.append(avg_weight_update_times)
            result.caught_frac.append(episode_caught_frac)
            result.early_stopping_frac.append(episode_early_stopped_frac)
            result.intrusion_frac.append(episode_successful_intrusion_frac)
            result.eval_caught_frac.append(eval_episode_caught_frac)
            result.eval_early_stopping_frac.append(eval_episode_early_stopped_frac)
            result.eval_intrusion_frac.append(eval_episode_successful_intrusion_frac)
            result.eval_2_caught_frac.append(eval_2_episode_caught_frac)
            result.eval_2_early_stopping_frac.append(eval_2_episode_early_stopped_frac)
            result.eval_2_intrusion_frac.append(eval_2_episode_successful_intrusion_frac)
            result.attacker_action_costs.append(avg_episode_costs)
            result.attacker_action_costs_norm.append(avg_episode_costs_norm)
            result.attacker_action_alerts.append(avg_episode_alerts)
            result.attacker_action_alerts_norm.append(avg_episode_alerts_norm)
            result.eval_attacker_action_costs.append(eval_avg_episode_costs)
            result.eval_attacker_action_costs_norm.append(eval_avg_episode_costs_norm)
            result.eval_attacker_action_alerts.append(eval_avg_episode_alerts)
            result.eval_attacker_action_alerts_norm.append(eval_avg_episode_alerts_norm)
            result.eval_2_attacker_action_costs.append(eval_2_avg_episode_costs)
            result.eval_2_attacker_action_costs_norm.append(eval_2_avg_episode_costs_norm)
            result.eval_2_attacker_action_alerts.append(eval_2_avg_episode_alerts)
            result.eval_2_attacker_action_alerts_norm.append(eval_2_avg_episode_alerts_norm)
            result.avg_episode_flags.append(avg_episode_flags)
            result.avg_episode_flags_percentage.append(avg_episode_flags_percentage)
            result.eval_avg_episode_flags.append(eval_avg_episode_flags)
            result.eval_avg_episode_flags_percentage.append(eval_avg_episode_flags_percentage)
            result.eval_2_avg_episode_flags.append(eval_2_avg_episode_flags)
            result.eval_2_avg_episode_flags_percentage.append(eval_2_avg_episode_flags_percentage)


            if train_log_dto.train_env_specific_steps is not None:
                for key in train_log_dto.train_env_specific_steps.keys():
                    avg = np.mean(train_log_dto.train_env_specific_steps[key])
                    if key in result.train_env_specific_steps:
                        result.train_env_specific_steps[key].append(avg)
                    else:
                        result.train_env_specific_steps[key] = [avg]
            if train_log_dto.eval_env_specific_steps is not None:
                for key in train_log_dto.eval_env_specific_steps.keys():
                    avg = np.mean(train_log_dto.eval_env_specific_steps[key])
                    if key in result.eval_env_specific_steps:
                        result.eval_env_specific_steps[key].append(avg)
                    else:
                        result.eval_env_specific_steps[key] = [avg]
            if train_log_dto.eval_2_env_specific_steps is not None:
                for key in train_log_dto.eval_2_env_specific_steps.keys():
                    avg = np.mean(train_log_dto.eval_2_env_specific_steps[key])
                    if key in result.eval_2_env_specific_steps:
                        result.eval_2_env_specific_steps[key].append(avg)
                    else:
                        result.eval_2_env_specific_steps[key] = [avg]
            if not eval:
                train_log_dto.train_result = result
            else:
                train_log_dto.eval_result = result
            return train_log_dto

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
            return r/opt_r
        elif r < 0 and opt_r > 0:
            return 1/abs_difference
        else:
            return 1/abs_difference

    @staticmethod
    def compute_regret(r: float, opt_r : float) -> float:
        """
        Utility function for computing the regret

        :param r: the reward
        :param opt_r: the optimal reward
        :return: the regret
        """
        return abs(opt_r - r)
