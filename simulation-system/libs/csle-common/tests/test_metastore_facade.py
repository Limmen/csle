import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.emulation_config.emulation_simulation_trace import EmulationSimulationTrace
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.training.experiment_execution import ExperimentExecution
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
