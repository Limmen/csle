import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.emulation_config.emulation_simulation_trace import EmulationSimulationTrace
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
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
