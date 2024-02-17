from csle_common.dao.emulation_action.attacker.emulation_attacker_action \
    import EmulationAttackerAction
from csle_attack_profiler.tactics import Tactics
from csle_attack_profiler.techniques import Techniques
from csle_attack_profiler.attack_mapping import EmulationAttackerMapping

from mitreattack.stix20 import MitreAttackData
from typing import List, Dict

class AttackProfiler():
    """
    Class represting the attack profile based on the MITRE ATT&CK framework for Enterprise.
    """

    def __init__(self, techniques_tactics: Dict[str,List[str]], mitigations: Dict[str, List[str]], data_sources: Dict[str, List[str]], subtechniques: Dict[str, List[str]]):
        """
        Class constructor

        :params techniques_tactics: the techniques and tactics used by the attacker action. The key is the technique and the value is the tactics
        :params mitigations: the mitigations used by the attacker action. The key is the technique and the value is the mitigations
        :params data_sources: the data sources used by the attacker action. The key is the technqiue and the value is the data sources
        :params sub_techniques: the sub-techniques used by the attacker action. The key is the technique and the value is the sub-techniques 
        """        


        self.techniques_tactics = techniques_tactics
        self.mitigations = mitigations
        self.data_sources = data_sources
        self.subtechniques = subtechniques

    @staticmethod
    def get_attack_profile(attacker_action: EmulationAttackerAction):
        """
        Returns the attack profile of the actions

        :params attacker_action: the attacker action

        :return: 
        """
        mitre_attack_data = MitreAttackData("./src/csle_attack_profiler/enterprise-attack.json")

        # Retrieve the id from the attacker action
        attacker_id = attacker_action.id
        # Get the defined tactics and techniques for the attack
        attack_mapping = EmulationAttackerMapping.get_attack_info(attacker_id)
        #TODO: Return revelant error message
        print(attack_mapping)
        if attack_mapping == {None} or attack_mapping is None:
            return AttackProfiler({}, {}, {}, {})

        attack_techniques_vals = [technique.value for technique in attack_mapping['techniques']]
        
        techniques_tactics = {}
        mitigations = {}
        data_sources = {}
        sub_techniques = {}
        # Loop over the techniques associated with the attack
        for technique_name in attack_techniques_vals:
            # Get technique from MitreAttackData, stix_id maps to technique in the library.
            try:
                obj = mitre_attack_data.get_objects_by_name(technique_name, "attack-pattern")
            except:
                #TODO: Add logging
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
            except:
                continue
                
        
        # Add the sub-technique to the dictionary 
        if 'subtechniques' in attack_mapping:
            sub_techniques_mapping = [sub_technique.value for sub_technique in attack_mapping['subtechniques']]
            for st in sub_techniques_mapping:
                try:
                    sub_technique_obj = mitre_attack_data.get_objects_by_name(st, "attack-pattern")
                    parent_technique_obj = mitre_attack_data.get_parent_technique_of_subtechnique(sub_technique_obj[0].id)
                    sub_techniques[parent_technique_obj[0]['object'].name] = st
                except:
                    continue


        return AttackProfiler(techniques_tactics, mitigations, data_sources, sub_techniques)
                


            



        







    

    