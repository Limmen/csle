from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_defender.emulation.defender_stopping_middleware import DefenderStoppingMiddleware
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_defender.emulation.defender_update_state_middleware import DefenderUpdateStateMiddleware


class EmulatedDefender:
    """
    Represents an emulated defender agent
    """

    @staticmethod
    def defender_transition(s: EmulationEnvState, defender_action: EmulationDefenderAction, attacker_action: EmulationAttackerAction,
                            emulation_env_config: EmulationEnvConfig) -> EmulationEnvState:
        """
        Implements the transition operator T: (s,a) -> s'

        :param s: the current state
        :param defender_action: the defender action
        :param attacker_action: the previous action of the attacker
        :param emulation_env_config: the emulation environment configuration
        :return: s'
        """
        if defender_action.type == EmulationDefenderActionType.STOP or defender_action.type == EmulationDefenderActionType.CONTINUE:
            return EmulatedDefender.defender_stopping_action(s=s, defender_action=defender_action,
                                                             attacker_action=attacker_action,
                                                             emulation_env_config=emulation_env_config)
        if defender_action.type == EmulationDefenderActionType.STATE_UPDATE:
            return EmulatedDefender.defender_update_state_action(s=s, defender_action=defender_action,
                                                                 emulation_env_config=emulation_env_config,
                                                                 attacker_action=attacker_action)
        else:
            raise ValueError("Action type not recognized")


    @staticmethod
    def defender_stopping_action(s: EmulationEnvState, defender_action: EmulationDefenderAction, attacker_action: EmulationAttackerAction,
                                 emulation_env_config: EmulationEnvConfig) -> EmulationEnvState:
        """
        Implements transition of a stopping action of the defender

        :param s: the current state
        :param defender_action: the defender's action
        :param attacker_action: the previous action of the attacker
        :param emulation_env_config: the emulation environment configuration
        :return: s'
        """
        if defender_action.id == EmulationDefenderActionId.STOP:
            return DefenderStoppingMiddleware.stop_monitor(s=s, defender_action=defender_action,
                                                           attacker_action=attacker_action,
                                                           emulation_env_config=emulation_env_config)
        elif defender_action.id == EmulationDefenderActionId.CONTINUE:
            return DefenderStoppingMiddleware.continue_monitor(s=s, defender_action=defender_action,
                                                               attacker_action=attacker_action,
                                                               emulation_env_config=emulation_env_config)
        else:
            raise ValueError("Stopping action id:{},name:{} not recognized".format(defender_action.id, defender_action.name))


    @staticmethod
    def defender_update_state_action(s: EmulationEnvState, defender_action: EmulationDefenderAction,
                                     emulation_env_config: EmulationEnvConfig,
                                     attacker_action: EmulationAttackerAction) -> EmulationEnvState:
        """
        Implements transition of state update for the defender

        :param s: the current state
        :param defender_action: the action
        :param attacker_action: the attacker's previous action
        :param emulation_env_config: the emulation environment configuration
        :return: s'
        """
        if defender_action.id == EmulationDefenderActionId.UPDATE_STATE:
            return DefenderUpdateStateMiddleware.update_belief_state(
                s=s, defender_action=defender_action, emulation_env_config=emulation_env_config,
                attacker_action=attacker_action)
        elif defender_action.id == EmulationDefenderActionId.INITIALIZE_STATE:
            return DefenderUpdateStateMiddleware.initialize_state(
                s=s, defender_action=defender_action, emulation_env_config=emulation_env_config,
                attacker_action=attacker_action)
        elif defender_action.id == EmulationDefenderActionId.RESET_STATE:
            return DefenderUpdateStateMiddleware.reset_state(
                s=s, defender_action=defender_action, emulation_env_config=emulation_env_config,
                attacker_action=attacker_action)
        else:
            raise ValueError("State update action id:{},name:{} not recognized".format(defender_action.id,
                                                                                       defender_action.name))