from csle_common.dao.emulation_action.attacker.emulation_attacker_action \
    import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id \
    import EmulationAttackerActionId
from csle_attack_profiler.dao.tactics import Tactics
from csle_attack_profiler.dao.attack_mapping import EmulationAttackerMapping
from csle_attack_profiler.dao.attack_graph import AttackGraph
from mitreattack.stix20 import MitreAttackData
from typing import List, Dict, Union
import os


class AttackProfiler:
    """
    Class representing the attack profile based on the MITRE ATT&CK framework for Enterprise.
    """

    def __init__(self, techniques_tactics: Dict[str, List[str]], mitigations: Dict[str, List[str]],
                 data_sources: Dict[str, List[str]], subtechniques: Dict[str, str],
                 action_id: EmulationAttackerActionId) -> None:
        """
        Class constructor

        :params techniques_tactics: the techniques and tactics used by the attacker action.
                                    The key is the technique and the value is the tactics
        :params mitigations: the mitigations used by the attacker action. The key is the technique and the
                             value is the mitigations
        :params data_sources: the data sources used by the attacker action. The key is the technqiue and the value is
                              the data sources
        :params sub_techniques: the sub-techniques used by the attacker action. The key is the technique and
                                the value is the sub-techniques
        :params action_id: the id of the attacker action
        """
        
        self.techniques_tactics = techniques_tactics
        self.mitigations = mitigations
        self.data_sources = data_sources
        self.subtechniques = subtechniques
        self.action_id = action_id

    @staticmethod
    def get_attack_profile(attacker_action: EmulationAttackerAction) -> 'AttackProfiler':
        """
        Returns the attack profile of the actions

        :params attacker_action: the attacker action
        :return: the attack profile of the action
        """
        current_dir = os.path.dirname(__file__)
        path = os.path.join(current_dir, "./dao/enterprise-attack.json")
        mitre_attack_data = MitreAttackData(path)

        # Retrieve the id from the attacker action
        attacker_id = attacker_action.id
        # Get the defined tactics and techniques for the attack
        attack_mapping = EmulationAttackerMapping.get_attack_info(attacker_id)
        if attack_mapping is None:
            return AttackProfiler({}, {}, {}, {}, EmulationAttackerActionId.CONTINUE)

        attack_techniques_vals = [technique.value for technique in attack_mapping['techniques']]
        
        attacker_action_id = attacker_action.id
        techniques_tactics = {}
        mitigations = {}
        data_sources = {}
        sub_techniques = {}
        # Loop over the techniques associated with the attack
        for technique_name in attack_techniques_vals:
            # Get technique from MitreAttackData, stix_id maps to technique in the library.
            try:
                obj = mitre_attack_data.get_objects_by_name(technique_name, "attack-pattern")
            except Exception as e:
                os.system("echo 'Error in getting technique: {}'".format(e))
                continue
            technique = obj[0]
            stix_id = technique.id

            # Collect the tactics and add it to the dictionary
            tactics = [phase['phase_name'] for phase in technique.kill_chain_phases]
            techniques_tactics[technique_name] = tactics
            
            # Add the data sources to the dictionary
            if hasattr(technique, 'x_mitre_data_sources'):
                data_sources[technique_name] = technique.x_mitre_data_sources
            # Fetch the mitigations from the technique and add it to the dictionary
            try:
                mitigations_object = mitre_attack_data.get_mitigations_mitigating_technique(stix_id)
                mitigations_list = [mitig['object']['name'] for mitig in mitigations_object]
                mitigations[technique_name] = mitigations_list
            except Exception as e:
                os.system("echo 'Error in getting mitigations: {}'".format(e))
                continue
        
        # Add the sub-technique to the dictionary
        if 'subtechniques' in attack_mapping:
            sub_techniques_mapping = [sub_technique.value for sub_technique in attack_mapping['subtechniques']]
            for st in sub_techniques_mapping:
                try:
                    sub_technique_obj = mitre_attack_data.get_objects_by_name(st, "attack-pattern")
                    parent_technique_obj = mitre_attack_data.get_parent_technique_of_subtechnique(
                        sub_technique_obj[0].id)
                    sub_techniques[parent_technique_obj[0]['object'].name] = st
                except Exception as e:
                    os.system("echo 'Error in getting sub-techniques: {}'".format(e))
                    continue

        return AttackProfiler(techniques_tactics, mitigations, data_sources, sub_techniques, attacker_action_id)
    
    @staticmethod
    def get_attack_profile_sequence(attacker_actions: List[EmulationAttackerAction],
                                    attack_graph: Union[AttackGraph, None] = None) -> List['AttackProfiler']:
        """
        Returns the attack profile of the actions in a sequence

        :params attacker_action: a list of attacker actions

        :return: a list of attack profiles of the actions
        """

        attack_profiles = []
        for action in attacker_actions:
            attack_profiles.append(AttackProfiler.get_attack_profile(action))
        
        # IF attack graph is provided
        if attack_graph:

            node = attack_graph.get_root_node()
            for profile in attack_profiles:
                # Get the mappings of the techniques and tactics
                techniques_tactics = profile.techniques_tactics
                techniques_to_keep = []
                children = attack_graph.get_children(node[0], node[2])
                possible_nodes = []
                # First we check the techniques in node we are currently at
                for technique in techniques_tactics:
                    # If the node.name is in the techniques_tactics, add it to the techniques_to_keep
                    if node[0].value in techniques_tactics[technique]:
                        techniques_to_keep.append(technique)
                        if node not in possible_nodes:
                            possible_nodes.append(node)
                if children is None:
                    continue
                for child in children:
                    # Child is a list of tuples, where the first element is the node name,
                    # and the second element is the node id
                    for technique in techniques_tactics:
                        if child[0].value in techniques_tactics[technique]:
                            
                            techniques_to_keep.append(technique)
                            # If the child is not in the possible_children, add it to the list.
                            if attack_graph.get_node(child[0], child[1]) not in possible_nodes:
                                p_node = attack_graph.get_node(child[0], child[1])
                                if p_node is not None:
                                    possible_nodes.append(p_node)

                # If the possible node is just one node, move to that node
                if len(possible_nodes) == 1:
                    node = possible_nodes[0]
                if not techniques_to_keep:
                    continue
                # Remove the techniques and associated tactics, data sources,
                # mitigations and sub-techniques that are not in the techniques_to_keep
                techniques_to_remove = set(profile.techniques_tactics.keys()) - set(techniques_to_keep)
                for technique in techniques_to_remove:
                    try:
                        del profile.techniques_tactics[technique]
                        del profile.mitigations[technique]
                        del profile.data_sources[technique]
                        del profile.subtechniques[technique]
                    except Exception as e:
                        os.system("echo 'Error in removing techniques: {}'".format(e))
                        continue
                            
        # ELSE Baseline conditions
        else:
            initial_access = False
            for profile in attack_profiles:
                techniques_tactics = profile.techniques_tactics
                techniques_to_remove = set()
                # Loop over the mappings of the techniques to tactics
                for technique in techniques_tactics:
                    if Tactics.DISCOVERY.value in techniques_tactics[technique] and not initial_access:
                        techniques_to_remove.add(technique)
                    elif Tactics.RECONNAISSANCE.value in techniques_tactics[technique] and initial_access:
                        techniques_to_remove.add(technique)
                    if Tactics.INITIAL_ACCESS.value in techniques_tactics[technique] and not initial_access:
                        initial_access = True
                    elif Tactics.INITIAL_ACCESS.value in techniques_tactics[technique] and initial_access:
                        techniques_to_remove.add(technique)
                    elif Tactics.LATERAL_MOVEMENT.value in techniques_tactics[technique] and not initial_access:
                        techniques_to_remove.add(technique)
                
                # Remove the techniques and associated tactics, data sources, mitigations and sub-techniques
                for technique in techniques_to_remove:
                    try:
                        del profile.techniques_tactics[technique]
                        del profile.mitigations[technique]
                        del profile.data_sources[technique]
                        del profile.subtechniques[technique]
                    except Exception as e:
                        os.system("echo 'Error in removing techniques: {}'".format(e))
                        continue
                
        return attack_profiles
