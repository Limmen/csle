from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv
from gym_csle_ctf.envs_model.config.multi_sim.csle_ctf_multisim_base import CSLECTFMultiSimBase
from gym_csle_ctf.envs_model.config.multi_sim.csle_ctf_multisim_v1 import CSLECTFMultiSimV1
from gym_csle_ctf.envs_model.logic.common.domain_randomization.csle_ctf_domain_randomizer import CSLECTFCSLEDomainRandomizer


# -------- Version 1 emulation ------------
class CSLECTFMultiSim1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 idx: int = -1, dr_max_num_nodes : int = 10, dr_min_num_nodes : int  = 4, dr_max_num_flags = 3,
                 dr_min_num_flags : int = 1, dr_min_num_users :int = 2, dr_max_num_users : int = 5):
        if env_config is None:
            render_config = CSLECTFMultiSimBase.render_conf(num_nodes=dr_max_num_nodes)
            randomization_space = CSLECTFCSLEDomainRandomizer.generate_randomization_space(
                [], max_num_nodes=dr_max_num_nodes,
                min_num_nodes=dr_min_num_nodes, max_num_flags=dr_max_num_flags,
                min_num_flags=dr_min_num_flags, min_num_users=dr_min_num_users,
                max_num_users=dr_max_num_users,
                use_base_randomization=True)
            self.randomization_space = randomization_space
            attacker_action_conf = CSLECTFMultiSimV1.attacker_actions_conf(num_nodes=dr_max_num_nodes - 1,
                                                                           subnet_mask=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}2{constants.CSLE.CSLE_SUBNETMASK_SUFFIX}",
                                                                           hacker_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}2.191")
            defender_action_conf = CSLECTFMultiSimV1.defender_actions_conf(
                num_nodes=dr_max_num_nodes - 1, subnet_mask=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}2{constants.CSLE.CSLE_SUBNETMASK_SUFFIX}")
            env_config = CSLECTFMultiSimV1.env_config(attacker_action_conf=attacker_action_conf,
                                                      defender_action_conf=defender_action_conf,
                                                      emulation_config=emulation_config, render_conf=render_config,
                                                      num_nodes=dr_max_num_nodes-1)
            env_config.domain_randomization = True
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.SIMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.idx=idx
            env_config.attacker_filter_illegal_actions = True
            env_config.max_episode_length = 200
            env_config.compute_pi_star_attacker = True
            env_config.use_upper_bound_pi_star_attacker = True
            randomized_network_conf, env_config = CSLECTFCSLEDomainRandomizer.randomize(subnet_prefix=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}",
                                                                                        network_ids=list(range(1, 254)),
                                                                                        r_space=self.randomization_space,
                                                                                        env_config=env_config)
        super(CSLECTFMultiSim1Env, self).__init__(env_config=env_config, rs=randomization_space)