from typing import List
from gym_pycr_pwcrack.dao.action_results.nmap_hop import NmapHop

class NmapTrace:

    def __init__(self, hops : List[NmapHop]):
        self.hops = hops


    def __str__(self):
        return "hops:{}".format(list(map(lambda x: str(x), self.hops)))