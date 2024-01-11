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
    env = ChallengeWrapper(env=cyborg, agent_name='Blue')
    o, _ = env.reset()
    print(o)
    o, r, done, _, info = env.step(1)
    print(env.action_space)
    print(env.observation_space)