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
import pytest_mock


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
            f"(config, emulation_name, pid) "
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
