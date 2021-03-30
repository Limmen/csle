from typing import List

class NodeTrafficConfig:

    def __init__(self, ip: str, commands: List[str], jumphosts: List[str], target_hosts: List[str]):
        self.ip = ip
        self.commands = commands
        self.jumphosts = jumphosts
        self.target_hosts = target_hosts