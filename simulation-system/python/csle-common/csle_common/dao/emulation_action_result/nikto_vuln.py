from typing import Union
from csle_common.dao.emulation_observation.common.emulation_vulnerability_observation_state \
    import EmulationVulnerabilityObservationState
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol


class NiktoVuln:
    """
    DTO representing a vulnerability found with a Nikto scan
    """

    def __init__(self, id: str, osvdb_id: Union[int, None], method: str, iplink: str,
                 namelink: str, uri: str, description: str):
        """
        Initializes the object

        :param id: the id of the vuln
        :param osvdb_id: the osvdb_id of the vuln
        :param method: the method of the vuln
        :param iplink: the iplink of the vuln
        :param namelink: the namelink of the vuln
        :param uri: the uri of the vuln
        :param description: the description of the vuln
        """
        self.id = id
        self.osvdb_id = osvdb_id
        self.method = method
        self.iplink = iplink
        self.namelink = namelink
        self.uri = uri
        self.description = description

    def to_obs(self) -> EmulationVulnerabilityObservationState:
        """
        Converts the object into a VulnerabilityObservationState

        :return: the created VulnerabilityObservationState object
        """
        vuln = EmulationVulnerabilityObservationState(name="nikto_" + str(self.osvdb_id), port=None,
                                                      protocol=TransportProtocol.TCP,
                                                      cvss=0, osvdbid=self.osvdb_id, description=self.description,
                                                      service="http")
        return vuln

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"id:{self.id}, osvdb_id:{self.osvdb_id}, method:{self.method}, iplink:{self.iplink}, " \
               f"namelink:{self.namelink}, uri:{self.uri}, descr:{self.description}"
