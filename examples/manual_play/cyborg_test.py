import inspect
from csle_cyborg.main import Main
from csle_cyborg.agents.simple_agents.b_line import B_lineAgent
from csle_cyborg.agents.wrappers.challenge_wrapper import ChallengeWrapper

if __name__ == '__main__':
    cyborg_scenario_config_path = str(inspect.getfile(Main))
    cyborg_scenario_config_path = cyborg_scenario_config_path[:-7] + '/shared/scenarios/Scenario2.yaml'
    cyborg = Main(cyborg_scenario_config_path, 'sim', agents={
        'Red': B_lineAgent
    })
    # env = BlueTableWrapper(env=cyborg)
    env = ChallengeWrapper(env=cyborg, agent_name="Blue")
    env.reset()
    # results = env.reset(agent='Blue')
    # print(results.observation)
    print(env)
    print(env)
    print(env.env)
    print(env.env.env)
    print(env.env.env.env)
    print(env.env.env.env.env)
    print(env.env.env.env.env.env)
    # print(env.env.env.env.env.env.environment_controller)
    # print(env.env.env.env.env.env.environment_controller.agent_interfaces)
    # print(env.env.env.env.env.env.environment_controller.agent_interfaces["Blue"])
    # print(env.env.env.env.env.env.environment_controller.agent_interfaces["Blue"].actions)
    # print(env.env.env.env.env.env.environment_controller.agent_interfaces["Blue"].action_space)
    # print(env.env.env.env.env.env.environment_controller.agent_interfaces["Blue"].action_space.get_action_space())
    # print(env.env.env.env.env.env.get_action_space(agent="Blue"))
    # print(env.env.env.env.env.get_action_space(agent="Blue"))
    # print(env.env.env.env.get_action_space(agent="Blue"))
    # print(env.env.env.get_action_space(agent="Blue"))
    # print(env.env.env)
    # actions = list(map(lambda x: str(x), env.env.env.possible_actions))
    # print(actions)
    # print(env.env.possible_actions)
    # print(env.possible_actions)
    # print(list(env.env.env.env.info.keys()))
    # actions = list(map(lambda x: str(x), env.possible_actions))
    # for i in range(len(actions)):
    #     print(f"{i}, {actions[i]}")
    # print(env.get_observation(agent="Blue"))
    # print(env.env.env.env.get_table())
    # print(env.observation_space)
    # o, r, done, _, info = env.step(1)
    # print(o)
    # print(len(o))
    # print(52 / 13)
    #
    # config = CSLECyborgConfig(
    #     gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=RedAgentType.B_LINE_AGENT,
    #     maximum_steps=100)
    # csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    # o, r, done, _, info = csle_cyborg_env.step(0)
    # print(info)
    # print(len(o))
    # print(csle_cyborg_env.cyborg_actions)
    # print(csle_cyborg_env.cyborg_hostnames)
    # print(env.env.env.env.info)
    # print(env.env.env.env.info)
    # o, r, done, _, info = env.step(1)
    # print(env.action_space)
    # print(env.observation_space)
