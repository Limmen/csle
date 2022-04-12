from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_agents.ppo.ppo_agent import PPOAgent

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation("csle-level9-001")
    simulation_env_config = MetastoreFacade.get_simulation("csle-stopping-pomdp-defender-001")
    experiment_config = ExperimentConfig(
        output_dir="/tmp/ppo_test", title="PPO test", random_seeds=[399, 98912], agent_type=AgentType.PPO,
        log_every=1,
        hparams={
            "num_neurons_per_hidden_layer": HParam(value=64, name="num_neurons_per_hidden_layer",
                                                   descr="neurons per hidden layer of the policy network"),
            "num_hidden_layers": HParam(value=4, name="num_neurons_per_hidden_layer",
                                        descr="number of layers of the policy network"),
            "steps_between_updates": HParam(value=4096, name="steps_between_updates",
                                            descr="number of steps in the environment for doing "
                                                  "rollouts between policy updates"),
            "batch_size": HParam(value=64, name="batch_size", descr="batch size for updates"),
            "learning_rate": HParam(value=0.0001, name="learning_rate", descr="learning rate for updating the policy"),
            "device": HParam(value="cpu", name="device", descr="the device to train on (cpu or cuda:x)"),
            "gamma": HParam(value=1, name="gamma", descr="the discount factor"),
            "gae_lambda": HParam(value=0.95, name="gae_lambda", descr="the GAE weighting term"),
            "clip_range": HParam(value=0.2, name="clip_range", descr="the clip range for PPO"),
            "clip_range_vf": HParam(value=None, name="clip_range_vf", descr="the clip range for PPO-update of the "
                                                                            "value network"),
            "ent_coef": HParam(value=0.0, name="ent_coef", descr="the entropy coefficient for exploration"),
            "vf_coef": HParam(value=0.5, name="vf_coef", descr="the coefficient of the value network for the loss"),
            "max_grad_norm": HParam(value=0.5, name="max_grad_norm", descr="the maximum allows gradient norm"),
            "target_kl": HParam(value=None, name="target_kl", descr="the target kl"),
            "num_training_timesteps": HParam(value=int(100000), name="num_training_timesteps", descr="number "
                                                                                              "of timesteps to train"),
            "eval_every": HParam(value=10, name="eval_every",
                                 descr="training iterations between evaluations"),
            "eval_batch_size": HParam(value=10, name="eval_batch_size",
                                 descr="the batch size for evaluation")
        }
    )
    # simulation_env_config.simulation_env_input_config
    agent = PPOAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                       experiment_config=experiment_config)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_ppo_policy(ppo_policy=policy)
