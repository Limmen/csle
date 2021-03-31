from gym_pycr_ctf.dao.observation.common.vulnerability_observation_state import VulnerabilityObservationState

class NiktoVuln:


    def __init__(self, id : str, osvdb_id : int, method: str, iplink: str, namelink: str, uri: str, description: str):
        self.id = id
        self.osvdb_id = osvdb_id
        self.method = method
        self.iplink = iplink
        self.namelink = namelink
        self.uri = uri
        self.description = description

    def to_obs(self) -> VulnerabilityObservationState:
        vuln = VulnerabilityObservationState(name="nikto_" + str(self.osvdb_id), port=None, protocol="HTTP",
                                             cvss=0, osvdbid=self.osvdb_id, description=self.description)
        return vuln

    def __str__(self):
        return "id:{}, osvdb_id:{}, method:{}, iplink:{}, namelink:{}, uri:{}, descr:{}".format(
            self.id, self.osvdb_id, self.method, self.iplink, self.namelink, self.uri, self.description)