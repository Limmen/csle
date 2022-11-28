from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.metastore.metastore_facade import MetastoreFacade


class SimulationEnvController:
    """
    Class managing operations related to simulation environments
    """

    @staticmethod
    def install_simulation(config: SimulationEnvConfig) -> None:
        """
        Installs the simulation configuration in the metastore

        :param config: the configuration to install
        :return: None
        """
        MetastoreFacade.install_simulation(config=config)

    @staticmethod
    def uninstall_simulation(config: SimulationEnvConfig) -> None:
        """
        Uninstalls a simulation config from the metastore

        :param config: the config to uninstall
        :return: None
        """
        MetastoreFacade.uninstall_simulation(config=config)

    @staticmethod
    def save_simulation_image(img: bytes, simulation: str) -> None:
        """
        Saves the simulation image

        :param image: the image data
        :param simulation: the name of the simulation
        :return: None
        """
        MetastoreFacade.save_simulation_image(img=img, simulation_name=simulation)
