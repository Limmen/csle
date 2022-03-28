from typing import Tuple
from csle_common.dao.network.emulation_env_state import EmulationEnvState
from csle_common.dao.network.emulation_env_agent_config import EmulationEnvAgentConfig
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.defender.defender_action import DefenderAction
from csle_common.dao.action.defender.defender_action_type import DefenderActionType
from csle_defender.emulation.defender_stopping_middleware import DefenderStoppingMiddleware
from csle_common.dao.action.defender.defender_action_id import DefenderActionId
from csle_defender.emulation.defender_update_state_middleware import DefenderUpdateStateMiddleware


class EmulatedDefender:
    """
    Represents an emulated defender agent
    """

    @staticmethod
    def defender_transition(s: EmulationEnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                            env_config: EmulationEnvAgentConfig) -> EmulationEnvState:
        """
        Implements the transition operator T: (s,a) -> s'

        :param s: the current state
        :param defender_action: the defender action
        :param attacker_action: the previous action of the attacker
        :param env_config: the environment configuration
        :return: s'
        """
        if defender_action.type == DefenderActionType.STOP or defender_action.type == DefenderActionType.CONTINUE:
            return EmulatedDefender.defender_stopping_action(s=s, defender_action=defender_action,
                                                                attacker_action=attacker_action,
                                                                env_config=env_config)
        if defender_action.type == DefenderActionType.STATE_UPDATE:
            return EmulatedDefender.defender_update_state_action(s=s, defender_action=defender_action,
                                                                    env_config=env_config,
                                                                    attacker_action=attacker_action)
        else:
            raise ValueError("Action type not recognized")


    @staticmethod
    def defender_stopping_action(s: EmulationEnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                                 env_config: EmulationEnvAgentConfig) -> EmulationEnvState:
        """
        Implements transition of a stopping action of the defender

        :param s: the current state
        :param defender_action: the defender's action
        :param attacker_action: the previous action of the attacker
        :param env_config: the environment configuration
        :return: s'
        """
        if defender_action.id == DefenderActionId.STOP:
            return DefenderStoppingMiddleware.stop_monitor(s=s, defender_action=defender_action,
                                                           attacker_action=attacker_action,
                                                           env_config=env_config)
        elif defender_action.id == DefenderActionId.CONTINUE:
            return DefenderStoppingMiddleware.continue_monitor(s=s, defender_action=defender_action,
                                                               attacker_action=attacker_action,
                                                               env_config=env_config)
        else:
            raise ValueError("Stopping action id:{},name:{} not recognized".format(defender_action.id, defender_action.name))


    @staticmethod
    def defender_update_state_action(s: EmulationEnvState, defender_action: DefenderAction, env_config: EmulationEnvAgentConfig,
                                     attacker_action: AttackerAction) -> EmulationEnvState:
        """
        Implements transition of state update for the defender

        :param s: the current state
        :param defender_action: the action
        :param attacker_action: the attacker's previous action
        :param env_config: the environment configuration
        :return: s'
        """
        if defender_action.id == DefenderActionId.UPDATE_STATE:
            return DefenderUpdateStateMiddleware.update_belief_state(
                s=s, defender_action=defender_action, env_config=env_config, attacker_action=attacker_action)
        elif defender_action.id == DefenderActionId.INITIALIZE_STATE:
            return DefenderUpdateStateMiddleware.initialize_state(
                s=s, defender_action=defender_action, env_config=env_config, attacker_action=attacker_action)
        elif defender_action.id == DefenderActionId.RESET_STATE:
            return DefenderUpdateStateMiddleware.reset_state(
                s=s, defender_action=defender_action, env_config=env_config, attacker_action=attacker_action)
        else:
            raise ValueError("State update action id:{},name:{} not recognized".format(defender_action.id,
                                                                                       defender_action.name))