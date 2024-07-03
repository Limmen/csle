from unittest.mock import patch, MagicMock
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.controllers.simulation_env_controller import SimulationEnvController


class TestSimulationEnvControllerSuite:
    """
    Test suite for SimulationEnvController
    """

    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.install_simulation")
    def test_install_simulation(self, mock_install_simulation) -> None:
        """
        Test method that installs the simulation configuration in the metastore

        :param mock_install_simulation: mock_install_simulation
        :return: None
        """
        config = MagicMock(spec=SimulationEnvConfig)
        SimulationEnvController.install_simulation(config)
        mock_install_simulation.assert_called_once_with(config=config)

    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.uninstall_simulation")
    def test_uninstall_simulation(self, mock_uninstall_simulation) -> None:
        """
        Test method that uninstalls a simulation config from the metastore

        :param mock_uninstall_simulation: mock_uninstall_simulation
        :return: None
        """
        config = MagicMock(spec=SimulationEnvConfig)
        SimulationEnvController.uninstall_simulation(config)
        mock_uninstall_simulation.assert_called_once_with(config=config)

    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.save_simulation_image")
    def test_save_simulation_image(self, mock_save_simulation_image) -> None:
        """
        Test method that saves the simulation image

        :param mock_save_simulation_image: mock_save_simulation_image
        :return: None
        """
        img = b"image"
        simulation = "test_simulation"
        SimulationEnvController.save_simulation_image(img, simulation)
        mock_save_simulation_image.assert_called_once_with(img=img, simulation_name=simulation)
