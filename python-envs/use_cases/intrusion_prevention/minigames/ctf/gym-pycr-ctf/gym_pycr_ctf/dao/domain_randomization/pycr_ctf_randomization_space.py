from pycr_common.dao.domain_randomization.pycr_randomization_space import PyCRRandomizationSpace
from gym_pycr_ctf.dao.domain_randomization.pycr_ctf_randomization_space_config import PyCRCTFRandomizationSpaceConfig


class PyCrCTFRandomizationSpace(PyCRRandomizationSpace):
    """
    Object representing a randomization space
    """

    def __init__(self, config: PyCRCTFRandomizationSpaceConfig):
        """
        Initializes the randomization space

        :param services: the list of services to randomize
        :param vulnerabilities: the list of vulnerabilities to randomize
        :param os: the operating system
        :param min_num_nodes: the minimum number of nodes for randomization
        :param max_num_nodes: the maximum number of nodes for randomization
        :param min_num_flags: the minimum number of flags for randomization
        :param max_num_flags: the maximum number of flags for randomization
        :param min_num_users: the minimum number of users for randomization
        :param max_num_users: the maximum number of users for randomization
        """
        self.config = config


    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"config:{str(self.config)}"

