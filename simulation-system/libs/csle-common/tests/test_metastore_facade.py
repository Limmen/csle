import json
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.emulation_config.emulation_simulation_trace import EmulationSimulationTrace
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_common.dao.training.alpha_vectors_policy import AlphaVectorsPolicy
from csle_common.dao.training.dqn_policy import DQNPolicy
from csle_common.dao.training.fnn_with_softmax_policy import FNNWithSoftmaxPolicy
from csle_common.dao.training.vector_policy import VectorPolicy
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.system_identification.empirical_system_model import EmpiricalSystemModel
from csle_common.dao.system_identification.mcmc_system_model import MCMCSystemModel
from csle_common.dao.system_identification.gp_system_model import GPSystemModel
from csle_common.dao.management.management_user import ManagementUser
from csle_common.dao.management.session_token import SessionToken
from csle_common.dao.datasets.traces_dataset import TracesDataset
from csle_common.dao.encoding.np_encoder import NpEncoder
from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.training.linear_threshold_stopping_policy import LinearThresholdStoppingPolicy


class TestMetastoreFacadeSuite:
    """
    Test suite for metastore_facade.py
    """

    def test_list_emulations(self, mocker: pytest_mock.MockFixture,
                             example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Tests the list_emulations function

        :param mocker: the pytest mocker object
        :param example_emulation_env_config: an example EmulationEnvConfig
        :return: None
        """
        id = 1
        example_emulation_env_config.id = 1
        example_record = (id, example_emulation_env_config.name, example_emulation_env_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_configs = MetastoreFacade.list_emulations()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(f"SELECT * FROM {constants.METADATA_STORE.EMULATIONS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_configs, list)
        assert isinstance(emulation_configs[0], EmulationEnvConfig)
        assert emulation_configs[0] == example_emulation_env_config

    def test_list_emulation_ids(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the list_emulations_ids function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_record = (id, "emulation1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_ids_and_names = MetastoreFacade.list_emulations_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,name FROM {constants.METADATA_STORE.EMULATIONS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_ids_and_names, list)
        assert isinstance(emulation_ids_and_names[0], tuple)
        assert emulation_ids_and_names[0] == example_record

    def test_convert_emulation_record_to_dto(self, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Tests the _convert_emulation_record_to_dto function

        :param example_emulation_env_config: an example EmulationEnvConfig DTO
        :return: None
        """
        id = 1
        name = example_emulation_env_config.name
        example_emulation_env_config.id = 1
        example_record = (id, name, example_emulation_env_config.to_dict())
        converted_object = MetastoreFacade._convert_emulation_record_to_dto(emulation_record=example_record)
        assert isinstance(converted_object, EmulationEnvConfig)
        assert converted_object == example_emulation_env_config

    def test_install_emulation(self, mocker: pytest_mock.MockFixture,
                               example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Tests the install_emulation function

        :param mocker: the pytest mocker object
        :param example_emulation_env_config: an example EmulationEnvConfig
        :return: None
        """
        id = 2
        example_emulation_env_config.id = 1
        example_record = (id, example_emulation_env_config.name, example_emulation_env_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.install_emulation(config=example_emulation_env_config)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(f"INSERT INTO {constants.METADATA_STORE.EMULATIONS_TABLE} "
                                                      f"(id, name, config) "
                                                      f"VALUES (%s, %s, %s) RETURNING id",
                                                      (id, example_emulation_env_config.name,
                                                       example_emulation_env_config.to_json_str()))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_get_emulation_by_name(self, mocker: pytest_mock.MockFixture,
                                   example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Tests the get_emulation_by_name function

        :param mocker: the pytest mocker object
        :param example_emulation_env_config: an example EmulationEnvConfig
        :return: None
        """
        id = 1
        example_emulation_env_config.id = id
        example_record = (id, example_emulation_env_config.name, example_emulation_env_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_emulation = MetastoreFacade.get_emulation_by_name(name=example_emulation_env_config.name)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE name = %s",
            (example_emulation_env_config.name,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_emulation, EmulationEnvConfig)
        assert fetched_emulation == example_emulation_env_config

    def test_get_emulation(self, mocker: pytest_mock.MockFixture,
                           example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Tests the get_emulation function

        :param mocker: the pytest mocker object
        :param example_emulation_env_config: an example EmulationEnvConfig
        :return: None
        """
        id = 1
        example_emulation_env_config.id = id
        example_record = (id, example_emulation_env_config.name, example_emulation_env_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_emulation = MetastoreFacade.get_emulation(id=example_emulation_env_config.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE id = %s",
            (example_emulation_env_config.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_emulation, EmulationEnvConfig)
        assert fetched_emulation == example_emulation_env_config

    def test_list_simulations(self, mocker: pytest_mock.MockFixture,
                              example_simulation_env_config: SimulationEnvConfig) -> None:
        """
        Tests the list_simulation function

        :param mocker: the pytest mocker object
        :param example_simulation_env_config: an example EmulationEnvConfig
        :return: None
        """
        id = 1
        example_simulation_env_config.id = 1
        example_record = (id, example_simulation_env_config.name, example_simulation_env_config.to_dict())
        mocker.patch('csle_common.dao.simulation_config.simulation_env_config.SimulationEnvConfig.from_dict',
                     return_value=example_simulation_env_config)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        simulation_configs = MetastoreFacade.list_simulations()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(f"SELECT * FROM {constants.METADATA_STORE.SIMULATIONS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(simulation_configs, list)
        assert isinstance(simulation_configs[0], SimulationEnvConfig)
        assert simulation_configs[0] == example_simulation_env_config

    def test_list_simulation_ids(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the list_simulation_ids function

        :param mocker: the pytest mocker object
        :param example_simulation_env_config: an example SimulationEnvConfig
        :return: None
        """
        id = 1
        example_record = (id, "simulation1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        simulation_configs = MetastoreFacade.list_simulation_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,name FROM {constants.METADATA_STORE.SIMULATIONS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(simulation_configs, list)
        assert isinstance(simulation_configs[0], tuple)
        assert simulation_configs[0] == example_record

    def test_get_simulations_by_name(self, mocker: pytest_mock.MockFixture,
                                     example_simulation_env_config: SimulationEnvConfig) -> None:
        """
        Tests the get_simulation_by_name function

        :param mocker: the pytest mocker object
        :param example_simulation_env_config: an example EmulationEnvConfig
        :return: None
        """
        id = 1
        example_simulation_env_config.id = 1
        example_record = (id, example_simulation_env_config.name, example_simulation_env_config.to_dict())
        mocker.patch('csle_common.dao.simulation_config.simulation_env_config.SimulationEnvConfig.from_dict',
                     return_value=example_simulation_env_config)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        simulation_config = MetastoreFacade.get_simulation_by_name(example_simulation_env_config.name)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.SIMULATIONS_TABLE} WHERE name = %s",
            (example_simulation_env_config.name,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(simulation_config, SimulationEnvConfig)
        assert simulation_config == example_simulation_env_config

    def test_get_simulations(self, mocker: pytest_mock.MockFixture,
                             example_simulation_env_config: SimulationEnvConfig) -> None:
        """
        Tests the get_simulation function

        :param mocker: the pytest mocker object
        :param example_simulation_env_config: an example EmulationEnvConfig
        :return: None
        """
        id = 1
        example_simulation_env_config.id = 1
        example_record = (id, example_simulation_env_config.name, example_simulation_env_config.to_dict())
        mocker.patch('csle_common.dao.simulation_config.simulation_env_config.SimulationEnvConfig.from_dict',
                     return_value=example_simulation_env_config)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        simulation_config = MetastoreFacade.get_simulation(example_simulation_env_config.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(f"SELECT * FROM {constants.METADATA_STORE.SIMULATIONS_TABLE} "
                                                      f"WHERE id = %s", (example_simulation_env_config.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(simulation_config, SimulationEnvConfig)
        assert simulation_config == example_simulation_env_config

    def test_convert_simulation_record_to_dto(self, mocker: pytest_mock.MockFixture,
                                              example_simulation_env_config: SimulationEnvConfig) -> None:
        """
        Tests the _convert_simulation_record_to_dto function

        :param mocker: the pytest mocker object
        :param example_simulation_env_config: an example SimulationEnvConfig DTO
        :return: None
        """
        id = 1
        example_simulation_env_config.id = 1
        example_record = (id, example_simulation_env_config.name, example_simulation_env_config.to_dict())
        mocker.patch('csle_common.dao.simulation_config.simulation_env_config.SimulationEnvConfig.from_dict',
                     return_value=example_simulation_env_config)
        converted_object = MetastoreFacade._convert_simulation_record_to_dto(simulation_record=example_record)
        assert isinstance(converted_object, SimulationEnvConfig)
        assert converted_object == example_simulation_env_config

    def test_convert_emulation_trace_record_to_dto(self, example_emulation_trace: EmulationTrace) -> None:
        """
        Tests the _convert_emulation_trace_record_to_dto function

        :param example_emulation_trace: an example EmulationTrace DTO
        :return: None
        """
        id = 1
        example_emulation_trace.emulation_name = "emulation_trace1"
        example_emulation_trace.id = 1
        example_record = (id, example_emulation_trace.emulation_name, example_emulation_trace.to_dict())
        converted_object = MetastoreFacade._convert_emulation_trace_record_to_dto(emulation_trace_record=example_record)
        assert isinstance(converted_object, EmulationTrace)
        assert converted_object == example_emulation_trace

    def test_convert_emulation_simulation_trace_record_to_dto(self, mocker: pytest_mock.MockFixture,
                                                              example_simulation_trace: SimulationTrace,
                                                              example_emulation_trace: EmulationTrace) -> None:
        """
        Tests the _convert_emulation_simulation_trace_record_to_dto function

        :param mocker: the pytest mocker object
        :param example_simulation_trace: an example SimulationTrace DTO
        :param example_emulation_trace: an example EmulationTrace DTO
        :return: None
        """
        id = 1
        example_simulation_emulation_trace = EmulationSimulationTrace(simulation_trace=example_simulation_trace,
                                                                      emulation_trace=example_emulation_trace)
        example_simulation_emulation_trace.id = id
        example_record = (id, example_simulation_emulation_trace.emulation_trace.id,
                          example_simulation_emulation_trace.simulation_trace.id)
        mocker.patch(
            'csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_trace',
            return_value=example_emulation_trace)
        mocker.patch(
            'csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation_trace',
            return_value=example_simulation_trace)
        converted_object = MetastoreFacade._convert_emulation_simulation_trace_record_to_dto(
            emulation_simulation_trace_record=example_record)
        assert isinstance(converted_object, EmulationSimulationTrace)
        assert converted_object == example_simulation_emulation_trace

    def test_convert_simulation_trace_record_to_dto(self, example_simulation_trace: SimulationTrace) -> None:
        """
        Tests the _convert_simulation_trace_record_to_dto function

        :param example_simulation_trace: an example SimulationTrace DTO
        :return: None
        """
        id = 1
        example_simulation_trace.name = "simulation_trace1"
        example_simulation_trace.id = 1
        example_record = (id, example_simulation_trace.name, example_simulation_trace.to_dict())
        converted_object = MetastoreFacade._convert_simulation_trace_record_to_dto(
            simulation_trace_record=example_record)
        assert isinstance(converted_object, SimulationTrace)
        assert converted_object == example_simulation_trace

    def test_convert_emulation_statistics_record_to_dto(self,
                                                        example_emulation_statistics: EmulationStatistics) -> None:
        """
        Tests the _convert_emulation_statistics_record_to_dto function

        :param example_emulation_statistics: an example EmulationStatistics DTO
        :return: None
        """
        id = 1
        example_emulation_statistics.name = "emulation_static1"
        example_emulation_statistics.id = 1
        example_record = (id, example_emulation_statistics.name, example_emulation_statistics.to_dict())
        converted_object = MetastoreFacade._convert_emulation_statistics_record_to_dto(
            emulation_statistics_record=example_record)
        assert isinstance(converted_object, EmulationStatistics)
        assert converted_object == example_emulation_statistics

    def test_convert_emulation_image_record_to_tuple(self) -> None:
        """
        Tests the _convert_emulation_image_record_to_tuple function

        :return: None
        """
        id = 1
        example_emulation_image_name = "image_name1"
        example_emulation_image_data = bytes([1, 3, 5, 6])
        example_record = (id, example_emulation_image_name, example_emulation_image_data)
        converted_object = MetastoreFacade._convert_emulation_image_record_to_tuple(
            emulation_image_record=example_record)
        assert isinstance(converted_object, tuple)
        assert converted_object == (example_emulation_image_name, example_emulation_image_data)

    def test_convert_simulation_image_record_to_tuple(self) -> None:
        """
        Tests the _convert_simulation_image_record_to_tuple function

        :return: None
        """
        id = 1
        example_simulation_image_name = "image_name1"
        example_simulation_image_data = bytes([1, 3, 5, 6])
        example_record = (id, example_simulation_image_name, example_simulation_image_data)
        converted_object = MetastoreFacade._convert_simulation_image_record_to_tuple(
            simulation_image_record=example_record)
        assert isinstance(converted_object, tuple)
        assert converted_object == (example_simulation_image_name, example_simulation_image_data)

    def test_uninstall_emulation(self, mocker: pytest_mock.MockFixture, example_emulation_env_config) -> None:
        """
        Tests the uninstall_emulation function

        :param mocker: the pytest mocker object
        :param example_emulation_env_config: an example EmulationEnvConfig object
        :return: None
        """
        example_emulation_env_config.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.uninstall_emulation(config=example_emulation_env_config)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE name = %s",
            (example_emulation_env_config.name,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_install_simulation(self, mocker: pytest_mock.MockFixture,
                                example_simulation_env_config: SimulationEnvConfig) -> None:
        """
        Tests the install_simulation function

        :param mocker: the pytest mocker object
        :param example_simulation_env_config: an example SimulationEnvConfig object
        :return: None
        """
        id = 2
        example_simulation_env_config.id = 1
        example_simulation_env_config.name = "simulation1"
        example_record = (id, example_simulation_env_config.name, example_simulation_env_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.install_simulation(config=example_simulation_env_config)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_uninstall_simulation(self, mocker: pytest_mock.MockFixture,
                                  example_simulation_env_config: SimulationEnvConfig) -> None:
        """
        Tests the uninstall_simulation function

        :param mocker: the pytest mocker object
        :param example_simulation_env_config: an example SimulationEnvConfig object
        :return: None
        """
        example_simulation_env_config.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.uninstall_simulation(config=example_simulation_env_config)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.SIMULATIONS_TABLE} WHERE name = %s",
            (example_simulation_env_config.name,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_save_emulation_trace(self, mocker: pytest_mock.MockFixture,
                                  example_emulation_trace: EmulationTrace) -> None:
        """
        Tests the save_emulation_trace function

        :param mocker: the pytest mocker object
        :param example_emulation_trace: an example EmulationTrace object
        :return: None
        """
        id = 2
        example_emulation_trace.id = 1
        example_record = (id, example_emulation_trace.emulation_name, example_emulation_trace.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_emulation_trace(emulation_trace=example_emulation_trace)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(f"INSERT INTO {constants.METADATA_STORE.EMULATION_TRACES_TABLE} "
                                                      f"(id, emulation_name, trace) "
                                                      f"VALUES (%s, %s, %s) RETURNING id",
                                                      (id, example_emulation_trace.emulation_name,
                                                       example_emulation_trace.to_json_str()))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_save_emulation_statistic(self, mocker: pytest_mock.MockFixture,
                                      example_emulation_statistics: EmulationStatistics) -> None:
        """
        Tests the save_emulation_statistic function

        :param mocker: the pytest mocker object
        :param example_emulation_statistics: an example EmulationStatistics object
        :return: None
        """
        id = 2
        example_emulation_statistics.id = id
        example_record = (id, example_emulation_statistics.emulation_name, example_emulation_statistics.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_emulation_statistic(emulation_statistics=example_emulation_statistics)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(f"INSERT INTO "
                                                      f"{constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} "
                                                      f"(id, emulation_name, statistics) "
                                                      f"VALUES (%s, %s, %s) RETURNING id",
                                                      (id, example_emulation_statistics.emulation_name,
                                                       example_emulation_statistics.to_json_str()))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_update_emulation_statistic(self, mocker: pytest_mock.MockFixture,
                                        example_emulation_statistics: EmulationStatistics) -> None:
        """
        Tests the update_emulation_statistic function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 2
        example_emulation_statistics.id = id
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_emulation_statistic(
            id=id,
            emulation_statistics=example_emulation_statistics)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} "
            f" SET statistics=%s "
            f"WHERE {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE}.id = %s",
            (example_emulation_statistics.to_json_str(), id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_list_emulation_statistics(self, mocker: pytest_mock.MockFixture,
                                       example_emulation_statistics: EmulationStatistics) -> None:
        """
        Tests the list_emulation_statistics function

        :param mocker: the pytest mocker object
        :param example_emulation_statistics: an example EmulationStatistics object
        :return: None
        """
        id = 1
        example_emulation_statistics.id = id
        example_record = (id, example_emulation_statistics.emulation_name, example_emulation_statistics.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_statistics = MetastoreFacade.list_emulation_statistics()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_statistics, list)
        assert isinstance(emulation_statistics[0], EmulationStatistics)
        assert emulation_statistics[0] == example_emulation_statistics

    def test_list_emulation_statistics_ids(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the list_emulation_statistics_ids function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_record = (id, "emulation_statistics1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_statistics_ids = MetastoreFacade.list_emulation_statistics_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,"
            f"emulation_name FROM {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_statistics_ids, list)
        assert isinstance(emulation_statistics_ids[0], tuple)
        assert isinstance(emulation_statistics_ids[0][0], int)
        assert isinstance(emulation_statistics_ids[0][1], str)
        assert emulation_statistics_ids[0] == example_record

    def test_list_emulation_traces(self, mocker: pytest_mock.MockFixture,
                                   example_emulation_trace: EmulationTrace) -> None:
        """
        Tests the list_emulation_traces function

        :param mocker: the pytest mocker object
        :param example_emulation_traces: an example EmulationTrace object
        :return: None
        """
        id = 1
        example_emulation_trace.id = id
        example_record = (id, example_emulation_trace.emulation_name, example_emulation_trace.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_traces = MetastoreFacade.list_emulation_traces()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_traces, list)
        assert isinstance(emulation_traces[0], EmulationTrace)
        assert emulation_traces[0] == example_emulation_trace

    def test_list_emulation_traces_ids(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the list_emulation_traces_ids function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_record = (id, "emulation_trace1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_traces_ids = MetastoreFacade.list_emulation_traces_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,emulation_name FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_traces_ids, list)
        assert isinstance(emulation_traces_ids[0], tuple)
        assert isinstance(emulation_traces_ids[0][0], int)
        assert isinstance(emulation_traces_ids[0][1], str)
        assert emulation_traces_ids[0] == example_record

    def test_list_emulation_simulation_traces_ids(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the list_emulation_simulation_traces_ids function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_record = (id,)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_emulation_simulation_ids = MetastoreFacade.list_emulation_simulation_traces_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id FROM {constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_emulation_simulation_ids, list)
        assert isinstance(emulation_emulation_simulation_ids[0], int)
        assert emulation_emulation_simulation_ids[0] == example_record[0]

    def test_list_simulation_traces_ids(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the list_simulation_traces_ids function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_record = (id, "simulation_gym_env1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        simulation_traces_ids = MetastoreFacade.list_simulation_traces_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,gym_env FROM {constants.METADATA_STORE.SIMULATION_TRACES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(simulation_traces_ids, list)
        assert isinstance(simulation_traces_ids[0], tuple)
        assert isinstance(simulation_traces_ids[0][0], int)
        assert isinstance(simulation_traces_ids[0][1], str)
        assert simulation_traces_ids[0] == example_record

    def test_list_simulation_traces(self, mocker: pytest_mock.MockFixture,
                                    example_simulation_trace: SimulationTrace) -> None:
        """
        Tests the list_simulation_traces function

        :param mocker: the pytest mocker object
        :param example_simulation_traces: an example SimulationTrace object
        :return: None
        """
        id = 1
        example_simulation_trace.id = id
        example_record = (id, example_simulation_trace.simulation_env, example_simulation_trace.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        simulation_traces = MetastoreFacade.list_simulation_traces()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_TRACES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(simulation_traces, list)
        assert isinstance(simulation_traces[0], SimulationTrace)
        assert simulation_traces[0] == example_simulation_trace

    def test_remove_simulation_trace(self, mocker: pytest_mock.MockFixture,
                                     example_simulation_trace: SimulationTrace) -> None:
        """
        Tests the remove_simulation_trace function

        :param mocker: the pytest mocker object
        :param example_simulation_trace: an example SimulationTrace object
        :return: None
        """
        example_simulation_trace.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_simulation_trace(simulation_trace=example_simulation_trace)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.SIMULATION_TRACES_TABLE} WHERE id = %s",
            (example_simulation_trace.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_get_emulation_trace(self, mocker: pytest_mock.MockFixture,
                                 example_emulation_trace: EmulationTrace) -> None:
        """
        Tests the get_emulation_trace function

        :param mocker: the pytest mocker object
        :param example_emulation_trace: an example EmulationTrace
        :return: None
        """
        id = 1
        example_emulation_trace.id = id
        example_record = (id, example_emulation_trace.emulation_name, example_emulation_trace.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_emulation_trace = MetastoreFacade.get_emulation_trace(id=example_emulation_trace.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE} WHERE id = %s",
            (example_emulation_trace.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_emulation_trace, EmulationTrace)
        assert fetched_emulation_trace == example_emulation_trace

    def test_remove_emulation_trace(self, mocker: pytest_mock.MockFixture,
                                    example_emulation_trace: EmulationTrace) -> None:
        """
        Tests the remove_emulation_trace function

        :param mocker: the pytest mocker object
        :param example_emulation_trace: an example EmulationTrace object
        :return: None
        """
        example_emulation_trace.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_emulation_trace(emulation_trace=example_emulation_trace)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE} WHERE id = %s",
            (example_emulation_trace.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_emulation_simulation_trace(self, mocker: pytest_mock.MockFixture,
                                               example_emulation_trace: EmulationTrace,
                                               example_simulation_trace: SimulationTrace) -> None:
        """
        Tests the remove_emulation_simulation_trace function

        :param mocker: the pytest mocker object
        :param example_emulation_trace: an example EmulationTrace object
        :param example_simulation_trace_trace: an example Simulation object
        :return: None
        """
        example_emulation_simulation_trace = EmulationSimulationTrace(simulation_trace=example_simulation_trace,
                                                                      emulation_trace=example_emulation_trace)
        example_emulation_simulation_trace.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_emulation_simulation_trace(
            emulation_simulation_trace=example_emulation_simulation_trace)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE} WHERE id = %s",
            (example_emulation_simulation_trace.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_get_emulation_statistics(self, mocker: pytest_mock.MockFixture,
                                      example_emulation_statistics: EmulationStatistics) -> None:
        """
        Tests the get_emulation_statistics function

        :param mocker: the pytest mocker object
        :param example_emulation_statistics: an example EmulationTrace
        :return: None
        """
        id = 1
        example_emulation_statistics.id = id
        example_record = (id, example_emulation_statistics.emulation_name, example_emulation_statistics.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_emulation_statistics = MetastoreFacade.get_emulation_statistic(id=example_emulation_statistics.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} "
            f"WHERE id = %s", (example_emulation_statistics.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_emulation_statistics, EmulationStatistics)
        assert fetched_emulation_statistics == example_emulation_statistics

    def test_remove_emulation_statistic(self, mocker: pytest_mock.MockFixture,
                                        example_emulation_statistics: EmulationStatistics) -> None:
        """
        Tests the remove_emulation_statistic function

        :param mocker: the pytest mocker object
        :param example_emulation_statistics: an example EmulationStatistics object
        :return: None
        """
        example_emulation_statistics.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_emulation_statistic(
            emulation_statistic=example_emulation_statistics)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} WHERE id = %s",
            (example_emulation_statistics.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_get_simulation_trace(self, mocker: pytest_mock.MockFixture,
                                  example_simulation_trace: SimulationTrace) -> None:
        """
        Tests the get_simulation_trace function

        :param mocker: the pytest mocker object
        :param example_simulation_trace: an example SimulationTrace
        :return: None
        """
        id = 1
        example_simulation_trace.id = id
        example_record = (id, example_simulation_trace.simulation_env, example_simulation_trace.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_simulation_trace = MetastoreFacade.get_simulation_trace(id=example_simulation_trace.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_TRACES_TABLE} WHERE id = %s",
            (example_simulation_trace.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_simulation_trace, SimulationTrace)
        assert fetched_simulation_trace == example_simulation_trace

    def test_save_simulation_trace(self, mocker: pytest_mock.MockFixture,
                                   example_simulation_trace: SimulationTrace) -> None:
        """
        Tests the save_simulation_trace function

        :param mocker: the pytest mocker object
        :param example_simulation_trace: an example SimulationTrace object
        :return: None
        """
        id = 2
        example_simulation_trace.id = id
        example_record = (id, example_simulation_trace.simulation_env, example_simulation_trace.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_simulation_trace(simulation_trace=example_simulation_trace)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.SIMULATION_TRACES_TABLE} (id, gym_env, trace) "
            f"VALUES (%s, %s, %s) RETURNING id", (id, example_simulation_trace.simulation_env,
                                                  example_simulation_trace.to_json_str()))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_save_emulation_simulation_trace(self, mocker: pytest_mock.MockFixture,
                                             example_simulation_trace: SimulationTrace,
                                             example_emulation_trace: EmulationTrace) -> None:
        """
        Tests the save_simulation_trace function

        :param mocker: the pytest mocker object
        :param example_simulation_trace: an example SimulationTrace object
        :param example_emulation_trace: an example EmulationTrace object
        :return: None
        """
        id = 2
        example_simulation_trace.id = 1
        example_emulation_trace.id = 3
        example_emulation_simulation_trace = EmulationSimulationTrace(simulation_trace=example_simulation_trace,
                                                                      emulation_trace=example_emulation_trace)
        example_emulation_simulation_trace.id = id
        example_record = (id, example_emulation_simulation_trace.emulation_trace.id,
                          example_emulation_simulation_trace.simulation_trace.id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_emulation_trace',
                     return_value=example_emulation_trace.id)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_simulation_trace',
                     return_value=example_simulation_trace.id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_emulation_simulation_trace(
            emulation_simulation_trace=example_emulation_simulation_trace)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO "
            f"{constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE} "
            f"(id, emulation_trace, simulation_trace) "
            f"VALUES (%s, %s, %s) RETURNING id", (id, example_emulation_trace.id, example_simulation_trace.id))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_list_emulation_simulation_traces(self, mocker: pytest_mock.MockFixture,
                                              example_simulation_trace: SimulationTrace,
                                              example_emulation_trace: EmulationTrace) -> None:
        """
        Tests the list_emulation_simulation_traces function

        :param mocker: the pytest mocker object
        :param example_simulation_traces: an example SimulationTrace object
        :param example_emulation_traces: an example EmulationTrace object
        :return: None
        """
        id = 1
        example_emulation_simulation_trace = EmulationSimulationTrace(emulation_trace=example_emulation_trace,
                                                                      simulation_trace=example_simulation_trace)
        example_emulation_simulation_trace.id = id
        example_record = (id, example_emulation_trace.id, example_simulation_trace.id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_trace',
                     return_value=example_emulation_trace)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation_trace',
                     return_value=example_simulation_trace)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_simulation_traces = MetastoreFacade.list_emulation_simulation_traces()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_simulation_traces, list)
        assert isinstance(emulation_simulation_traces[0], EmulationSimulationTrace)
        assert emulation_simulation_traces[0] == example_emulation_simulation_trace

    def test_get_emulation_simulation_trace(self, mocker: pytest_mock.MockFixture,
                                            example_simulation_trace: SimulationTrace,
                                            example_emulation_trace: EmulationTrace) -> None:
        """
        Tests the get_emulation_simulation_trace function

        :param mocker: the pytest mocker object
        :param example_simulation_trace: an example SimulationTrace
        :param example_emulation_trace: an example EmulationTrace
        :return: None
        """
        id = 1
        example_emulation_simulation_trace = EmulationSimulationTrace(emulation_trace=example_emulation_trace,
                                                                      simulation_trace=example_simulation_trace)
        example_emulation_simulation_trace.id = id
        example_record = (id, example_emulation_trace.id, example_simulation_trace.id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_trace',
                     return_value=example_emulation_trace)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation_trace',
                     return_value=example_simulation_trace)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_emulation_simulation_trace = MetastoreFacade.get_emulation_simulation_trace(
            id=example_emulation_simulation_trace.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE} "
            f"WHERE id = %s", (example_emulation_simulation_trace.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_emulation_simulation_trace, EmulationSimulationTrace)
        assert fetched_emulation_simulation_trace == example_emulation_simulation_trace

    def test_save_emulation_image(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the save_emulation_image function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_emulation_image_name = "image_name1"
        example_emulation_image_data = bytes([1, 3, 5, 6])
        example_record = (id, example_emulation_image_name, example_emulation_image_data)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_emulation_image(emulation_name=example_emulation_image_name,
                                                           img=example_emulation_image_data)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.EMULATION_IMAGES_TABLE} "
            f"(id, emulation_name, image) VALUES (%s, %s, %s) RETURNING id", (id, example_emulation_image_name,
                                                                              example_emulation_image_data))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_list_emulation_images(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the list_emulation_images function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_emulation_image_name = "image_name1"
        example_emulation_image_data = bytes([1, 3, 5, 6])
        example_record = (id, example_emulation_image_name, example_emulation_image_data)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_images = MetastoreFacade.list_emulation_images()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_IMAGES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_images, list)
        assert isinstance(emulation_images[0], tuple)
        assert isinstance(emulation_images[0][0], str)
        assert isinstance(emulation_images[0][1], bytes)
        assert emulation_images[0] == (example_emulation_image_name, example_emulation_image_data)

    def test_get_emulation_image(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the get_emulation_image function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_emulation_image_name = "image_name1"
        example_emulation_image_data = bytes([1, 3, 5, 6])
        example_record = (id, example_emulation_image_name, example_emulation_image_data)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_emulation_image = MetastoreFacade.get_emulation_image(emulation_name=example_emulation_image_name)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_IMAGES_TABLE} "
            f"WHERE emulation_name = %s", (example_emulation_image_name,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_emulation_image, tuple)
        assert isinstance(fetched_emulation_image[0], str)
        assert isinstance(fetched_emulation_image[1], bytes)
        assert fetched_emulation_image == (example_emulation_image_name, example_emulation_image_data)

    def test_delete_all(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the delete_all function

        :param mocker: the pytest mocker object
        :return: None
        """
        table_name = "test_table1"
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.delete_all(table=table_name)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {table_name}")
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_save_simmulation_image(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the save_simulation_image function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_simulation_image_name = "image_name1"
        example_simulation_image_data = bytes([1, 3, 5, 6])
        example_record = (id, example_simulation_image_name, example_simulation_image_data)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_simulation_image(simulation_name=example_simulation_image_name,
                                                            img=example_simulation_image_data)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.SIMULATION_IMAGES_TABLE} "
            f"(id, simulation_name, image) VALUES (%s, %s, %s) RETURNING id",
            (id, example_simulation_image_name, example_simulation_image_data))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_list_simulation_images(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the list_simulation_images function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_simulation_image_name = "image_name1"
        example_simulation_image_data = bytes([1, 3, 5, 6])
        example_record = (id, example_simulation_image_name, example_simulation_image_data)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        simulation_images = MetastoreFacade.list_simulation_images()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_IMAGES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(simulation_images, list)
        assert isinstance(simulation_images[0], tuple)
        assert isinstance(simulation_images[0][0], str)
        assert isinstance(simulation_images[0][1], bytes)
        assert simulation_images[0] == (example_simulation_image_name, example_simulation_image_data)

    def test_get_simulation_image(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the get_simulation_image function

        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_simulation_image_name = "image_name1"
        example_simulation_image_data = bytes([1, 3, 5, 6])
        example_record = (id, example_simulation_image_name, example_simulation_image_data)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_simulation_image = MetastoreFacade.get_simulation_image(simulation_name=example_simulation_image_name)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_IMAGES_TABLE} "
            f"WHERE simulation_name = %s", (example_simulation_image_name,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_simulation_image, tuple)
        assert isinstance(fetched_simulation_image[0], str)
        assert isinstance(fetched_simulation_image[1], bytes)
        assert fetched_simulation_image == (example_simulation_image_name, example_simulation_image_data)

    def test_save_experiment_execution(self, mocker: pytest_mock.MockFixture,
                                       example_experiment_execution: ExperimentExecution) -> None:
        """
        Tests the save_experiment_execution function

        :param mocker: the pytest mocker object
        :param example_experiment_execution: an example ExperimentExecution object
        :return: None
        """
        id = 2
        example_experiment_execution.id = id
        example_record = (id, example_experiment_execution.to_dict(), example_experiment_execution.simulation_name,
                          example_experiment_execution.emulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_experiment_execution(experiment_execution=example_experiment_execution)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE} "
            f"(id, execution, simulation_name, emulation_name) "
            f"VALUES (%s, %s, %s, %s) RETURNING id", (id, example_experiment_execution.to_json_str(),
                                                      example_experiment_execution.simulation_name,
                                                      example_experiment_execution.emulation_name))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_list_experiment_execution(self, mocker: pytest_mock.MockFixture,
                                       example_experiment_execution: ExperimentExecution) -> None:
        """
        Tests the list_experiment_execution function

        :param mocker: the pytest mocker object
        :param example_experiment_execution: an example ExperimentExecution object
        :return: None
        """
        id = 1
        example_experiment_execution.id = id
        example_record = (id, example_experiment_execution.to_dict(), example_experiment_execution.simulation_name,
                          example_experiment_execution.emulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        experiment_execution = MetastoreFacade.list_experiment_executions()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(experiment_execution, list)
        assert isinstance(experiment_execution[0], ExperimentExecution)
        assert experiment_execution[0] == example_experiment_execution

    def test_list_experiment_execution_ids(self, mocker: pytest_mock.MockFixture,
                                           example_experiment_execution: ExperimentExecution) -> None:
        """
        Tests the list_experiment_execution_ids function

        :param mocker: the pytest mocker object
        :param example_experiment_execution: an example ExperimentExecution object
        :return: None
        """
        id = 1
        example_experiment_execution.id = id
        example_record = (id, example_experiment_execution.simulation_name,
                          example_experiment_execution.emulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        experiment_executions_ids = MetastoreFacade.list_experiment_executions_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,simulation_name,emulation_name FROM "
            f"{constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(experiment_executions_ids, list)
        assert isinstance(experiment_executions_ids[0], tuple)
        assert isinstance(experiment_executions_ids[0][0], int)
        assert isinstance(experiment_executions_ids[0][1], str)
        assert isinstance(experiment_executions_ids[0][2], str)
        assert experiment_executions_ids[0][0] == id
        assert experiment_executions_ids[0][1] == example_experiment_execution.simulation_name
        assert experiment_executions_ids[0][2] == example_experiment_execution.emulation_name

    def test_convert_experiment_execution_record_to_dto(
            self, example_experiment_execution: ExperimentExecution) -> None:
        """
        Tests the _convert_experiment_execution_record_to_dto function

        :param example_experiment_execution: an example ExperimentExecution object
        :return: None
        """
        id = 1
        example_experiment_execution.id = 1
        example_record = (id, example_experiment_execution.to_dict())
        converted_object = MetastoreFacade._convert_experiment_execution_record_to_dto(
            experiment_execution_record=example_record)
        assert isinstance(converted_object, ExperimentExecution)
        assert converted_object == example_experiment_execution

    def test_get_experiment_execution(self, mocker: pytest_mock.MockFixture,
                                      example_experiment_execution: ExperimentExecution) -> None:
        """
        Tests the get_experiment_execution function

        :param example_experiment_execution: an example ExperimentExecution object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_experiment_execution.id = id
        example_record = (id, example_experiment_execution.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_experiment_execution = MetastoreFacade.get_experiment_execution(id=example_experiment_execution.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE} "
            f"WHERE id = %s", (example_experiment_execution.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_experiment_execution, ExperimentExecution)
        assert fetched_experiment_execution == example_experiment_execution

    def test_remove_experiment_execution(self, mocker: pytest_mock.MockFixture,
                                         example_experiment_execution: ExperimentExecution) -> None:
        """
        Tests the remove_experiment_execution function

        :param mocker: the pytest mocker object
        :param example_experiment_execution: an example ExperimentExecution object
        :return: None
        """
        example_experiment_execution.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_experiment_execution(experiment_execution=example_experiment_execution)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE} WHERE id = %s",
            (example_experiment_execution.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_list_multi_threshold_stopping_policies(
            self, mocker: pytest_mock.MockFixture,
            example_multi_threshold_stopping_policy: MultiThresholdStoppingPolicy) -> None:
        """
        Tests the remove_experiment_execution function

        :param mocker: the pytest mocker object
        :param example_multi_threshold_stopping_policy: an example MultiThresholdStoppingPolicy object
        :return: None
        """
        id = 1
        example_multi_threshold_stopping_policy.id = id
        example_record = (id, example_multi_threshold_stopping_policy.to_dict(),
                          example_multi_threshold_stopping_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        multi_threshold_stopping_policies = MetastoreFacade.list_multi_threshold_stopping_policies()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(multi_threshold_stopping_policies, list)
        assert isinstance(multi_threshold_stopping_policies[0], MultiThresholdStoppingPolicy)
        assert multi_threshold_stopping_policies[0] == example_multi_threshold_stopping_policy

    def test_list_multi_threshold_stopping_policies_ids(
            self, mocker: pytest_mock.MockFixture,
            example_multi_threshold_stopping_policy: MultiThresholdStoppingPolicy) -> None:
        """
        Tests the list_multi_threshold_stopping_policies_ids function

        :param mocker: the pytest mocker object
        :param example_multi_threshold_stopping_policy: an example MultiThresholdStoppingPolicy object
        :return: None
        """
        id = 1
        example_record = (id, "multi_threshold_stopping_policy1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        multi_threshold_stopping_policy_ids = MetastoreFacade.list_multi_threshold_stopping_policies_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,simulation_name FROM "
            f"{constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(multi_threshold_stopping_policy_ids, list)
        assert isinstance(multi_threshold_stopping_policy_ids[0], tuple)
        assert isinstance(multi_threshold_stopping_policy_ids[0][0], int)
        assert isinstance(multi_threshold_stopping_policy_ids[0][1], str)
        assert multi_threshold_stopping_policy_ids[0] == example_record

    def test_convert_multi_threshold_stopping_policy_record_to_dto(
            self, example_multi_threshold_stopping_policy: MultiThresholdStoppingPolicy) -> None:
        """
        Tests the _convert_multi_threshold_stopping_policy_record_to_dto function

        :param example_multi_threshold_stopping_policy: an example MultiThresholdStoppingPolicy object
        :return: None
        """
        id = 1
        example_multi_threshold_stopping_policy.id = 1
        example_record = (id, example_multi_threshold_stopping_policy.to_dict())
        converted_object = MetastoreFacade._convert_multi_threshold_stopping_policy_record_to_dto(
            multi_threshold_stopping_policy_record=example_record)
        assert isinstance(converted_object, MultiThresholdStoppingPolicy)
        assert converted_object == example_multi_threshold_stopping_policy

    def test_get_multi_threshold_stopping_policy(
            self, mocker: pytest_mock.MockFixture,
            example_multi_threshold_stopping_policy: MultiThresholdStoppingPolicy) -> None:
        """
        Tests the get_multi_threshold_stopping_policy function

        :param example_multi_threshold_stopping_policy: an example MultiThresholdStoppingPolicy object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_multi_threshold_stopping_policy.id = id
        example_record = (id, example_multi_threshold_stopping_policy.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_multi_threshold_stopping_policy = MetastoreFacade.get_multi_threshold_stopping_policy(
            id=example_multi_threshold_stopping_policy.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE} "
            f"WHERE id = %s", (example_multi_threshold_stopping_policy.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_multi_threshold_stopping_policy, MultiThresholdStoppingPolicy)
        assert fetched_multi_threshold_stopping_policy == example_multi_threshold_stopping_policy

    def test_remove_multi_threshold_stopping_policy(
            self, mocker: pytest_mock.MockFixture,
            example_multi_threshold_stopping_policy: MultiThresholdStoppingPolicy) -> None:
        """
        Tests the remove_multi_threshold_stopping_policy function

        :param mocker: the pytest mocker object
        :param example_multi_threshold_stopping_policy: an example MultiThresholdStoppingPolicy object
        :return: None
        """
        example_multi_threshold_stopping_policy.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_multi_threshold_stopping_policy(
            multi_threshold_stopping_policy=example_multi_threshold_stopping_policy)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE} "
            f"WHERE id = %s", (example_multi_threshold_stopping_policy.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_save_multi_threshold_stopping_policy(
            self, mocker: pytest_mock.MockFixture,
            example_multi_threshold_stopping_policy: MultiThresholdStoppingPolicy) -> None:
        """
        Tests the save_multi_threshold_stopping_policy function

        :param mocker: the pytest mocker object
        :param example_multi_threshold_stopping_policy: an example MultiThresholdStoppingPolicy object
        :return: None
        """
        id = 2
        example_multi_threshold_stopping_policy.id = id
        example_record = (id, example_multi_threshold_stopping_policy.simulation_name,
                          example_multi_threshold_stopping_policy.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_multi_threshold_stopping_policy(
            multi_threshold_stopping_policy=example_multi_threshold_stopping_policy)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE} "
            f"(id, policy, simulation_name) "
            f"VALUES (%s, %s, %s) RETURNING id", (id, example_multi_threshold_stopping_policy.to_json_str(),
                                                  example_multi_threshold_stopping_policy.simulation_name))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_convert_training_job_record_to_dto(self, example_training_job_config: TrainingJobConfig) -> None:
        """
        Tests the _convert_training_job_record_to_dto function

        :param example_training_job_config: an example TrainingJobConfig object
        :return: None
        """
        id = 1
        example_training_job_config.id = 1
        example_record = (id, example_training_job_config.to_dict())
        converted_object = MetastoreFacade._convert_training_job_record_to_dto(
            training_job_record=example_record)
        assert isinstance(converted_object, TrainingJobConfig)
        assert converted_object == example_training_job_config

    def test_list_training_jobs(self, mocker: pytest_mock.MockFixture,
                                example_training_job_config: TrainingJobConfig) -> None:
        """
        Tests the list_training_jobs function

        :param mocker: the pytest mocker object
        :param example_training_job_config: an example TrainingJobConfig object
        :return: None
        """
        id = 1
        example_training_job_config.id = id
        example_record = (id, example_training_job_config.to_dict(),
                          example_training_job_config.simulation_env_name,
                          example_training_job_config.emulation_env_name, example_training_job_config.pid)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        training_job = MetastoreFacade.list_training_jobs()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.TRAINING_JOBS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(training_job, list)
        assert isinstance(training_job[0], TrainingJobConfig)
        assert training_job[0] == example_training_job_config

    def test_list_training_jobs_ids(self, mocker: pytest_mock.MockFixture,
                                    example_training_job_config: TrainingJobConfig) -> None:
        """
        Tests the list_training_jobs_ids function

        :param mocker: the pytest mocker object
        :param example_training_job_config: TrainingJobConfig object
        :return: None
        """
        id = 1
        example_record = (id, "training_jobs_simulation1", "training_jobs_emulation1", 123)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        training_job_ids = MetastoreFacade.list_training_jobs_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,simulation_name,emulation_name,pid FROM "
            f"{constants.METADATA_STORE.TRAINING_JOBS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(training_job_ids, list)
        assert isinstance(training_job_ids[0], tuple)
        assert isinstance(training_job_ids[0][0], int)
        assert isinstance(training_job_ids[0][1], str)
        assert isinstance(training_job_ids[0][2], str)
        assert isinstance(training_job_ids[0][3], int)
        assert training_job_ids[0] == example_record

    def test_get_training_job_config(self, mocker: pytest_mock.MockFixture,
                                     example_training_job_config: TrainingJobConfig) -> None:
        """
        Tests the get_training_job_config function

        :param example_training_job_config: an example TrainingJobConfig object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_training_job_config.id = id
        example_record = (id, example_training_job_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_training_job_config = MetastoreFacade.get_training_job_config(
            id=example_training_job_config.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.TRAINING_JOBS_TABLE} WHERE id = %s",
            (example_training_job_config.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_training_job_config, TrainingJobConfig)
        assert fetched_training_job_config == example_training_job_config

    def test_save_training_job(self, mocker: pytest_mock.MockFixture,
                               example_training_job_config: TrainingJobConfig) -> None:
        """
        Tests the save_training_job function

        :param mocker: the pytest mocker object
        :param example_training_job_config: an example TrainingJobConfig object
        :return: None
        """
        id = 2
        example_training_job_config.id = id
        example_record = (id, example_training_job_config.to_dict(), example_training_job_config.simulation_env_name,
                          example_training_job_config.emulation_env_name, example_training_job_config.pid)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_training_job(training_job=example_training_job_config)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.TRAINING_JOBS_TABLE} "
            f"(id, config, simulation_name, emulation_name, pid) "
            f"VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (example_training_job_config.id, example_training_job_config.to_json_str(),
             example_training_job_config.simulation_env_name, example_training_job_config.emulation_env_name,
             example_training_job_config.pid))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_convert_data_collection_job_record_to_dto(self,
                                                       example_data_collection_job: DataCollectionJobConfig) -> None:
        """
        Tests the _convert_data_collection_job_record_to_dto function

        :param example_data_collection_job: an example DataCollectionJobConfig object
        :return: None
        """
        id = 1
        example_data_collection_job.id = 1
        example_record = (id, example_data_collection_job.to_dict())
        converted_object = MetastoreFacade._convert_data_collection_job_record_to_dto(
            data_collection_job_record=example_record)
        assert isinstance(converted_object, DataCollectionJobConfig)
        assert converted_object == example_data_collection_job

    def test_list_data_collection_jobs(self, mocker: pytest_mock.MockFixture,
                                       example_data_collection_job: DataCollectionJobConfig) -> None:
        """
        Tests the list_data_collection_jobs function

        :param mocker: the pytest mocker object
        :param example_data_collection_job: an example DataCollectionJobConfig object
        :return: None
        """
        id = 1
        example_data_collection_job.id = id
        example_record = (id, example_data_collection_job.to_dict(), example_data_collection_job.emulation_env_name,
                          example_data_collection_job.pid)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        data_collection_jobs = MetastoreFacade.list_data_collection_jobs()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(data_collection_jobs, list)
        assert isinstance(data_collection_jobs[0], DataCollectionJobConfig)
        assert data_collection_jobs[0] == example_data_collection_job

    def test_list_data_collection_jobs_ids(self, mocker: pytest_mock.MockFixture,
                                           example_data_collection_job: DataCollectionJobConfig) -> None:
        """
        Tests the list_data_collection_jobs_ids function

        :param mocker: the pytest mocker object
        :param example_data_collection_job: DataCollectionJobConfig object
        :return: None
        """
        id = 1
        example_record = (id, "training_jobs_emulation1", 123)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        data_collection_jobs_ids = MetastoreFacade.list_data_collection_jobs_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,emulation_name,pid FROM {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(data_collection_jobs_ids, list)
        assert isinstance(data_collection_jobs_ids[0], tuple)
        assert isinstance(data_collection_jobs_ids[0][0], int)
        assert isinstance(data_collection_jobs_ids[0][1], str)
        assert isinstance(data_collection_jobs_ids[0][2], int)
        assert data_collection_jobs_ids[0] == example_record

    def test_get_data_collection_job_config(self, mocker: pytest_mock.MockFixture,
                                            example_data_collection_job: DataCollectionJobConfig) -> None:
        """
        Tests the get_data_collection_job_config function

        :param example_data_collection_job: an example DataCollectionJobConfig object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_data_collection_job.id = id
        example_record = (id, example_data_collection_job.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_data_collection_job_config = MetastoreFacade.get_data_collection_job_config(
            id=example_data_collection_job.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE} WHERE id = %s",
            (example_data_collection_job.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_data_collection_job_config, DataCollectionJobConfig)
        assert fetched_data_collection_job_config == example_data_collection_job

    def test_save_data_collection_job(self, mocker: pytest_mock.MockFixture,
                                      example_data_collection_job: DataCollectionJobConfig) -> None:
        """
        Tests the save_data_collection_job function

        :param mocker: the pytest mocker object
        :param example_data_collection_job: an example DataCollectionJobConfig object
        :return: None
        """
        id = 2
        example_data_collection_job.id = id
        example_record = (id, example_data_collection_job.to_dict(), example_data_collection_job.emulation_env_name,
                          example_data_collection_job.pid)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_data_collection_job(data_collection_job=example_data_collection_job)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE} "
            f"(id, config, emulation_name, pid) "
            f"VALUES (%s, %s, %s, %s) RETURNING id",
            (id, example_data_collection_job.to_json_str(), example_data_collection_job.emulation_env_name,
             example_data_collection_job.pid))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_update_training_job(self, mocker: pytest_mock.MockFixture,
                                 example_training_job_config: TrainingJobConfig) -> None:
        """
        Tests the update_training_job function

        :param mocker: the pytest mocker object
        :param example_training_job_config: an example TrainingJobConfig object
        :return: None
        """
        id = 2
        example_training_job_config.id = id
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_training_job(id=id, training_job=example_training_job_config)
        mocked_cursor.execute.assert_called_once_with(f"UPDATE "
                                                      f"{constants.METADATA_STORE.TRAINING_JOBS_TABLE} "
                                                      f" SET config=%s "
                                                      f"WHERE {constants.METADATA_STORE.TRAINING_JOBS_TABLE}.id = %s",
                                                      (example_training_job_config.to_json_str(),
                                                       example_training_job_config.id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_update_experiment_execution(self, mocker: pytest_mock.MockFixture,
                                         example_experiment_execution: ExperimentExecution) -> None:
        """
        Tests the update_experiment_execution function

        :param mocker: the pytest mocker object
        :param example_experiment_execution: an example ExperimentExecution object
        :return: None
        """
        id = 2
        example_experiment_execution.id = id
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_experiment_execution(id=id, experiment_execution=example_experiment_execution)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE} "
            f" SET execution=%s "
            f"WHERE {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE}.id = %s",
            (example_experiment_execution.to_json_str(), example_experiment_execution.id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_update_data_collection_job(self, mocker: pytest_mock.MockFixture,
                                        example_data_collection_job: DataCollectionJobConfig) -> None:
        """
        Tests the update_data_collection_job function

        :param mocker: the pytest mocker object
        :param example_data_collection_job: an example DataCollectionJobConfig object
        :return: None
        """
        id = 2
        example_data_collection_job.id = id
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_data_collection_job(id=id, data_collection_job=example_data_collection_job)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE} "
            f" SET config=%s "
            f"WHERE {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE}.id = %s",
            (example_data_collection_job.to_json_str(), example_data_collection_job.id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_training_job(self, mocker: pytest_mock.MockFixture,
                                 example_training_job_config: TrainingJobConfig) -> None:
        """
        Tests the remove_training_job function

        :param mocker: the pytest mocker object
        :param example_training_job_config: an example TrainingJobConfig object
        :return: None
        """
        example_training_job_config.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_training_job(training_job=example_training_job_config)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.TRAINING_JOBS_TABLE} WHERE id = %s",
            (example_training_job_config.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_data_collection_job(self, mocker: pytest_mock.MockFixture,
                                        example_data_collection_job: DataCollectionJobConfig) -> None:
        """
        Tests the remove_data_collection_job function

        :param mocker: the pytest mocker object
        :param example_data_collection_job: an example DataCollectionJobConfig object
        :return: None
        """
        example_data_collection_job.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_data_collection_job(data_collection_job=example_data_collection_job)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE} WHERE id = %s",
            (example_data_collection_job.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_list_ppo_policies(self, mocker: pytest_mock.MockFixture, example_ppo_policy: PPOPolicy) -> None:
        """
        Tests the list_ppo_policies function

        :param mocker: the pytest mocker object
        :param example_ppo_policy: an example PPOPolicy object
        :return: None
        """
        id = 1
        example_ppo_policy.id = id
        example_record = (id, example_ppo_policy.to_dict(), example_ppo_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        ppo_policies = MetastoreFacade.list_ppo_policies()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.PPO_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(ppo_policies, list)
        assert isinstance(ppo_policies[0], PPOPolicy)
        assert ppo_policies[0] == example_ppo_policy

    def test_list_ppo_policies_ids(self, mocker: pytest_mock.MockFixture, example_ppo_policy: PPOPolicy) -> None:
        """
        Tests the list_ppo_policies_ids function

        :param mocker: the pytest mocker object
        :param example_ppo_policy: PPOPolicy object
        :return: None
        """
        id = 1
        example_record = (id, "training_jobs_emulation1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        ppo_policies_ids = MetastoreFacade.list_ppo_policies_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,simulation_name FROM {constants.METADATA_STORE.PPO_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(ppo_policies_ids, list)
        assert isinstance(ppo_policies_ids[0], tuple)
        assert isinstance(ppo_policies_ids[0][0], int)
        assert isinstance(ppo_policies_ids[0][1], str)
        assert ppo_policies_ids[0] == example_record

    def test_convert_ppo_policy_record_to_dto(self, example_ppo_policy: PPOPolicy) -> None:
        """
        Tests the _convert_ppo_policy_record_to_dto function

        :param example_ppo_policy: an example PPOPolicy object
        :return: None
        """
        id = 1
        example_ppo_policy.id = 1
        example_record = (id, example_ppo_policy.to_dict())
        converted_object = MetastoreFacade._convert_ppo_policy_record_to_dto(ppo_policy_record=example_record)
        assert isinstance(converted_object, PPOPolicy)
        assert converted_object == example_ppo_policy

    def test_get_ppo_policy(self, mocker: pytest_mock.MockFixture, example_ppo_policy: PPOPolicy) -> None:
        """
        Tests the get_ppo_policy function

        :param example_ppo_policy: an example PPOPolicy object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_ppo_policy.id = id
        example_record = (id, example_ppo_policy.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_ppo_policy = MetastoreFacade.get_ppo_policy(id=example_ppo_policy.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.PPO_POLICIES_TABLE} WHERE id = %s", (example_ppo_policy.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_ppo_policy, PPOPolicy)
        assert fetched_ppo_policy == example_ppo_policy

    def test_remove_ppo_policy(self, mocker: pytest_mock.MockFixture, example_ppo_policy: PPOPolicy) -> None:
        """
        Tests the remove_ppo_policy function

        :param mocker: the pytest mocker object
        :param example_ppo_policy: an example PPOPolicy object
        :return: None
        """
        example_ppo_policy.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_ppo_policy(ppo_policy=example_ppo_policy)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.PPO_POLICIES_TABLE} WHERE id = %s", (example_ppo_policy.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_save_ppo_policy(self, mocker: pytest_mock.MockFixture, example_ppo_policy: PPOPolicy) -> None:
        """
        Tests the save_ppo_policy function

        :param mocker: the pytest mocker object
        :param example_ppo_policy: an example PPOPolicy object
        :return: None
        """
        id = 2
        example_ppo_policy.id = id
        example_record = (id, example_ppo_policy.to_dict(), example_ppo_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_ppo_policy(ppo_policy=example_ppo_policy)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.PPO_POLICIES_TABLE} "
            f"(id, policy, simulation_name) "
            f"VALUES (%s, %s, %s) RETURNING id", (id, example_ppo_policy.to_json_str(),
                                                  example_ppo_policy.simulation_name))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_convert_system_identification_job_record_to_dto(
            self, example_system_identification_job_config: SystemIdentificationJobConfig) -> None:
        """
        Tests the _convert_system_identification_job_record_to_dto function

        :param example_system_identification_job_config: an example SystemIdentificationJobConfig object
        :return: None
        """
        id = 1
        example_system_identification_job_config.id = 1
        example_record = (id, example_system_identification_job_config.to_dict())
        converted_object = MetastoreFacade._convert_system_identification_job_record_to_dto(
            system_identification_job_record=example_record)
        assert isinstance(converted_object, SystemIdentificationJobConfig)
        assert converted_object == example_system_identification_job_config

    def test_list_system_identification_jobs(
            self, mocker: pytest_mock.MockFixture,
            example_system_identification_job_config: SystemIdentificationJobConfig) -> None:
        """
        Tests the list_system_identification_jobs function

        :param mocker: the pytest mocker object
        :param example_system_identification_job_config: an example SystemIdentificationJobConfig object
        :return: None
        """
        id = 1
        example_system_identification_job_config.id = id
        example_record = (id, example_system_identification_job_config.to_dict(),
                          example_system_identification_job_config.emulation_env_name,
                          example_system_identification_job_config.pid)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        system_identification_jobs = MetastoreFacade.list_system_identification_jobs()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(system_identification_jobs, list)
        assert isinstance(system_identification_jobs[0], SystemIdentificationJobConfig)
        assert system_identification_jobs[0] == example_system_identification_job_config

    def test_list_system_identification_jobs_ids(
            self, mocker: pytest_mock.MockFixture,
            example_system_identification_job_config: SystemIdentificationJobConfig) -> None:
        """
        Tests the list_system_identification_jobs_ids function

        :param mocker: the pytest mocker object
        :param example_system_identification_job_config: SystemIdentificationJobConfig object
        :return: None
        """
        id = 1
        example_record = (id, "system_identification_job1", 123)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        system_identification_jobs_ids = MetastoreFacade.list_system_identification_jobs_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(f"SELECT id,emulation_name,pid FROM "
                                                      f"{constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(system_identification_jobs_ids, list)
        assert isinstance(system_identification_jobs_ids[0], tuple)
        assert isinstance(system_identification_jobs_ids[0][0], int)
        assert isinstance(system_identification_jobs_ids[0][1], str)
        assert isinstance(system_identification_jobs_ids[0][2], int)
        assert system_identification_jobs_ids[0] == example_record

    def test_get_system_identification_job_config(
            self, mocker: pytest_mock.MockFixture,
            example_system_identification_job_config: SystemIdentificationJobConfig) -> None:
        """
        Tests the get_system_identification_job_config function

        :param example_system_identification_job_config: an example SystemIdentificationJobConfig object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_system_identification_job_config.id = id
        example_record = (id, example_system_identification_job_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_system_identification_job = MetastoreFacade.get_system_identification_job_config(
            id=example_system_identification_job_config.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM "
            f"{constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE} WHERE id = %s",
            (example_system_identification_job_config.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_system_identification_job, SystemIdentificationJobConfig)
        assert fetched_system_identification_job == example_system_identification_job_config

    def test_save_system_identification_job(
            self, mocker: pytest_mock.MockFixture,
            example_system_identification_job_config: SystemIdentificationJobConfig) -> None:
        """
        Tests the save_system_identification_job function

        :param mocker: the pytest mocker object
        :param example_system_identification_job_config: an example SystemIdentificationJobConfig object
        :return: None
        """
        id = 2
        example_system_identification_job_config.id = id
        example_record = (id, example_system_identification_job_config.to_dict(),
                          example_system_identification_job_config.emulation_env_name,
                          example_system_identification_job_config.pid)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_system_identification_job(
            system_identification_job=example_system_identification_job_config)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE} "
            f"(id, config, emulation_name, pid) "
            f"VALUES (%s, %s, %s, %s) RETURNING id", (example_system_identification_job_config.id,
                                                      example_system_identification_job_config.to_json_str(),
                                                      example_system_identification_job_config.emulation_env_name,
                                                      example_system_identification_job_config.pid))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_update_system_identification_job(
            self, mocker: pytest_mock.MockFixture,
            example_system_identification_job_config: SystemIdentificationJobConfig) -> None:
        """
        Tests the update_system_identification_job function

        :param mocker: the pytest mocker object
        :param example_system_identification_job_config: an example SystemIdentificationJobConfig object
        :return: None
        """
        id = 2
        example_system_identification_job_config.id = id
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_system_identification_job(
            id=id, system_identification_job=example_system_identification_job_config)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE} "
            f" SET config=%s "
            f"WHERE {constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE}.id = %s",
            (example_system_identification_job_config.to_json_str(), example_system_identification_job_config.id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_system_identification_job(
            self, mocker: pytest_mock.MockFixture,
            example_system_identification_job_config: SystemIdentificationJobConfig) -> None:
        """
        Tests the remove_system_identification_job function

        :param mocker: the pytest mocker object
        :param example_system_identification_job_config: an example SystemIdentificationJobConfig object
        :return: None
        """
        example_system_identification_job_config.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_system_identification_job(
            system_identification_job=example_system_identification_job_config)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE} WHERE id = %s",
            (example_system_identification_job_config.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_convert_gaussian_mixture_system_model_record_to_dto(
            self, example_gaussian_mixture_system_model: GaussianMixtureSystemModel) -> None:
        """
        Tests the _convert_gaussian_mixture_system_model_record_to_dto function

        :param example_gaussian_mixture_system_model: an example GaussianMixtureSystemModel object
        :return: None
        """
        id = 1
        example_gaussian_mixture_system_model.id = 1
        example_record = (id, example_gaussian_mixture_system_model.to_dict())
        converted_object = MetastoreFacade._convert_gaussian_mixture_system_model_record_to_dto(
            gaussian_mixture_system_model_record=example_record)
        assert isinstance(converted_object, GaussianMixtureSystemModel)
        assert converted_object == example_gaussian_mixture_system_model

    def test_list_gaussian_mixture_system_models(
            self, mocker: pytest_mock.MockFixture,
            example_gaussian_mixture_system_model: GaussianMixtureSystemModel) -> None:
        """
        Tests the list_gaussian_mixture_system_models function

        :param mocker: the pytest mocker object
        :param example_gaussian_mixture_system_model: an example GaussianMixtureSystemModel object
        :return: None
        """
        id = 1
        example_gaussian_mixture_system_model.id = id
        example_record = (id, example_gaussian_mixture_system_model.to_dict(),
                          example_gaussian_mixture_system_model.emulation_env_name,
                          example_gaussian_mixture_system_model.emulation_statistic_id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        gaussian_mixture_system_models = MetastoreFacade.list_gaussian_mixture_system_models()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(gaussian_mixture_system_models, list)
        assert isinstance(gaussian_mixture_system_models[0], GaussianMixtureSystemModel)
        assert gaussian_mixture_system_models[0] == example_gaussian_mixture_system_model

    def test_list_gaussian_mixture_system_models_ids(
            self, mocker: pytest_mock.MockFixture,
            example_gaussian_mixture_system_model: GaussianMixtureSystemModel) -> None:
        """
        Tests the list_gaussian_mixture_system_models_ids function

        :param mocker: the pytest mocker object
        :param example_gaussian_mixture_system_model: GaussianMixtureSystemModel object
        :return: None
        """
        id = 1
        example_record = (id, "emulation_name1", 123)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        gaussian_mixture_system_models_ids = MetastoreFacade.list_gaussian_mixture_system_models_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,emulation_name,emulation_statistic_id FROM "
            f"{constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(gaussian_mixture_system_models_ids, list)
        assert isinstance(gaussian_mixture_system_models_ids[0], tuple)
        assert isinstance(gaussian_mixture_system_models_ids[0][0], int)
        assert isinstance(gaussian_mixture_system_models_ids[0][1], str)
        assert isinstance(gaussian_mixture_system_models_ids[0][2], int)
        assert gaussian_mixture_system_models_ids[0] == example_record

    def test_get_gaussian_mixture_system_model_config(
            self, mocker: pytest_mock.MockFixture,
            example_gaussian_mixture_system_model: GaussianMixtureSystemModel) -> None:
        """
        Tests the get_gaussian_mixture_system_model_config function

        :param example_gaussian_mixture_system_model: an example GaussianMixtureSystemModel object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_gaussian_mixture_system_model.id = id
        example_record = (id, example_gaussian_mixture_system_model.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_gaussian_mixture_system_model = MetastoreFacade.get_gaussian_mixture_system_model_config(
            id=example_gaussian_mixture_system_model.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} "
            f"WHERE id = %s", (example_gaussian_mixture_system_model.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_gaussian_mixture_system_model, GaussianMixtureSystemModel)
        assert fetched_gaussian_mixture_system_model == example_gaussian_mixture_system_model

    def test_save_gaussian_mixture_system_model(
            self, mocker: pytest_mock.MockFixture,
            example_gaussian_mixture_system_model: GaussianMixtureSystemModel) -> None:
        """
        Tests the save_gaussian_mixture_system_model function

        :param mocker: the pytest mocker object
        :param example_gaussian_mixture_system_model: an example GaussianMixtureSystemModel object
        :return: None
        """
        id = 2
        example_gaussian_mixture_system_model.id = id
        example_record = (example_gaussian_mixture_system_model.id, example_gaussian_mixture_system_model.to_dict(),
                          example_gaussian_mixture_system_model.emulation_env_name,
                          example_gaussian_mixture_system_model.emulation_statistic_id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_gaussian_mixture_system_model(
            gaussian_mixture_system_model=example_gaussian_mixture_system_model)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} "
            f"(id, model, emulation_name, emulation_statistic_id) "
            f"VALUES (%s, %s, %s, %s) RETURNING id",
            (example_gaussian_mixture_system_model.id, example_gaussian_mixture_system_model.to_json_str(),
             example_gaussian_mixture_system_model.emulation_env_name,
             example_gaussian_mixture_system_model.emulation_statistic_id))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_update_gaussian_mixture_system_model(
            self, mocker: pytest_mock.MockFixture,
            example_gaussian_mixture_system_model: GaussianMixtureSystemModel) -> None:
        """
        Tests the update_gaussian_mixture_system_model function

        :param mocker: the pytest mocker object
        :param example_gaussian_mixture_system_model: an example GaussianMixtureSystemModel object
        :return: None
        """
        id = 2
        example_gaussian_mixture_system_model.id = id
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_gaussian_mixture_system_model(
            id=id, gaussian_mixture_system_model=example_gaussian_mixture_system_model)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} "
            f" SET config=%s "
            f"WHERE {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE}.id = %s",
            (example_gaussian_mixture_system_model.to_json_str(), example_gaussian_mixture_system_model.id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_gaussian_mixture_system_model(
            self, mocker: pytest_mock.MockFixture,
            example_gaussian_mixture_system_model: GaussianMixtureSystemModel) -> None:
        """
        Tests the remove_gaussian_mixture_system_model function

        :param mocker: the pytest mocker object
        :param example_gaussian_mixture_system_model: an example GaussianMixtureSystemModel object
        :return: None
        """
        example_gaussian_mixture_system_model.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_gaussian_mixture_system_model(
            gaussian_mixture_system_model=example_gaussian_mixture_system_model)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} "
            f"WHERE id = %s", (example_gaussian_mixture_system_model.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_list_tabular_policies(self, mocker: pytest_mock.MockFixture,
                                   example_tabular_policy: TabularPolicy) -> None:
        """
        Tests the list_tabular_policies function

        :param mocker: the pytest mocker object
        :param example_tabular_policy: an example TabularPolicy object
        :return: None
        """
        id = 1
        example_tabular_policy.id = id
        example_record = (id, example_tabular_policy.to_dict(), example_tabular_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        tabular_policies = MetastoreFacade.list_tabular_policies()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.TABULAR_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(tabular_policies, list)
        assert isinstance(tabular_policies[0], TabularPolicy)
        assert tabular_policies[0] == example_tabular_policy

    def test_list_tabular_policies_ids(self, mocker: pytest_mock.MockFixture,
                                       example_tabular_policy: TabularPolicy) -> None:
        """
        Tests the list_tabular_policies_ids function

        :param mocker: the pytest mocker object
        :param example_tabular_policy: TabularPolicy object
        :return: None
        """
        id = 1
        example_record = (id, "simulation_name1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        tabular_policies_ids = MetastoreFacade.list_tabular_policies_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,simulation_name FROM {constants.METADATA_STORE.TABULAR_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(tabular_policies_ids, list)
        assert isinstance(tabular_policies_ids[0], tuple)
        assert isinstance(tabular_policies_ids[0][0], int)
        assert isinstance(tabular_policies_ids[0][1], str)
        assert tabular_policies_ids[0] == example_record

    def test_convert_tabular_policy_record_to_dto(self, example_tabular_policy: TabularPolicy) -> None:
        """
        Tests the _convert_tabular_policy_record_to_dto function

        :param example_tabular_policy: an example TabularPolicy object
        :return: None
        """
        id = 1
        example_tabular_policy.id = 1
        example_record = (id, example_tabular_policy.to_dict())
        converted_object = MetastoreFacade._convert_tabular_policy_record_to_dto(tabular_policy_record=example_record)
        assert isinstance(converted_object, TabularPolicy)
        assert converted_object == example_tabular_policy

    def test_get_tabular_policy(self, mocker: pytest_mock.MockFixture, example_tabular_policy: TabularPolicy) -> None:
        """
        Tests the get_tabular_policy function

        :param example_tabular_policy: an example TabularPolicy object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_tabular_policy.id = id
        example_record = (id, example_tabular_policy.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_tabular_policy = MetastoreFacade.get_tabular_policy(id=example_tabular_policy.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.TABULAR_POLICIES_TABLE} WHERE id = %s",
            (example_tabular_policy.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_tabular_policy, TabularPolicy)
        assert fetched_tabular_policy == example_tabular_policy

    def test_remove_tabular_policy(self, mocker: pytest_mock.MockFixture,
                                   example_tabular_policy: TabularPolicy) -> None:
        """
        Tests the remove_tabular_policy function

        :param mocker: the pytest mocker object
        :param example_tabular_policy: an example TabularPolicy object
        :return: None
        """
        example_tabular_policy.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_tabular_policy(tabular_policy=example_tabular_policy)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.TABULAR_POLICIES_TABLE} WHERE id = %s",
            (example_tabular_policy.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_save_tabular_policy(self, mocker: pytest_mock.MockFixture, example_tabular_policy: TabularPolicy) -> None:
        """
        Tests the save_tabular_policy function

        :param mocker: the pytest mocker object
        :param example_tabular_policy: an example TabularPolicy object
        :return: None
        """
        id = 2
        example_tabular_policy.id = id
        example_record = (example_tabular_policy.id, example_tabular_policy.to_dict(),
                          example_tabular_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_tabular_policy(tabular_policy=example_tabular_policy)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.TABULAR_POLICIES_TABLE} "
            f"(id, policy, simulation_name) "
            f"VALUES (%s, %s, %s) RETURNING id", (example_tabular_policy.id, example_tabular_policy.to_json_str(),
                                                  example_tabular_policy.simulation_name))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_list_alpha_vec_policies(self, mocker: pytest_mock.MockFixture,
                                     example_alpha_vectors_policy: AlphaVectorsPolicy) -> None:
        """
        Tests the list_alpha_vec_policies function

        :param mocker: the pytest mocker object
        :param example_alpha_vec_policies: an example AlphaVectorsPolicy object
        :return: None
        """
        id = 1
        example_alpha_vectors_policy.id = id
        example_record = (id, example_alpha_vectors_policy.to_dict(), example_alpha_vectors_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        alpha_vec_policies = MetastoreFacade.list_alpha_vec_policies()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.ALPHA_VEC_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(alpha_vec_policies, list)
        assert isinstance(alpha_vec_policies[0], AlphaVectorsPolicy)
        assert alpha_vec_policies[0] == example_alpha_vectors_policy

    def test_list_alpha_vec_policies_ids(self, mocker: pytest_mock.MockFixture,
                                         example_alpha_vectors_policy: AlphaVectorsPolicy) -> None:
        """
        Tests the list_alpha_vec_policies_ids function

        :param mocker: the pytest mocker object
        :param example_alpha_vectors_policy: AlphaVectorsPolicy object
        :return: None
        """
        id = 1
        example_record = (id, "simulation_name1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        alpha_vectors_policy_ids = MetastoreFacade.list_alpha_vec_policies_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,simulation_name FROM {constants.METADATA_STORE.ALPHA_VEC_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(alpha_vectors_policy_ids, list)
        assert isinstance(alpha_vectors_policy_ids[0], tuple)
        assert isinstance(alpha_vectors_policy_ids[0][0], int)
        assert isinstance(alpha_vectors_policy_ids[0][1], str)
        assert alpha_vectors_policy_ids[0] == example_record

    def test_convert_alpha_vec_policy_record_to_dto(self, example_alpha_vectors_policy: AlphaVectorsPolicy) -> None:
        """
        Tests the _convert_alpha_vec_policy_record_to_dto function

        :param example_alpha_vectors_policy: an example AlphaVectorsPolicy object
        :return: None
        """
        id = 1
        example_alpha_vectors_policy.id = 1
        example_record = (id, example_alpha_vectors_policy.to_dict())
        converted_object = MetastoreFacade._convert_alpha_vec_policy_record_to_dto(
            alpha_vec_policy_record=example_record)
        assert isinstance(converted_object, AlphaVectorsPolicy)
        assert converted_object == example_alpha_vectors_policy

    def test_get_alpha_vec_policy(self, mocker: pytest_mock.MockFixture,
                                  example_alpha_vectors_policy: AlphaVectorsPolicy) -> None:
        """
        Tests the get_alpha_vec_policy function

        :param example_alpha_vectors_policy: an example AlphaVectorsPolicy object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_alpha_vectors_policy.id = id
        example_record = (id, example_alpha_vectors_policy.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_alpha_vec_policy = MetastoreFacade.get_alpha_vec_policy(id=example_alpha_vectors_policy.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.ALPHA_VEC_POLICIES_TABLE} WHERE id = %s",
            (example_alpha_vectors_policy.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_alpha_vec_policy, AlphaVectorsPolicy)
        assert fetched_alpha_vec_policy == example_alpha_vectors_policy

    def test_remove_alpha_vec_policy(self, mocker: pytest_mock.MockFixture,
                                     example_alpha_vectors_policy: AlphaVectorsPolicy) -> None:
        """
        Tests the remove_alpha_vec_policy function

        :param mocker: the pytest mocker object
        :param example_alpha_vectors_policy: an example AlphaVectorsPolicy object
        :return: None
        """
        example_alpha_vectors_policy.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_alpha_vec_policy(alpha_vec_policy=example_alpha_vectors_policy)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.ALPHA_VEC_POLICIES_TABLE} WHERE id = %s",
            (example_alpha_vectors_policy.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_save_alpha_vec_policy(self, mocker: pytest_mock.MockFixture,
                                   example_alpha_vectors_policy: AlphaVectorsPolicy) -> None:
        """
        Tests the save_alpha_vec_policy function

        :param mocker: the pytest mocker object
        :param example_alpha_vectors_policy: an example AlphaVectorsPolicy object
        :return: None
        """
        id = 2
        example_alpha_vectors_policy.id = id
        example_record = (example_alpha_vectors_policy.id, example_alpha_vectors_policy.to_dict(),
                          example_alpha_vectors_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_alpha_vec_policy(alpha_vec_policy=example_alpha_vectors_policy)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.ALPHA_VEC_POLICIES_TABLE} "
            f"(id, policy, simulation_name) "
            f"VALUES (%s, %s, %s) RETURNING id", (id, example_alpha_vectors_policy.to_json_str(),
                                                  example_alpha_vectors_policy.simulation_name))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_list_dqn_policies(self, mocker: pytest_mock.MockFixture, example_dqn_policy: DQNPolicy) -> None:
        """
        Tests the list_dqn_policies function

        :param mocker: the pytest mocker object
        :param example_dqn_policy: an example DQNPolicy object
        :return: None
        """
        id = 1
        example_dqn_policy.id = id
        example_record = (id, example_dqn_policy.to_dict(), example_dqn_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        dqn_policies = MetastoreFacade.list_dqn_policies()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.DQN_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(dqn_policies, list)
        assert isinstance(dqn_policies[0], DQNPolicy)
        assert dqn_policies[0] == example_dqn_policy

    def test_list_dqn_policies_ids(self, mocker: pytest_mock.MockFixture, example_dqn_policy: DQNPolicy) -> None:
        """
        Tests the list_dqn_policies_ids function

        :param mocker: the pytest mocker object
        :param example_dqn_policy: DQNPolicy object
        :return: None
        """
        id = 1
        example_record = (id, "simulation_name1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        dqn_policies_ids = MetastoreFacade.list_dqn_policies_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,simulation_name FROM {constants.METADATA_STORE.DQN_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(dqn_policies_ids, list)
        assert isinstance(dqn_policies_ids[0], tuple)
        assert isinstance(dqn_policies_ids[0][0], int)
        assert isinstance(dqn_policies_ids[0][1], str)
        assert dqn_policies_ids[0] == example_record

    def test_convert_dqn_policy_record_to_dto(self, example_dqn_policy: DQNPolicy) -> None:
        """
        Tests the _convert_dqn_policy_record_to_dto function

        :param example_dqn_policy: an example DQNPolicy object
        :return: None
        """
        id = 1
        example_dqn_policy.id = 1
        example_record = (id, example_dqn_policy.to_dict())
        converted_object = MetastoreFacade._convert_dqn_policy_record_to_dto(dqn_policy_record=example_record)
        assert isinstance(converted_object, DQNPolicy)
        assert converted_object == example_dqn_policy

    def test_get_dqn_policy(self, mocker: pytest_mock.MockFixture, example_dqn_policy: DQNPolicy) -> None:
        """
        Tests the get_dqn_policy function

        :param example_dqn_policy: an example DQNPolicy object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_dqn_policy.id = id
        example_record = (id, example_dqn_policy.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_dqn_policy = MetastoreFacade.get_dqn_policy(id=example_dqn_policy.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.DQN_POLICIES_TABLE} WHERE id = %s", (example_dqn_policy.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_dqn_policy, DQNPolicy)
        assert fetched_dqn_policy == example_dqn_policy

    def test_remove_dqn_policy(self, mocker: pytest_mock.MockFixture, example_dqn_policy: DQNPolicy) -> None:
        """
        Tests the remove_dqn_policy function

        :param mocker: the pytest mocker object
        :param example_dqn_policy: an example DQNPolicy object
        :return: None
        """
        example_dqn_policy.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_dqn_policy(dqn_policy=example_dqn_policy)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.DQN_POLICIES_TABLE} WHERE id = %s", (example_dqn_policy.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_save_dqn_policy(self, mocker: pytest_mock.MockFixture, example_dqn_policy: DQNPolicy) -> None:
        """
        Tests the save_dqn_policy function

        :param mocker: the pytest mocker object
        :param example_dqn_policy: an example DQNPolicy object
        :return: None
        """
        id = 2
        example_dqn_policy.id = id
        example_record = (example_dqn_policy.id, example_dqn_policy.to_dict(), example_dqn_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_dqn_policy(dqn_policy=example_dqn_policy)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.DQN_POLICIES_TABLE} "
            f"(id, policy, simulation_name) "
            f"VALUES (%s, %s, %s) RETURNING id", (example_dqn_policy.id, example_dqn_policy.to_json_str(),
                                                  example_dqn_policy.simulation_name))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_list_fnn_w_softmax_policies(self, mocker: pytest_mock.MockFixture,
                                         example_fnn_with_softmax_policy: FNNWithSoftmaxPolicy) -> None:
        """
        Tests the list_fnn_w_softmax_policies function

        :param mocker: the pytest mocker object
        :param example_fnn_with_softmax_policy: an example FNNWithSoftmaxPolicy object
        :return: None
        """
        id = 1
        example_fnn_with_softmax_policy.id = id
        example_record = (id, example_fnn_with_softmax_policy.to_dict(),
                          example_fnn_with_softmax_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fnn_w_softmax_policies = MetastoreFacade.list_fnn_w_softmax_policies()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.FNN_W_SOFTMAX_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(fnn_w_softmax_policies, list)
        assert isinstance(fnn_w_softmax_policies[0], FNNWithSoftmaxPolicy)
        assert fnn_w_softmax_policies[0] == example_fnn_with_softmax_policy

    def test_list_fnn_w_softmax_policies_ids(self, mocker: pytest_mock.MockFixture,
                                             example_fnn_with_softmax_policy: FNNWithSoftmaxPolicy) -> None:
        """
        Tests the list_fnn_w_softmax_policies_ids function

        :param mocker: the pytest mocker object
        :param example_fnn_with_softmax_policy: FNNWithSoftmaxPolicy object
        :return: None
        """
        id = 1
        example_record = (id, "simulation_name1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fnn_w_softmax_policies_ids = MetastoreFacade.list_fnn_w_softmax_policies_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,simulation_name FROM {constants.METADATA_STORE.FNN_W_SOFTMAX_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(fnn_w_softmax_policies_ids, list)
        assert isinstance(fnn_w_softmax_policies_ids[0], tuple)
        assert isinstance(fnn_w_softmax_policies_ids[0][0], int)
        assert isinstance(fnn_w_softmax_policies_ids[0][1], str)
        assert fnn_w_softmax_policies_ids[0] == example_record

    def test_convert_fnn_w_softmax_policy_record_to_dto(self,
                                                        example_fnn_with_softmax_policy: FNNWithSoftmaxPolicy) -> None:
        """
        Tests the _convert_fnn_w_softmax_policy_record_to_dto function

        :param example_fnn_with_softmax_policy: an example FNNWithSoftmaxPolicy object
        :return: None
        """
        id = 1
        example_fnn_with_softmax_policy.id = 1
        example_record = (id, example_fnn_with_softmax_policy.to_dict())
        converted_object = MetastoreFacade._convert_fnn_w_softmax_policy_record_to_dto(
            fnn_w_softmax_policy_record=example_record)
        assert isinstance(converted_object, FNNWithSoftmaxPolicy)
        assert converted_object == example_fnn_with_softmax_policy

    def test_get_fnn_w_softmax_policy(self, mocker: pytest_mock.MockFixture,
                                      example_fnn_with_softmax_policy: FNNWithSoftmaxPolicy) -> None:
        """
        Tests the get_fnn_w_softmax_policy function

        :param example_fnn_with_softmax_policy: an example FNNWithSoftmaxPolicy object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_fnn_with_softmax_policy.id = id
        example_record = (id, example_fnn_with_softmax_policy.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_fnn_with_softmax_policy = MetastoreFacade.get_fnn_w_softmax_policy(
            id=example_fnn_with_softmax_policy.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.FNN_W_SOFTMAX_POLICIES_TABLE} "
            f"WHERE id = %s", (example_fnn_with_softmax_policy.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_fnn_with_softmax_policy, FNNWithSoftmaxPolicy)
        assert fetched_fnn_with_softmax_policy == example_fnn_with_softmax_policy

    def test_remove_fnn_w_softmax_policy(self, mocker: pytest_mock.MockFixture,
                                         example_fnn_with_softmax_policy: FNNWithSoftmaxPolicy) -> None:
        """
        Tests the remove_fnn_w_softmax_policy function

        :param mocker: the pytest mocker object
        :param example_fnn_with_softmax_policy: an example FNNWithSoftmaxPolicy object
        :return: None
        """
        example_fnn_with_softmax_policy.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_fnn_w_softmax_policy(fnn_w_softmax_policy=example_fnn_with_softmax_policy)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.FNN_W_SOFTMAX_POLICIES_TABLE} WHERE id = %s",
            (example_fnn_with_softmax_policy.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_save_fnn_w_softmax_policy(self, mocker: pytest_mock.MockFixture,
                                       example_fnn_with_softmax_policy: FNNWithSoftmaxPolicy) -> None:
        """
        Tests the save_fnn_w_softmax_policy function

        :param mocker: the pytest mocker object
        :param example_fnn_with_softmax_policy: an example FNNWithSoftmaxPolicy object
        :return: None
        """
        id = 2
        example_fnn_with_softmax_policy.id = id
        example_record = (example_fnn_with_softmax_policy.id, example_fnn_with_softmax_policy.to_dict(),
                          example_fnn_with_softmax_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_fnn_w_softmax_policy(fnn_w_softmax_policy=example_fnn_with_softmax_policy)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.FNN_W_SOFTMAX_POLICIES_TABLE} "
            f"(id, policy, simulation_name) "
            f"VALUES (%s, %s, %s) RETURNING id", (example_fnn_with_softmax_policy.id,
                                                  example_fnn_with_softmax_policy.to_json_str(),
                                                  example_fnn_with_softmax_policy.simulation_name))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_list_vector_policies(self, mocker: pytest_mock.MockFixture,
                                  example_vector_policy: VectorPolicy) -> None:
        """
        Tests the list_vector_policies function

        :param mocker: the pytest mocker object
        :param example_vector_policy: an example VectorPolicy object
        :return: None
        """
        id = 1
        example_vector_policy.id = id
        example_record = (id, example_vector_policy.to_dict(), example_vector_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        vector_policies = MetastoreFacade.list_vector_policies()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.VECTOR_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(vector_policies, list)
        assert isinstance(vector_policies[0], VectorPolicy)
        assert vector_policies[0] == example_vector_policy

    def test_list_vector_policies_ids(self, mocker: pytest_mock.MockFixture,
                                      example_vector_policy: VectorPolicy) -> None:
        """
        Tests the list_vector_policies_ids function

        :param mocker: the pytest mocker object
        :param example_vector_policy: VectorPolicy object
        :return: None
        """
        id = 1
        example_record = (id, "simulation_name1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        vector_policies_ids = MetastoreFacade.list_vector_policies_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,simulation_name FROM {constants.METADATA_STORE.VECTOR_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(vector_policies_ids, list)
        assert isinstance(vector_policies_ids[0], tuple)
        assert isinstance(vector_policies_ids[0][0], int)
        assert isinstance(vector_policies_ids[0][1], str)
        assert vector_policies_ids[0] == example_record

    def test_convert_vector_policy_record_to_dto(self, example_vector_policy: VectorPolicy) -> None:
        """
        Tests the _convert_vector_policy_record_to_dto function

        :param example_vector_policy: an example VectorPolicy object
        :return: None
        """
        id = 1
        example_vector_policy.id = 1
        example_record = (id, example_vector_policy.to_dict())
        converted_object = MetastoreFacade._convert_vector_policy_record_to_dto(vector_policy_record=example_record)
        assert isinstance(converted_object, VectorPolicy)
        assert converted_object == example_vector_policy

    def test_get_vector_policy(self, mocker: pytest_mock.MockFixture,
                               example_vector_policy: VectorPolicy) -> None:
        """
        Tests the get_vector_policy function

        :param example_vector_policy: an example VectorPolicy object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_vector_policy.id = id
        example_record = (id, example_vector_policy.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_vector_policy = MetastoreFacade.get_vector_policy(id=example_vector_policy.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.VECTOR_POLICIES_TABLE} WHERE id = %s",
            (example_vector_policy.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_vector_policy, VectorPolicy)
        assert fetched_vector_policy == example_vector_policy

    def test_remove_vector_policy(self, mocker: pytest_mock.MockFixture,
                                  example_vector_policy: VectorPolicy) -> None:
        """
        Tests the remove_vector_policy function

        :param mocker: the pytest mocker object
        :param example_vector_policy: an example VectorPolicy object
        :return: None
        """
        example_vector_policy.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_vector_policy(vector_policy=example_vector_policy)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.VECTOR_POLICIES_TABLE} WHERE id = %s",
            (example_vector_policy.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_save_vector_policy(self, mocker: pytest_mock.MockFixture, example_vector_policy: VectorPolicy) -> None:
        """
        Tests the save_vector_policy function

        :param mocker: the pytest mocker object
        :param example_vector_policy: an example VectorPolicy object
        :return: None
        """
        id = 2
        example_vector_policy.id = id
        example_record = (example_vector_policy.id, example_vector_policy.to_dict(),
                          example_vector_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_vector_policy(vector_policy=example_vector_policy)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.VECTOR_POLICIES_TABLE} "
            f"(id, policy, simulation_name) "
            f"VALUES (%s, %s, %s) RETURNING id", (example_vector_policy.id, example_vector_policy.to_json_str(),
                                                  example_vector_policy.simulation_name))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_list_emulation_execution_ids(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the list_emulation_execution_ids function

        :param mocker: the pytest mocker object
        :param example_emulation_execution: EmulationExecution object
        :return: None
        """
        ip_first_octet = 1
        example_record = (ip_first_octet, "emulation_name1")
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_execution_ids = MetastoreFacade.list_emulation_execution_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT ip_first_octet,emulation_name FROM "
            f"{constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_execution_ids, list)
        assert isinstance(emulation_execution_ids[0], tuple)
        assert isinstance(emulation_execution_ids[0][0], int)
        assert isinstance(emulation_execution_ids[0][1], str)
        assert emulation_execution_ids[0] == example_record

    def test_list_emulation_executions(self, mocker: pytest_mock.MockFixture,
                                       example_emulation_execution: EmulationExecution) -> None:
        """
        Tests the list_emulation_executions function

        :param mocker: the pytest mocker object
        :param example_fnn_with_softmax_policy: an example EmulationExecution object
        :return: None
        """
        id = 1
        example_emulation_execution.id = id
        mocker.patch('csle_common.dao.emulation_config.emulation_execution.EmulationExecution.from_dict',
                     return_value=example_emulation_execution)
        example_record = (id, example_emulation_execution.to_dict(), example_emulation_execution.emulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_executions = MetastoreFacade.list_emulation_executions()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_executions, list)
        assert isinstance(emulation_executions[0], EmulationExecution)
        assert emulation_executions[0] == example_emulation_execution

    def test_list_emulation_executions_for_a_given_emulation(self, mocker: pytest_mock.MockFixture,
                                                             example_emulation_execution: EmulationExecution) -> None:
        """
        Tests the list_emulation_executions_for_a_given_emulation function

        :param mocker: the pytest mocker object
        :param example_emulation_execution: EmulationExecution object
        :return: None
        """
        mocker.patch('csle_common.dao.emulation_config.emulation_execution.EmulationExecution.from_dict',
                     return_value=example_emulation_execution)
        example_recored = (example_emulation_execution.ip_first_octet, example_emulation_execution.emulation_name,
                           example_emulation_execution.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_recored]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_execution = MetastoreFacade.list_emulation_executions_for_a_given_emulation(
            emulation_name=example_emulation_execution.emulation_name)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
            f"WHERE emulation_name = %s", (example_emulation_execution.emulation_name,))
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_execution, list)
        assert isinstance(emulation_execution[0], EmulationExecution)
        assert emulation_execution[0] == example_emulation_execution

    def test_list_emulation_executions_by_id(self, mocker: pytest_mock.MockFixture,
                                             example_emulation_execution: EmulationExecution) -> None:
        """
        Tests the list_emulation_executions_by_id function

        :param mocker: the pytest mocker object
        :param example_emulation_execution: EmulationExecution object
        :return: None
        """
        mocker.patch('csle_common.dao.emulation_config.emulation_execution.EmulationExecution.from_dict',
                     return_value=example_emulation_execution)
        example_recored = (example_emulation_execution.ip_first_octet, example_emulation_execution.emulation_name,
                           example_emulation_execution.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_recored]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        emulation_execution = MetastoreFacade.list_emulation_executions_by_id(
            id=example_emulation_execution.ip_first_octet)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
            f"WHERE ip_first_octet = %s", (example_emulation_execution.ip_first_octet,))
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(emulation_execution, list)
        assert isinstance(emulation_execution[0], EmulationExecution)
        assert emulation_execution[0] == example_emulation_execution

    def test_convert_emulation_execution_record_to_dto(self, mocker: pytest_mock.MockFixture,
                                                       example_emulation_execution: EmulationExecution) -> None:
        """
        Tests the _convert_emulation_execution_record_to_dto function

        :param example_emulation_execution: an example EmulationExecution object
        :return: None
        """
        id = 1
        mocker.patch('csle_common.dao.emulation_config.emulation_execution.EmulationExecution.from_dict',
                     return_value=example_emulation_execution)
        example_emulation_execution.id = 1
        example_record = (id, example_emulation_execution.emulation_name, example_emulation_execution.to_dict())
        converted_object = MetastoreFacade._convert_emulation_execution_record_to_dto(
            emulation_execution_record=example_record)
        assert isinstance(converted_object, EmulationExecution)
        assert converted_object == example_emulation_execution

    def test_get_emulation_execution(self, mocker: pytest_mock.MockFixture,
                                     example_emulation_execution: EmulationExecution) -> None:
        """
        Tests the get_emulation_execution function

        :param example_emulation_execution: an example EmulationExecution object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        mocker.patch('csle_common.dao.emulation_config.emulation_execution.EmulationExecution.from_dict',
                     return_value=example_emulation_execution)
        example_emulation_execution.ip_first_octet = id
        example_record = (id, example_emulation_execution.emulation_name, example_emulation_execution.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        fetched_emulation_execution = MetastoreFacade.get_emulation_execution(
            ip_first_octet=example_emulation_execution.ip_first_octet,
            emulation_name=example_emulation_execution.emulation_name)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
            f"WHERE ip_first_octet = %s AND emulation_name=%s", (example_emulation_execution.ip_first_octet,
                                                                 example_emulation_execution.emulation_name))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(fetched_emulation_execution, EmulationExecution)
        assert fetched_emulation_execution == example_emulation_execution

    def test_remove_emulation_execution(self, mocker: pytest_mock.MockFixture,
                                        example_emulation_execution: EmulationExecution) -> None:
        """
        Tests the remove_emulation_execution function

        :param mocker: the pytest mocker object
        :param example_emulation_execution: an example EmulationExecution object
        :return: None
        """
        example_emulation_execution.ip_first_octet = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_emulation_execution(emulation_execution=example_emulation_execution)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
            f"WHERE ip_first_octet = %s AND emulation_name = %s",
            (example_emulation_execution.ip_first_octet, example_emulation_execution.emulation_name))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_save_emulation_execution(self, mocker: pytest_mock.MockFixture,
                                      example_emulation_execution: EmulationExecution) -> None:
        """
        Tests the save_emulation_execution function

        :param mocker: the pytest mocker object
        :param example_emulation_execution: an example EmulationExecution object
        :return: None
        """
        id = 2
        example_emulation_execution.ip_first_octet = id
        mocker.patch('csle_common.dao.emulation_config.emulation_execution.EmulationExecution.from_dict',
                     return_value=example_emulation_execution)
        example_record = (example_emulation_execution.ip_first_octet, example_emulation_execution.emulation_name,
                          example_emulation_execution.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_emulation_execution(emulation_execution=example_emulation_execution)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
            f"(ip_first_octet, emulation_name, info) "
            f"VALUES (%s, %s, %s) RETURNING ip_first_octet", (example_emulation_execution.ip_first_octet,
                                                              example_emulation_execution.emulation_name,
                                                              example_emulation_execution.to_json_str()))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_update_emulation_execution(self, mocker: pytest_mock.MockFixture,
                                        example_emulation_execution: EmulationExecution) -> None:
        """
        Tests the update_emulation_execution function

        :param mocker: the pytest mocker object
        :param example_emulation_execution: an example EmulationExecution object
        :return: None
        """
        id = 2
        example_emulation_execution.ip_first_octet = id
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_emulation_execution(emulation_execution=example_emulation_execution,
                                                            ip_first_octet=example_emulation_execution.ip_first_octet,
                                                            emulation=example_emulation_execution.emulation_name)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
            f" SET info=%s "
            f"WHERE {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE}.ip_first_octet = %s "
            f"AND {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE}.emulation_name = %s",
            (example_emulation_execution.to_json_str(), example_emulation_execution.ip_first_octet,
             example_emulation_execution.emulation_name))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_convert_empirical_system_model_record_to_dto(self, mocker: pytest_mock.MockFixture,
                                                          example_empirical_system_model: EmpiricalSystemModel) -> None:
        """
        Tests the _convert_empirical_system_model_record_to_dto function

        :param example_empirical_system_model: an example EmpiricalSystemModel object
        :return: None
        """
        id = 1
        example_empirical_system_model.id = 1
        example_record = (id, example_empirical_system_model.to_dict(),
                          example_empirical_system_model.emulation_env_name,
                          example_empirical_system_model.emulation_statistic_id)
        converted_object = MetastoreFacade._convert_empirical_system_model_record_to_dto(
            empirical_system_model_record=example_record)
        assert isinstance(converted_object, EmpiricalSystemModel)
        assert converted_object == example_empirical_system_model

    def test_list_empirical_system_models(self, mocker: pytest_mock.MockFixture,
                                          example_empirical_system_model: EmpiricalSystemModel) -> None:
        """
        Tests the list_empirical_system_models function

        :param mocker: the pytest mocker object
        :param example_empirical_system_model: an example EmpiricalSystemModel object
        :return: None
        """
        id = 1
        example_empirical_system_model.id = id
        example_record = (id, example_empirical_system_model.to_dict(),
                          example_empirical_system_model.emulation_env_name,
                          example_empirical_system_model.emulation_statistic_id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        empirical_system_models = MetastoreFacade.list_empirical_system_models()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(empirical_system_models, list)
        assert isinstance(empirical_system_models[0], EmpiricalSystemModel)
        assert empirical_system_models[0] == example_empirical_system_model

    def test_list_empirical_system_models_ids(self, mocker: pytest_mock.MockFixture,
                                              example_empirical_system_model: EmpiricalSystemModel) -> None:
        """
        Tests the list_empirical_system_models_ids function

        :param mocker: the pytest mocker object
        :param example_empirical_system_model: EmpiricalSystemModel object
        :return: None
        """
        id = 1
        example_record = (id, example_empirical_system_model.emulation_env_name,
                          example_empirical_system_model.emulation_statistic_id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        empirical_system_models_ids = MetastoreFacade.list_empirical_system_models_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,emulation_name,emulation_statistic_id FROM "
            f"{constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(empirical_system_models_ids, list)
        assert isinstance(empirical_system_models_ids[0], tuple)
        assert isinstance(empirical_system_models_ids[0][0], int)
        assert isinstance(empirical_system_models_ids[0][1], str)
        assert isinstance(empirical_system_models_ids[0][2], int)
        assert empirical_system_models_ids[0] == example_record

    def test_get_empirical_system_model_config(self, mocker: pytest_mock.MockFixture,
                                               example_empirical_system_model: EmpiricalSystemModel) -> None:
        """
        Tests the get_empirical_system_model_config function

        :param example_empirical_system_model: an example EmpiricalSystemModel object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_empirical_system_model.id = id
        example_record = (id, example_empirical_system_model.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        empirical_system_model_config = MetastoreFacade.get_empirical_system_model_config(
            id=example_empirical_system_model.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE} "
            f"WHERE id = %s", (example_empirical_system_model.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(empirical_system_model_config, EmpiricalSystemModel)
        assert empirical_system_model_config == example_empirical_system_model

    def test_save_empirical_system_model(self, mocker: pytest_mock.MockFixture,
                                         example_empirical_system_model: EmpiricalSystemModel) -> None:
        """
        Tests the save_empirical_system_model function

        :param mocker: the pytest mocker object
        :param example_empirical_system_model: an example EmpiricalSystemModel object
        :return: None
        """
        id = 2
        example_empirical_system_model.id = id
        example_record = (example_empirical_system_model.id, example_empirical_system_model.to_dict(),
                          example_empirical_system_model.emulation_env_name,
                          example_empirical_system_model.emulation_statistic_id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_empirical_system_model(empirical_system_model=example_empirical_system_model)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE} "
            f"(id, model, emulation_name, emulation_statistic_id) "
            f"VALUES (%s, %s, %s, %s) RETURNING id", (id, example_empirical_system_model.to_json_str(),
                                                      example_empirical_system_model.emulation_env_name,
                                                      example_empirical_system_model.emulation_statistic_id))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_update_empirical_system_model(self, mocker: pytest_mock.MockFixture,
                                           example_empirical_system_model: EmpiricalSystemModel) -> None:
        """
        Tests the update_empirical_system_model function

        :param mocker: the pytest mocker object
        :param example_empirical_system_model: an example EmpiricalSystemModel object
        :return: None
        """
        id = 2
        example_empirical_system_model.id = id
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_empirical_system_model(empirical_system_model=example_empirical_system_model,
                                                               id=example_empirical_system_model.id)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE} "
            f" SET config=%s "f"WHERE {constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE}.id = %s",
            (example_empirical_system_model.to_json_str(), example_empirical_system_model.id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_empirical_system_model(self, mocker: pytest_mock.MockFixture,
                                           example_empirical_system_model: EmpiricalSystemModel) -> None:
        """
        Tests the remove_empirical_system_model function

        :param mocker: the pytest mocker object
        :param example_empirical_system_model: an example EmpiricalSystemModel object
        :return: None
        """
        example_empirical_system_model.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_empirical_system_model(empirical_system_model=example_empirical_system_model)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE} WHERE id = %s",
            (example_empirical_system_model.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_convert_mcmc_system_model_record_to_dto(self, example_mcmc_system_model: MCMCSystemModel) -> None:
        """
        Tests the _convert_mcmc_system_model_record_to_dto function

        :param example_mcmc_system_model: an example MCMCSystemModel object
        :return: None
        """
        id = 1
        example_mcmc_system_model.id = 1
        example_record = (id, example_mcmc_system_model.to_dict(),
                          example_mcmc_system_model.emulation_env_name,
                          example_mcmc_system_model.emulation_statistic_id)
        converted_object = MetastoreFacade._convert_mcmc_system_model_record_to_dto(
            mcmc_system_model_record=example_record)
        assert isinstance(converted_object, MCMCSystemModel)
        assert converted_object == example_mcmc_system_model

    def test_list_mcmc_system_models(self, mocker: pytest_mock.MockFixture,
                                     example_mcmc_system_model: MCMCSystemModel) -> None:
        """
        Tests the list_mcmc_system_models function

        :param mocker: the pytest mocker object
        :param example_mcmc_system_model: an example MCMCSystemModel object
        :return: None
        """
        id = 1
        example_mcmc_system_model.id = id
        example_record = (id, example_mcmc_system_model.to_dict(),
                          example_mcmc_system_model.emulation_env_name,
                          example_mcmc_system_model.emulation_statistic_id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        mcmc_system_models = MetastoreFacade.list_mcmc_system_models()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(mcmc_system_models, list)
        assert isinstance(mcmc_system_models[0], MCMCSystemModel)
        assert mcmc_system_models[0] == example_mcmc_system_model

    def test_list_mcmc_system_models_ids(self, mocker: pytest_mock.MockFixture,
                                         example_mcmc_system_model: MCMCSystemModel) -> None:
        """
        Tests the list_mcmc_system_models_ids function

        :param mocker: the pytest mocker object
        :param example_mcmc_system_model: MCMCSystemModel object
        :return: None
        """
        id = 1
        example_record = (id, example_mcmc_system_model.emulation_env_name,
                          example_mcmc_system_model.emulation_statistic_id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        mcmc_system_models_ids = MetastoreFacade.list_mcmc_system_models_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,emulation_name,emulation_statistic_id FROM "
            f"{constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(mcmc_system_models_ids, list)
        assert isinstance(mcmc_system_models_ids[0], tuple)
        assert isinstance(mcmc_system_models_ids[0][0], int)
        assert isinstance(mcmc_system_models_ids[0][1], str)
        assert isinstance(mcmc_system_models_ids[0][2], int)
        assert mcmc_system_models_ids[0] == example_record

    def test_get_mcmc_system_model_config(self, mocker: pytest_mock.MockFixture,
                                          example_mcmc_system_model: MCMCSystemModel) -> None:
        """
        Tests the get_mcmc_system_model_config function

        :param example_mcmc_system_model: an example MCMCSystemModel object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_mcmc_system_model.id = id
        example_record = (id, example_mcmc_system_model.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        mcmc_system_model_config = MetastoreFacade.get_mcmc_system_model_config(
            id=example_mcmc_system_model.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE} "
            f"WHERE id = %s", (example_mcmc_system_model.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(mcmc_system_model_config, MCMCSystemModel)
        assert mcmc_system_model_config == example_mcmc_system_model

    def test_save_mcmc_system_model(self, mocker: pytest_mock.MockFixture,
                                    example_mcmc_system_model: MCMCSystemModel) -> None:
        """
        Tests the save_mcmc_system_model function

        :param mocker: the pytest mocker object
        :param example_mcmc_system_model: an example MCMCSystemModel object
        :return: None
        """
        id = 2
        example_mcmc_system_model.id = id
        example_record = (example_mcmc_system_model.id, example_mcmc_system_model.to_dict(),
                          example_mcmc_system_model.emulation_env_name,
                          example_mcmc_system_model.emulation_statistic_id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_mcmc_system_model(mcmc_system_model=example_mcmc_system_model)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE} "
            f"(id, model, emulation_name, emulation_statistic_id) "
            f"VALUES (%s, %s, %s, %s) RETURNING id", (id, example_mcmc_system_model.to_json_str(),
                                                      example_mcmc_system_model.emulation_env_name,
                                                      example_mcmc_system_model.emulation_statistic_id))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_update_mcmc_system_model(self, mocker: pytest_mock.MockFixture,
                                      example_mcmc_system_model: MCMCSystemModel) -> None:
        """
        Tests the update_mcmc_system_model function

        :param mocker: the pytest mocker object
        :param example_mcmc_system_model: an example MCMCSystemModel object
        :return: None
        """
        id = 2
        example_mcmc_system_model.id = id
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_mcmc_system_model(mcmc_system_model=example_mcmc_system_model,
                                                          id=example_mcmc_system_model.id)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE} "
            f" SET config=%s "
            f"WHERE {constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE}.id = %s",
            (example_mcmc_system_model.to_json_str(), example_mcmc_system_model.id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_mcmc_system_model(self, mocker: pytest_mock.MockFixture,
                                      example_mcmc_system_model: MCMCSystemModel) -> None:
        """
        Tests the remove_mcmc_system_model function

        :param mocker: the pytest mocker object
        :param example_mcmc_system_model: an example MCMCSystemModel object
        :return: None
        """
        example_mcmc_system_model.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_mcmc_system_model(mcmc_system_model=example_mcmc_system_model)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE} WHERE id = %s",
            (example_mcmc_system_model.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_convert_gp_system_model_record_to_dto(self, example_gp_system_model: GPSystemModel) -> None:
        """
        Tests the _convert_gp_system_model_record_to_dto function

        :param example_gp_system_model: an example GPSystemModel object
        :return: None
        """
        id = 1
        example_gp_system_model.id = 1
        example_record = (id, example_gp_system_model.to_dict(),
                          example_gp_system_model.emulation_env_name,
                          example_gp_system_model.emulation_statistic_id)
        converted_object = MetastoreFacade._convert_gp_system_model_record_to_dto(gp_system_model_record=example_record)
        assert isinstance(converted_object, GPSystemModel)
        assert converted_object == example_gp_system_model

    def test_list_gp_system_models(self, mocker: pytest_mock.MockFixture,
                                   example_gp_system_model: GPSystemModel) -> None:
        """
        Tests the list_gp_system_models function

        :param mocker: the pytest mocker object
        :param example_gp_system_model: an example GPSystemModel object
        :return: None
        """
        id = 1
        example_gp_system_model.id = id
        example_record = (id, example_gp_system_model.to_dict(),
                          example_gp_system_model.emulation_env_name,
                          example_gp_system_model.emulation_statistic_id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        gp_system_model = MetastoreFacade.list_gp_system_models()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(gp_system_model, list)
        assert isinstance(gp_system_model[0], GPSystemModel)
        assert gp_system_model[0] == example_gp_system_model

    def test_list_gp_system_models_ids(self, mocker: pytest_mock.MockFixture,
                                       example_gp_system_model: GPSystemModel) -> None:
        """
        Tests the list_gp_system_models_ids function

        :param mocker: the pytest mocker object
        :param example_gp_system_model: GPSystemModel object
        :return: None
        """
        id = 1
        example_record = (id, example_gp_system_model.emulation_env_name,
                          example_gp_system_model.emulation_statistic_id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        gp_system_model = MetastoreFacade.list_gp_system_models_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,emulation_name,emulation_statistic_id FROM "
            f"{constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(gp_system_model, list)
        assert isinstance(gp_system_model[0], tuple)
        assert isinstance(gp_system_model[0][0], int)
        assert isinstance(gp_system_model[0][1], str)
        assert isinstance(gp_system_model[0][2], int)
        assert gp_system_model[0] == example_record

    def test_get_gp_system_model_config(self, mocker: pytest_mock.MockFixture,
                                        example_gp_system_model: GPSystemModel) -> None:
        """
        Tests the get_gp_system_model_config function

        :param example_gp_system_model: an example GPSystemModel object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_gp_system_model.id = id
        example_record = (id, example_gp_system_model.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        gp_system_model = MetastoreFacade.get_gp_system_model_config(id=example_gp_system_model.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE} "
            f"WHERE id = %s", (example_gp_system_model.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(gp_system_model, GPSystemModel)
        assert gp_system_model == example_gp_system_model

    def test_save_gp_system_model(self, mocker: pytest_mock.MockFixture,
                                  example_gp_system_model: GPSystemModel) -> None:
        """
        Tests the save_gp_system_model function

        :param mocker: the pytest mocker object
        :param example_gp_system_model: an example GPSystemModel object
        :return: None
        """
        id = 2
        example_gp_system_model.id = id
        example_record = (example_gp_system_model.id, example_gp_system_model.to_dict(),
                          example_gp_system_model.emulation_env_name,
                          example_gp_system_model.emulation_statistic_id)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_gp_system_model(gp_system_model=example_gp_system_model)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE} "
            f"(id, model, emulation_name, emulation_statistic_id) "
            f"VALUES (%s, %s, %s, %s) RETURNING id", (example_gp_system_model.id, example_gp_system_model.to_json_str(),
                                                      example_gp_system_model.emulation_env_name,
                                                      example_gp_system_model.emulation_statistic_id))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_update_gp_system_model(self, mocker: pytest_mock.MockFixture,
                                    example_gp_system_model: GPSystemModel) -> None:
        """
        Tests the update_gp_system_model function

        :param mocker: the pytest mocker object
        :param example_gp_system_model: an example GPSystemModel object
        :return: None
        """
        id = 2
        example_gp_system_model.id = id
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_gp_system_model(gp_system_model=example_gp_system_model,
                                                        id=example_gp_system_model.id)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE} "
            f" SET config=%s "
            f"WHERE {constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE}.id = %s",
            (example_gp_system_model.to_json_str(), id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_gp_system_model(self, mocker: pytest_mock.MockFixture,
                                    example_gp_system_model: GPSystemModel) -> None:
        """
        Tests the remove_gp_system_model function

        :param mocker: the pytest mocker object
        :param example_gp_system_model: an example GPSystemModel object
        :return: None
        """
        example_gp_system_model.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_gp_system_model(gp_system_model=example_gp_system_model)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE} WHERE id = %s",
            (example_gp_system_model.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_convert_management_user_record_to_dto(self, example_management_user: ManagementUser) -> None:
        """
        Tests the _convert_management_user_record_to_dto function

        :param example_management_user: an example ManagementUser object
        :return: None
        """
        id = 1
        example_management_user.id = 1
        example_record = (id, example_management_user.username, example_management_user.password,
                          example_management_user.email, example_management_user.first_name,
                          example_management_user.last_name, example_management_user.organization,
                          example_management_user.admin, example_management_user.salt)
        converted_object = MetastoreFacade._convert_management_user_record_to_dto(
            management_user_record=example_record)
        assert isinstance(converted_object, ManagementUser)
        assert converted_object == example_management_user

    def test_list_management_users(self, mocker: pytest_mock.MockFixture,
                                   example_management_user: ManagementUser) -> None:
        """
        Tests the list_management_users function

        :param mocker: the pytest mocker object
        :param example_management_user: an example ManagementUser object
        :return: None
        """
        id = 1
        example_management_user.id = id
        example_record = (id, example_management_user.username, example_management_user.password,
                          example_management_user.email, example_management_user.first_name,
                          example_management_user.last_name, example_management_user.organization,
                          example_management_user.admin, example_management_user.salt)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        management_user = MetastoreFacade.list_management_users()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(management_user, list)
        assert isinstance(management_user[0], ManagementUser)
        assert management_user[0] == example_management_user

    def test_list_management_users_ids(self, mocker: pytest_mock.MockFixture,
                                       example_management_user: ManagementUser) -> None:
        """
        Tests the list_management_users_ids function

        :param mocker: the pytest mocker object
        :param example_management_user: ManagementUser object
        :return: None
        """
        id = 1
        example_management_user.id = id
        example_record = (example_management_user.id,)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        management_users_ids = MetastoreFacade.list_management_users_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id FROM "
            f"{constants.METADATA_STORE.MANAGEMENT_USERS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(management_users_ids, list)
        assert isinstance(management_users_ids[0], int)
        assert management_users_ids[0] == example_record[0]

    def test_get_management_user_config(self, mocker: pytest_mock.MockFixture,
                                        example_management_user: ManagementUser) -> None:
        """
        Tests the get_management_user_config function

        :param example_management_user: an example ManagementUser object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_management_user.id = id
        example_record = (id, example_management_user.username, example_management_user.password,
                          example_management_user.email, example_management_user.first_name,
                          example_management_user.last_name, example_management_user.organization,
                          example_management_user.admin, example_management_user.salt)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        management_user_config = MetastoreFacade.get_management_user_config(id=example_management_user.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE} "
            f"WHERE id = %s", (example_management_user.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(management_user_config, ManagementUser)
        assert management_user_config == example_management_user

    def test_save_management_user(self, mocker: pytest_mock.MockFixture,
                                  example_management_user: ManagementUser) -> None:
        """
        Tests the save_management_user function

        :param mocker: the pytest mocker object
        :param example_management_user: an example ManagementUser object
        :return: None
        """
        id = 2
        example_management_user.id = id
        example_record = (id, example_management_user.username, example_management_user.password,
                          example_management_user.email, example_management_user.first_name,
                          example_management_user.last_name, example_management_user.organization,
                          example_management_user.admin, example_management_user.salt)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_management_user(management_user=example_management_user)
        mocked_cursor.execute.assert_called_once_with(
            f"INSERT INTO {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE} "
            f"(id, username, password, email, first_name, last_name, organization, admin, salt) "
            f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (example_management_user.id, example_management_user.username, example_management_user.password,
             example_management_user.email, example_management_user.first_name, example_management_user.last_name,
             example_management_user.organization, example_management_user.admin, example_management_user.salt))
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == id

    def test_update_management_user(self, mocker: pytest_mock.MockFixture,
                                    example_management_user: ManagementUser) -> None:
        """
        Tests the update_management_user function

        :param mocker: the pytest mocker object
        :param example_management_user: an example ManagementUser object
        :return: None
        """
        id = 2
        example_management_user.id = id
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_management_user(management_user=example_management_user,
                                                        id=example_management_user.id)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.MANAGEMENT_USERS_TABLE} "
            f" SET username=%s, password=%s, email=%s, first_name=%s, last_name=%s, organization=%s, "
            f"admin=%s, salt=%s WHERE {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE}.id = %s",
            (example_management_user.username, example_management_user.password, example_management_user.email,
             example_management_user.first_name, example_management_user.last_name,
             example_management_user.organization,
             example_management_user.admin, example_management_user.salt, id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_management_user(self, mocker: pytest_mock.MockFixture,
                                    example_management_user: ManagementUser) -> None:
        """
        Tests the remove_management_user function

        :param mocker: the pytest mocker object
        :param example_management_user: an example ManagementUser object
        :return: None
        """
        example_management_user.id = 1
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_management_user(management_user=example_management_user)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE} WHERE id = %s",
            (example_management_user.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_get_management_user_by_username(self, mocker: pytest_mock.MockFixture,
                                             example_management_user: ManagementUser) -> None:
        """
        Tests the get_management_user_by_username function

        :param example_management_user: an example ManagementUser object
        :param mocker: the pytest mocker object
        :return: None
        """
        id = 1
        example_management_user.id = id
        example_record = (id, example_management_user.username, example_management_user.password,
                          example_management_user.email, example_management_user.first_name,
                          example_management_user.last_name, example_management_user.organization,
                          example_management_user.admin, example_management_user.salt)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        management_user_config = MetastoreFacade.get_management_user_by_username(
            username=example_management_user.username)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE} "
            f"WHERE username = %s", (example_management_user.username,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(management_user_config, ManagementUser)
        assert management_user_config == example_management_user

    def test_convert_session_token_record_to_dto(self, example_session_token: SessionToken) -> None:
        """
        Tests the _convert_session_token_record_to_dto function

        :param example_session_token: an example SessionToken object
        :return: None
        """
        example_record = (example_session_token.token, example_session_token.timestamp, example_session_token.username)
        converted_object = MetastoreFacade._convert_session_token_record_to_dto(
            session_token_record=example_record)
        assert isinstance(converted_object, SessionToken)
        assert converted_object == example_session_token

    def test_list_session_tokens(self, mocker: pytest_mock.MockFixture,
                                 example_session_token: SessionToken) -> None:
        """
        Tests the list_session_tokens function

        :param mocker: the pytest mocker object
        :param example_session_token: an example SessionToken object
        :return: None
        """

        example_record = (example_session_token.token, example_session_token.timestamp, example_session_token.username)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        session_token = MetastoreFacade.list_session_tokens()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.SESSION_TOKENS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(session_token, list)
        assert isinstance(session_token[0], SessionToken)
        assert session_token[0] == example_session_token

    def test_get_session_token_metadata(self, mocker: pytest_mock.MockFixture,
                                        example_session_token: SessionToken) -> None:
        """
        Tests the get_session_token_metadata function

        :param example_session_token: an example SessionToken object
        :param mocker: the pytest mocker object
        :return: None
        """
        example_record = (example_session_token.token, example_session_token.timestamp, example_session_token.username)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        session_token = MetastoreFacade.get_session_token_metadata(token=example_session_token.token)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.SESSION_TOKENS_TABLE} "
            f"WHERE token = %s", (example_session_token.token,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(session_token, SessionToken)
        assert session_token == example_session_token

    def test_save_session_token(self, mocker: pytest_mock.MockFixture, example_session_token: SessionToken) -> None:
        """
        Tests the save_session_token function

        :param mocker: the pytest mocker object
        :param example_session_token: an example SessionToken object
        :return: None
        """
        example_record = (example_session_token.token, example_session_token.timestamp, example_session_token.username)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_session_token(session_token=example_session_token)
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, str)
        assert inserted_id == example_session_token.token

    def test_update_session_token(self, mocker: pytest_mock.MockFixture, example_session_token: SessionToken) -> None:
        """
        Tests the update_session_token function

        :param mocker: the pytest mocker object
        :param example_session_token: an example SessionToken object
        :return: None
        """
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_session_token(session_token=example_session_token, token="token")
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.SESSION_TOKENS_TABLE} "
            f" SET token=%s, timestamp=%s, username=%s "
            f"WHERE {constants.METADATA_STORE.SESSION_TOKENS_TABLE}.token = %s",
            (example_session_token.token, example_session_token.timestamp, example_session_token.username, "token"))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_session_token(self, mocker: pytest_mock.MockFixture, example_session_token: SessionToken) -> None:
        """
        Tests the remove_session_token function

        :param mocker: the pytest mocker object
        :param example_session_token: an example SessionToken object
        :return: None
        """
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_session_token(session_token=example_session_token)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.SESSION_TOKENS_TABLE} WHERE token = %s",
            (example_session_token.token,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_get_session_token_by_username(self, mocker: pytest_mock.MockFixture,
                                           example_session_token: SessionToken) -> None:
        """
        Tests the get_session_token_by_username function

        :param example_session_token: an example SessionToken object
        :param mocker: the pytest mocker object
        :return: None
        """
        example_record = (example_session_token.token, example_session_token.timestamp, example_session_token.username)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        session_token = MetastoreFacade.get_session_token_by_username(username=example_session_token.username)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.SESSION_TOKENS_TABLE} "
            f"WHERE username = %s", (example_session_token.username,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(session_token, SessionToken)
        assert session_token == example_session_token

    def test_convert_traces_dataset_record_to_dto(self, example_traces_dataset: TracesDataset) -> None:
        """
        Tests the _convert_traces_dataset_record_to_dto function

        :param example_traces_dataset: an example TracesDataset object
        :return: None
        """
        example_traces_dataset.id = 1
        example_record = (example_traces_dataset.id, example_traces_dataset.name, example_traces_dataset.description,
                          example_traces_dataset.data_schema, example_traces_dataset.download_count,
                          example_traces_dataset.file_path, example_traces_dataset.url,
                          example_traces_dataset.date_added, example_traces_dataset.num_traces,
                          example_traces_dataset.num_attributes_per_time_step, example_traces_dataset.size_in_gb,
                          example_traces_dataset.compressed_size_in_gb, example_traces_dataset.citation,
                          example_traces_dataset.num_files, example_traces_dataset.file_format,
                          example_traces_dataset.added_by, example_traces_dataset.columns)
        converted_object = MetastoreFacade._convert_traces_dataset_record_to_dto(traces_dataset_record=example_record)
        assert isinstance(converted_object, TracesDataset)
        assert converted_object == example_traces_dataset

    def test_list_traces_datasets_ids(self, mocker: pytest_mock.MockFixture,
                                      example_traces_dataset: TracesDataset) -> None:
        """
        Tests the list_traces_datasets_ids function

        :param mocker: the pytest mocker object
        :param example_traces_dataset: TracesDataset object
        :return: None
        """
        id = 1
        example_traces_dataset.id = id
        example_record = (example_traces_dataset.id, example_traces_dataset.name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        traces_datasets_ids = MetastoreFacade.list_traces_datasets_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,name FROM {constants.METADATA_STORE.TRACES_DATASETS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(traces_datasets_ids, list)
        assert isinstance(traces_datasets_ids[0], tuple)
        assert isinstance(traces_datasets_ids[0][0], int)
        assert isinstance(traces_datasets_ids[0][1], str)
        assert traces_datasets_ids[0] == example_record

    def test_list_traces_datasets(self, mocker: pytest_mock.MockFixture, example_traces_dataset: TracesDataset) -> None:
        """
        Tests the list_traces_datasets function

        :param mocker: the pytest mocker object
        :param example_traces_dataset: an example TracesDataset object
        :return: None
        """
        id = 1
        example_traces_dataset.id = id
        example_record = (example_traces_dataset.id, example_traces_dataset.name, example_traces_dataset.description,
                          example_traces_dataset.data_schema, example_traces_dataset.download_count,
                          example_traces_dataset.file_path, example_traces_dataset.url,
                          example_traces_dataset.date_added, example_traces_dataset.num_traces,
                          example_traces_dataset.num_attributes_per_time_step, example_traces_dataset.size_in_gb,
                          example_traces_dataset.compressed_size_in_gb, example_traces_dataset.citation,
                          example_traces_dataset.num_files, example_traces_dataset.file_format,
                          example_traces_dataset.added_by, example_traces_dataset.columns)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        traces_datasets = MetastoreFacade.list_traces_datasets()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.TRACES_DATASETS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(traces_datasets, list)
        assert isinstance(traces_datasets[0], TracesDataset)
        assert traces_datasets[0] == example_traces_dataset

    def test_get_traces_dataset_metadata(self, mocker: pytest_mock.MockFixture,
                                         example_traces_dataset: TracesDataset) -> None:
        """
        Tests the get_traces_dataset_metadata function

        :param example_traces_dataset: an example TracesDataset object
        :param mocker: the pytest mocker object
        :return: None
        """
        example_record = (example_traces_dataset.id, example_traces_dataset.name, example_traces_dataset.description,
                          example_traces_dataset.data_schema, example_traces_dataset.download_count,
                          example_traces_dataset.file_path, example_traces_dataset.url,
                          example_traces_dataset.date_added, example_traces_dataset.num_traces,
                          example_traces_dataset.num_attributes_per_time_step, example_traces_dataset.size_in_gb,
                          example_traces_dataset.compressed_size_in_gb, example_traces_dataset.citation,
                          example_traces_dataset.num_files, example_traces_dataset.file_format,
                          example_traces_dataset.added_by, example_traces_dataset.columns)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        traces_dataset_metadata = MetastoreFacade.get_traces_dataset_metadata(id=example_traces_dataset.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.TRACES_DATASETS_TABLE} "
            f"WHERE id = %s", (example_traces_dataset.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(traces_dataset_metadata, TracesDataset)
        assert traces_dataset_metadata == example_traces_dataset

    def test_get_traces_dataset_metadata_by_name(self, mocker: pytest_mock.MockFixture,
                                                 example_traces_dataset: TracesDataset) -> None:
        """
        Tests the get_traces_dataset_metadata_by_name function

        :param example_traces_dataset: an example TracesDataset object
        :param mocker: the pytest mocker object
        :return: None
        """
        example_record = (example_traces_dataset.id, example_traces_dataset.name, example_traces_dataset.description,
                          example_traces_dataset.data_schema, example_traces_dataset.download_count,
                          example_traces_dataset.file_path, example_traces_dataset.url,
                          example_traces_dataset.date_added, example_traces_dataset.num_traces,
                          example_traces_dataset.num_attributes_per_time_step, example_traces_dataset.size_in_gb,
                          example_traces_dataset.compressed_size_in_gb, example_traces_dataset.citation,
                          example_traces_dataset.num_files, example_traces_dataset.file_format,
                          example_traces_dataset.added_by, example_traces_dataset.columns)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        traces_dataset_metadata = MetastoreFacade.get_traces_dataset_metadata_by_name(
            dataset_name=example_traces_dataset.name)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.TRACES_DATASETS_TABLE} "
            f"WHERE name = %s", (example_traces_dataset.name,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(traces_dataset_metadata, TracesDataset)
        assert traces_dataset_metadata == example_traces_dataset

    def test_save_traces_dataset(self, mocker: pytest_mock.MockFixture, example_traces_dataset: TracesDataset) -> None:
        """
        Tests the save_traces_dataset function

        :param mocker: the pytest mocker object
        :param example_traces_dataset: an example TracesDataset object
        :return: None
        """
        example_traces_dataset.id = 1
        example_record = (example_traces_dataset.id, example_traces_dataset.name, example_traces_dataset.description,
                          example_traces_dataset.data_schema, example_traces_dataset.download_count,
                          example_traces_dataset.file_path, example_traces_dataset.url,
                          example_traces_dataset.date_added, example_traces_dataset.num_traces,
                          example_traces_dataset.num_attributes_per_time_step, example_traces_dataset.size_in_gb,
                          example_traces_dataset.compressed_size_in_gb, example_traces_dataset.citation,
                          example_traces_dataset.num_files, example_traces_dataset.file_format,
                          example_traces_dataset.added_by, example_traces_dataset.columns)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_traces_dataset(traces_dataset=example_traces_dataset)
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == example_traces_dataset.id

    def test_update_traces_dataset(self, mocker: pytest_mock.MockFixture,
                                   example_traces_dataset: TracesDataset) -> None:
        """
        Tests the update_traces_dataset function

        :param mocker: the pytest mocker object
        :param example_traces_dataset: an example TracesDataset object
        :return: None
        """
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_traces_dataset(traces_dataset=example_traces_dataset,
                                                       id=example_traces_dataset.id)
        schema_json_str = ""
        if example_traces_dataset.data_schema is not None:
            schema_json_str = json.dumps(example_traces_dataset.data_schema, indent=4, sort_keys=True, cls=NpEncoder)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.TRACES_DATASETS_TABLE} "
            f" SET name=%s, description=%s, data_schema=%s, download_count=%s, file_path=%s, "
            f"url=%s, date_added=%s, num_traces=%s, num_attributes_per_time_step=%s, size_in_gb=%s, "
            f"compressed_size_in_gb=%s, citation=%s, num_files=%s, file_format=%s, added_by=%s, "
            f"columns=%s "
            f"WHERE {constants.METADATA_STORE.TRACES_DATASETS_TABLE}.id = %s",
            (example_traces_dataset.name, example_traces_dataset.description, schema_json_str,
             example_traces_dataset.download_count, example_traces_dataset.file_path, example_traces_dataset.url,
             example_traces_dataset.date_added, example_traces_dataset.num_traces,
             example_traces_dataset.num_attributes_per_time_step, example_traces_dataset.size_in_gb,
             example_traces_dataset.compressed_size_in_gb, example_traces_dataset.citation,
             example_traces_dataset.num_files, example_traces_dataset.file_format, example_traces_dataset.added_by,
             example_traces_dataset.columns, example_traces_dataset.id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_traces_dataset(self, mocker: pytest_mock.MockFixture,
                                   example_traces_dataset: TracesDataset) -> None:
        """
        Tests the remove_traces_dataset function

        :param mocker: the pytest mocker object
        :param example_traces_dataset: an example TracesDataset object
        :return: None
        """
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_traces_dataset(traces_dataset=example_traces_dataset)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.TRACES_DATASETS_TABLE} WHERE id = %s",
            (example_traces_dataset.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_convert_statistics_dataset_record_to_dto(self, example_statistics_dataset: StatisticsDataset) -> None:
        """
        Tests the _convert_statistics_dataset_record_to_dto function

        :param example_statistics_dataset: an example StatisticsDataset object
        :return: None
        """
        example_statistics_dataset.id = 1
        example_record = (example_statistics_dataset.id, example_statistics_dataset.name,
                          example_statistics_dataset.description, example_statistics_dataset.download_count,
                          example_statistics_dataset.file_path, example_statistics_dataset.url,
                          example_statistics_dataset.date_added,
                          example_statistics_dataset.num_measurements,
                          example_statistics_dataset.num_metrics,
                          example_statistics_dataset.size_in_gb,
                          example_statistics_dataset.compressed_size_in_gb, example_statistics_dataset.citation,
                          example_statistics_dataset.num_files, example_statistics_dataset.file_format,
                          example_statistics_dataset.added_by, example_statistics_dataset.conditions,
                          example_statistics_dataset.metrics, example_statistics_dataset.num_conditions)
        converted_object = MetastoreFacade._convert_statistics_dataset_record_to_dto(
            statistics_dataset_record=example_record)
        assert isinstance(converted_object, StatisticsDataset)
        assert converted_object == example_statistics_dataset

    def test_list_statistics_datasets_ids(self, mocker: pytest_mock.MockFixture,
                                          example_statistics_dataset: StatisticsDataset) -> None:
        """
        Tests the list_statistics_datasets_ids function

        :param mocker: the pytest mocker object
        :param example_statistics_dataset: StatisticsDataset object
        :return: None
        """
        id = 1
        example_statistics_dataset.id = id
        example_record = (example_statistics_dataset.id, example_statistics_dataset.name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        statistics_datasets_ids = MetastoreFacade.list_statistics_datasets_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,name FROM {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(statistics_datasets_ids, list)
        assert isinstance(statistics_datasets_ids[0], tuple)
        assert isinstance(statistics_datasets_ids[0][0], int)
        assert isinstance(statistics_datasets_ids[0][1], str)
        assert statistics_datasets_ids[0] == example_record

    def test_list_statistics_datasets(self, mocker: pytest_mock.MockFixture,
                                      example_statistics_dataset: StatisticsDataset) -> None:
        """
        Tests the list_statistics_datasets function

        :param mocker: the pytest mocker object
        :param example_statistics_dataset: an example StatisticsDataset object
        :return: None
        """
        id = 1
        example_statistics_dataset.id = id
        example_record = (example_statistics_dataset.id, example_statistics_dataset.name,
                          example_statistics_dataset.description, example_statistics_dataset.download_count,
                          example_statistics_dataset.file_path, example_statistics_dataset.url,
                          example_statistics_dataset.date_added,
                          example_statistics_dataset.num_measurements,
                          example_statistics_dataset.num_metrics,
                          example_statistics_dataset.size_in_gb,
                          example_statistics_dataset.compressed_size_in_gb, example_statistics_dataset.citation,
                          example_statistics_dataset.num_files, example_statistics_dataset.file_format,
                          example_statistics_dataset.added_by, example_statistics_dataset.conditions,
                          example_statistics_dataset.metrics, example_statistics_dataset.num_conditions)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        statistics_datasets = MetastoreFacade.list_statistics_datasets()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(statistics_datasets, list)
        assert isinstance(statistics_datasets[0], StatisticsDataset)
        assert statistics_datasets[0] == example_statistics_dataset

    def test_get_statistics_dataset_metadata(self, mocker: pytest_mock.MockFixture,
                                             example_statistics_dataset: StatisticsDataset) -> None:
        """
        Tests the get_statistics_dataset_metadata function

        :param example_statistics_dataset: an example StatisticsDataset object
        :param mocker: the pytest mocker object
        :return: None
        """
        example_statistics_dataset.id = 1
        example_record = (example_statistics_dataset.id, example_statistics_dataset.name,
                          example_statistics_dataset.description, example_statistics_dataset.download_count,
                          example_statistics_dataset.file_path, example_statistics_dataset.url,
                          example_statistics_dataset.date_added,
                          example_statistics_dataset.num_measurements,
                          example_statistics_dataset.num_metrics,
                          example_statistics_dataset.size_in_gb,
                          example_statistics_dataset.compressed_size_in_gb, example_statistics_dataset.citation,
                          example_statistics_dataset.num_files, example_statistics_dataset.file_format,
                          example_statistics_dataset.added_by, example_statistics_dataset.conditions,
                          example_statistics_dataset.metrics, example_statistics_dataset.num_conditions)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        statistics_dataset_metadata = MetastoreFacade.get_statistics_dataset_metadata(id=example_statistics_dataset.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE} "
            f"WHERE id = %s", (example_statistics_dataset.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(statistics_dataset_metadata, StatisticsDataset)
        assert statistics_dataset_metadata == example_statistics_dataset

    def test_get_statistics_dataset_metadata_by_name(self, mocker: pytest_mock.MockFixture,
                                                     example_statistics_dataset: StatisticsDataset) -> None:
        """
        Tests the get_statistics_dataset_metadata_by_name function

        :param example_statistics_dataset: an example StatisticsDataset object
        :param mocker: the pytest mocker object
        :return: None
        """
        example_record = (example_statistics_dataset.id, example_statistics_dataset.name,
                          example_statistics_dataset.description, example_statistics_dataset.download_count,
                          example_statistics_dataset.file_path, example_statistics_dataset.url,
                          example_statistics_dataset.date_added,
                          example_statistics_dataset.num_measurements,
                          example_statistics_dataset.num_metrics,
                          example_statistics_dataset.size_in_gb,
                          example_statistics_dataset.compressed_size_in_gb, example_statistics_dataset.citation,
                          example_statistics_dataset.num_files, example_statistics_dataset.file_format,
                          example_statistics_dataset.added_by, example_statistics_dataset.conditions,
                          example_statistics_dataset.metrics, example_statistics_dataset.num_conditions)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        statistics_dataset_metadata = MetastoreFacade.get_statistics_dataset_metadata_by_name(
            dataset_name=example_statistics_dataset.name)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE} "
            f"WHERE name = %s", (example_statistics_dataset.name,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(statistics_dataset_metadata, StatisticsDataset)
        assert statistics_dataset_metadata == example_statistics_dataset

    def test_save_statistics_dataset(self, mocker: pytest_mock.MockFixture,
                                     example_statistics_dataset: StatisticsDataset) -> None:
        """
        Tests the save_statistics_dataset function

        :param mocker: the pytest mocker object
        :param example_statistics_dataset: an example StatisticsDataset object
        :return: None
        """
        example_statistics_dataset.id = 1
        example_record = (example_statistics_dataset.id, example_statistics_dataset.name,
                          example_statistics_dataset.description, example_statistics_dataset.download_count,
                          example_statistics_dataset.file_path, example_statistics_dataset.url,
                          example_statistics_dataset.date_added,
                          example_statistics_dataset.num_measurements,
                          example_statistics_dataset.num_metrics,
                          example_statistics_dataset.size_in_gb,
                          example_statistics_dataset.compressed_size_in_gb, example_statistics_dataset.citation,
                          example_statistics_dataset.num_files, example_statistics_dataset.file_format,
                          example_statistics_dataset.added_by, example_statistics_dataset.conditions,
                          example_statistics_dataset.metrics, example_statistics_dataset.num_conditions)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_statistics_dataset(statistics_dataset=example_statistics_dataset)
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == example_statistics_dataset.id

    def test_update_statistics_dataset(self, mocker: pytest_mock.MockFixture,
                                       example_statistics_dataset: StatisticsDataset) -> None:
        """
        Tests the update_statistics_dataset function

        :param mocker: the pytest mocker object
        :param example_statistics_dataset: an example StatisticsDataset object
        :return: None
        """
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_statistics_dataset(
            statistics_dataset=example_statistics_dataset, id=example_statistics_dataset.id)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.STATISTICS_DATASETS_TABLE} "
            f" SET name=%s, description=%s, download_count=%s, file_path=%s, "
            f"url=%s, date_added=%s, num_measurements=%s, num_metrics=%s, size_in_gb=%s, "
            f"compressed_size_in_gb=%s, citation=%s, num_files=%s, file_format=%s, added_by=%s, "
            f"conditions=%s, metrics=%s, num_conditions=%s "
            f"WHERE {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE}.id = %s",
            (example_statistics_dataset.name, example_statistics_dataset.description,
             example_statistics_dataset.download_count, example_statistics_dataset.file_path,
             example_statistics_dataset.url,
             example_statistics_dataset.date_added, example_statistics_dataset.num_measurements,
             example_statistics_dataset.num_metrics, example_statistics_dataset.size_in_gb,
             example_statistics_dataset.compressed_size_in_gb, example_statistics_dataset.citation,
             example_statistics_dataset.num_files, example_statistics_dataset.file_format,
             example_statistics_dataset.added_by,
             example_statistics_dataset.conditions, example_statistics_dataset.metrics,
             example_statistics_dataset.num_conditions, example_statistics_dataset.id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_statistics_dataset(self, mocker: pytest_mock.MockFixture,
                                       example_statistics_dataset: StatisticsDataset) -> None:
        """
        Tests the remove_statistics_dataset function

        :param mocker: the pytest mocker object
        :param example_statistics_dataset: an example StatisticsDataset object
        :return: None
        """
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_statistics_dataset(statistics_dataset=example_statistics_dataset)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE} WHERE id = %s",
            (example_statistics_dataset.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_convert_config_record_to_dto(self, example_config: Config) -> None:
        """
        Tests the _convert_config_record_to_dto function

        :param example_config: an example Config object
        :return: None
        """
        example_config.id = 1
        example_record = (example_config.id, example_config.to_dict())
        converted_object = MetastoreFacade._convert_config_record_to_dto(config_record=example_record)
        assert isinstance(converted_object, Config)
        assert converted_object == example_config

    def test_list_configs(self, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the list_configs function

        :param mocker: the pytest mocker object
        :param example_config: an example Config object
        :return: None
        """
        example_config.id = 1
        example_record = (example_config.id, example_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        configs = MetastoreFacade.list_configs()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.CONFIG_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(configs, list)
        assert isinstance(configs[0], Config)
        assert configs[0] == example_config

    def test_list_config_ids(self, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the list_config_ids function

        :param mocker: the pytest mocker object
        :param example_config: Config object
        :return: None
        """
        example_config.id = 1
        example_record = (example_config.id,)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        config_ids = MetastoreFacade.list_config_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id FROM {constants.METADATA_STORE.CONFIG_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(config_ids, list)
        assert isinstance(config_ids[0], int)
        assert config_ids[0] == example_config.id

    def test_get_config(self, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the get_config function

        :param example_config: an example Config object
        :param mocker: the pytest mocker object
        :return: None
        """
        example_config.id = 1
        example_record = (example_config.id, example_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        config = MetastoreFacade.get_config(id=example_config.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.CONFIG_TABLE} "
            f"WHERE id = %s", (example_config.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(config, Config)
        assert config == example_config

    def test_save_config(self, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the save_config function

        :param mocker: the pytest mocker object
        :param example_config: an example Config object
        :return: None
        """
        example_config.id = 1
        example_record = (example_config.id, example_config.to_dict())
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_config(config=example_config)
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == example_config.id

    def test_update_config(self, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the update_config function

        :param mocker: the pytest mocker object
        :param example_config: an example Config object
        :return: None
        """
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.update_config(config=example_config, id=example_config.id)
        mocked_cursor.execute.assert_called_once_with(
            f"UPDATE "
            f"{constants.METADATA_STORE.CONFIG_TABLE} "
            f" SET config=%s "
            f"WHERE {constants.METADATA_STORE.CONFIG_TABLE}.id = %s", (example_config.to_json_str(), example_config.id))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_remove_config(self, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the remove_config function

        :param mocker: the pytest mocker object
        :param example_config: an example Config object
        :return: None
        """
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_config(config=example_config)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.CONFIG_TABLE} WHERE id = %s", (example_config.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_list_linear_threshold_stopping_policies(
            self, mocker: pytest_mock.MockFixture,
            example_linear_threshold_stopping_policy: LinearThresholdStoppingPolicy) -> None:
        """
        Tests the list_linear_threshold_stopping_policies function

        :param mocker: the pytest mocker object
        :param example_linear_threshold_stopping_policy: an example LinearThresholdStoppingPolicy object
        :return: None
        """
        example_linear_threshold_stopping_policy.id = 1
        example_record = (example_linear_threshold_stopping_policy.id,
                          example_linear_threshold_stopping_policy.to_dict(),
                          example_linear_threshold_stopping_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        linear_threshold_stopping_policies = MetastoreFacade.list_linear_threshold_stopping_policies()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.LINEAR_THRESHOLD_STOPPING_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(linear_threshold_stopping_policies, list)
        assert isinstance(linear_threshold_stopping_policies[0], LinearThresholdStoppingPolicy)
        assert linear_threshold_stopping_policies[0] == example_linear_threshold_stopping_policy

    def test_list_linear_threshold_stopping_policies_ids(
            self, mocker: pytest_mock.MockFixture,
            example_linear_threshold_stopping_policy: LinearThresholdStoppingPolicy) -> None:
        """
        Tests the list_linear_threshold_stopping_policies_ids function

        :param mocker: the pytest mocker object
        :param example_linear_threshold_stopping_policy: LinearThresholdStoppingPolicy object
        :return: None
        """
        example_linear_threshold_stopping_policy.id = 1
        example_record = (example_linear_threshold_stopping_policy.id,
                          example_linear_threshold_stopping_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchall.return_value": [example_record]})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        linear_threshold_stopping_policies_ids = MetastoreFacade.list_linear_threshold_stopping_policies_ids()
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT id,simulation_name FROM "
            f"{constants.METADATA_STORE.LINEAR_THRESHOLD_STOPPING_POLICIES_TABLE}")
        mocked_cursor.fetchall.assert_called_once()
        assert isinstance(linear_threshold_stopping_policies_ids, list)
        assert isinstance(linear_threshold_stopping_policies_ids[0], tuple)
        assert isinstance(linear_threshold_stopping_policies_ids[0][0], int)
        assert isinstance(linear_threshold_stopping_policies_ids[0][1], str)
        assert linear_threshold_stopping_policies_ids[0] == example_record

    def test_convert_linear_threshold_stopping_policy_record_to_dto(
            self, example_linear_threshold_stopping_policy: LinearThresholdStoppingPolicy) -> None:
        """
        Tests the _convert_linear_threshold_stopping_policy_record_to_dto function

        :param example_linear_threshold_stopping_policy: an example LinearThresholdStoppingPolicy object
        :return: None
        """
        example_linear_threshold_stopping_policy.id = 1
        example_record = (example_linear_threshold_stopping_policy.id,
                          example_linear_threshold_stopping_policy.to_dict(),
                          example_linear_threshold_stopping_policy.simulation_name)
        converted_object = MetastoreFacade._convert_linear_threshold_stopping_policy_record_to_dto(
            linear_threshold_stopping_policy_record=example_record)
        assert isinstance(converted_object, LinearThresholdStoppingPolicy)
        assert converted_object == example_linear_threshold_stopping_policy

    def test_get_linear_threshold_stopping_policy(
            self, mocker: pytest_mock.MockFixture,
            example_linear_threshold_stopping_policy: LinearThresholdStoppingPolicy) -> None:
        """
        Tests the get_linear_threshold_stopping_policy function

        :param example_linear_threshold_stopping_policy: an example LinearThresholdStoppingPolicy object
        :param mocker: the pytest mocker object
        :return: None
        """
        example_linear_threshold_stopping_policy.id = 1
        example_record = (example_linear_threshold_stopping_policy.id,
                          example_linear_threshold_stopping_policy.to_dict(),
                          example_linear_threshold_stopping_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        linear_threshold_stopping_policy = MetastoreFacade.get_linear_threshold_stopping_policy(
            id=example_linear_threshold_stopping_policy.id)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"SELECT * FROM {constants.METADATA_STORE.LINEAR_THRESHOLD_STOPPING_POLICIES_TABLE} "
            f"WHERE id = %s", (example_linear_threshold_stopping_policy.id,))
        mocked_cursor.fetchone.assert_called_once()
        assert isinstance(linear_threshold_stopping_policy, LinearThresholdStoppingPolicy)
        assert linear_threshold_stopping_policy == example_linear_threshold_stopping_policy

    def test_remove_linear_threshold_stopping_policy(
            self, mocker: pytest_mock.MockFixture,
            example_linear_threshold_stopping_policy: LinearThresholdStoppingPolicy) -> None:
        """
        Tests the remove_linear_threshold_stopping_policy function

        :param mocker: the pytest mocker object
        :param example_linear_threshold_stopping_policy: an example LinearThresholdStoppingPolicy object
        :return: None
        """
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"commit.return_value": None})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        result = MetastoreFacade.remove_linear_threshold_stopping_policy(
            linear_threshold_stopping_policy=example_linear_threshold_stopping_policy)
        mocked_connection.cursor.assert_called_once()
        mocked_cursor.execute.assert_called_once_with(
            f"DELETE FROM {constants.METADATA_STORE.LINEAR_THRESHOLD_STOPPING_POLICIES_TABLE} "
            f"WHERE id = %s", (example_linear_threshold_stopping_policy.id,))
        mocked_connection.commit.assert_called_once()
        assert result is None

    def test_save_linear_threshold_stopping_policy(
            self, mocker: pytest_mock.MockFixture,
            example_linear_threshold_stopping_policy: LinearThresholdStoppingPolicy) -> None:
        """
        Tests the save_linear_threshold_stopping_policy function

        :param mocker: the pytest mocker object
        :param example_linear_threshold_stopping_policy: an LinearThresholdStoppingPolicy Config object
        :return: None
        """
        example_linear_threshold_stopping_policy.id = 1
        example_record = (example_linear_threshold_stopping_policy.id,
                          example_linear_threshold_stopping_policy.to_dict(),
                          example_linear_threshold_stopping_policy.simulation_name)
        mocked_connection = mocker.MagicMock()
        mocked_cursor = mocker.MagicMock()
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_latest_table_id', return_value=id)
        mocker.patch('psycopg.connect', return_value=mocked_connection)
        mocked_connection.configure_mock(**{"__enter__.return_value": mocked_connection})
        mocked_connection.configure_mock(**{"cursor.return_value": mocked_cursor})
        mocked_cursor.configure_mock(**{"execute.return_value": None})
        mocked_cursor.configure_mock(**{"fetchone.return_value": example_record})
        mocked_cursor.configure_mock(**{"__enter__.return_value": mocked_cursor})
        inserted_id = MetastoreFacade.save_linear_threshold_stopping_policy(
            linear_threshold_stopping_policy=example_linear_threshold_stopping_policy)
        mocked_cursor.fetchone.assert_called_once()
        mocked_connection.commit.assert_called_once()
        assert isinstance(inserted_id, int)
        assert inserted_id == example_linear_threshold_stopping_policy.id
