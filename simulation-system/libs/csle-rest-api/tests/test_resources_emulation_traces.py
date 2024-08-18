from typing import List, Tuple
import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.emulation_observation.attacker.emulation_attacker_observation_state \
    import EmulationAttackerObservationState
from csle_common.dao.emulation_observation.defender.emulation_defender_observation_state \
    import EmulationDefenderObservationState
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesEmulationTracesSuite:
    """
    Test suite for /emulation-traces resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_em_trac_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_emulation_traces_ids
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_emulation_traces_ids() -> List[Tuple[int, int]]:
            return [(1, 1)]
        list_emulation_traces_ids_mocker = mocker.MagicMock(side_effect=list_emulation_traces_ids)
        return list_emulation_traces_ids_mocker

    @pytest.fixture
    def list_em_trac(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_emulation_traces_ids
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_emulation_traces() -> List[EmulationTrace]:
            ex_em_tr = TestResourcesEmulationTracesSuite.get_ex_em_tr()
            return [ex_em_tr]
        list_emulation_traces_mocker = mocker.MagicMock(side_effect=list_emulation_traces)
        return list_emulation_traces_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for the remove_emulation_trace method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def remove_emulation_trace(emulation_trace: EmulationTrace) -> None:
            return None
        remove_emulation_trace_mocker = mocker.MagicMock(side_effect=remove_emulation_trace)
        return remove_emulation_trace_mocker

    @pytest.fixture
    def get_em_tr(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_emulation_trace method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_emulation_trace(id: int) -> EmulationTrace:
            em_tr = TestResourcesEmulationTracesSuite.get_ex_em_tr()
            return em_tr
        get_emulation_trace_mocker = mocker.MagicMock(side_effect=get_emulation_trace)
        return get_emulation_trace_mocker

    @pytest.fixture
    def get_em_tr_none(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_emulation_trace ethod

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_emulation_trace(id: int) -> None:
            return None
        get_emulation_trace_mocker = mocker.MagicMock(side_effect=get_emulation_trace)
        return get_emulation_trace_mocker

    @staticmethod
    def get_ex_em_tr() -> EmulationTrace:
        """
        Static help method for obtaining an EmulationTrace object

        :return: an EmulationTrace object of dummy-values instances
        """
        attacker_action = EmulationAttackerAction(id=EmulationAttackerActionId.CONTINUE, name="JohnDoe",
                                                  cmds=["123.456.78.99"],
                                                  type=EmulationAttackerActionType.CONTINUE, descr="null",
                                                  ips=["123.456.78.99"], index=2,
                                                  action_outcome=EmulationAttackerActionOutcome.GAME_END,
                                                  alt_cmds=["null"], execution_time=10.0, ts=10.0)
        defender_action = EmulationDefenderAction(id=EmulationDefenderActionId.STOP,
                                                  name="JohnDoe", cmds=["null"],
                                                  type=EmulationDefenderActionType.STOP, descr="null",
                                                  ips=["123.456.78.99"], index=1,
                                                  action_outcome=EmulationDefenderActionOutcome.GAME_END,
                                                  alt_cmds=["null"], execution_time=10.0, ts=10.0)
        host_met = HostMetrics(num_logged_in_users=5,
                               num_failed_login_attempts=0,
                               num_open_connections=0,
                               num_login_events=0, num_processes=0,
                               num_users=1,
                               ip="123.456.78.99", ts=1.0)
        cp_metrics = ClientPopulationMetrics(ip="123.456.78.99",
                                             ts=100.5, num_clients=5,
                                             rate=20.0,
                                             service_time=4.0)
        docker_stat = DockerStats(pids=0.0, timestamp="null",
                                  cpu_percent=50.0, mem_current=50.0,
                                  mem_total=50.0, mem_percent=50.0,
                                  blk_read=50.0, blk_write=50.0,
                                  net_rx=50.0, net_tx=50.0, container_name="null",
                                  ip="123.456.78.99", ts=10.0)
        attacker = EmulationAttackerObservationState(catched_flags=1, agent_reachable={"null", "null"})
        defender = EmulationDefenderObservationState(kafka_config=None,
                                                     client_population_metrics=cp_metrics, docker_stats=docker_stat,
                                                     snort_ids_alert_counters=SnortIdsAlertCounters(),
                                                     ossec_ids_alert_counters=OSSECIdsAlertCounters(),
                                                     aggregated_host_metrics=host_met,
                                                     defender_actions=[defender_action],
                                                     attacker_actions=[attacker_action],
                                                     snort_ids_rule_counters=SnortIdsRuleCounters())
        ex_em_tr = EmulationTrace(initial_attacker_observation_state=attacker,
                                  initial_defender_observation_state=defender,
                                  emulation_name="JohnDoe")
        return ex_em_tr

    def test_emulation_traces_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                  logged_in_as_admin, list_em_trac_ids, list_em_trac) -> None:
        """
        Testing the GET HTTPS method for the /emulation-traces resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param list_em_trac_ids: the list_em_trac_ids fixture
        :param list_em_trac: the list_em_trac fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_traces_ids",
                     side_effect=list_em_trac_ids)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_traces",
                     side_effect=list_em_trac)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == 1
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_em_tr = TestResourcesEmulationTracesSuite.get_ex_em_tr()
        ex_em_tr_dict = ex_em_tr.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_em_tr_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}")
        assert response.status_code == constants.HTTPS.METHOD_NOT_ALLOWED_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == 1
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_em_tr = TestResourcesEmulationTracesSuite.get_ex_em_tr()
        ex_em_tr_dict = ex_em_tr.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_em_tr_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}")
        assert response.status_code == constants.HTTPS.METHOD_NOT_ALLOWED_CODE

    def test_emulation_traces_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                     logged_in_as_admin, list_em_trac, remove) -> None:
        """
        Testing the DELETE HTTPS method for the /emulation-traces resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param list_em_trac_ids: the list_em_trac_ids fixture
        :param list_em_trac: the list_em_trac fixture
        :param remove: the remove fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_traces",
                     side_effect=list_em_trac)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_emulation_trace",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_traces_ids_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                      logged_in_as_admin, get_em_tr, get_em_tr_none) -> None:
        """
        Testing the GET HTTPS method for the /emulation-traces/id
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param list_em_trac_ids: the list_em_trac_ids fixture
        :param list_em_trac: the list_em_trac fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_trace",
                     side_effect=get_em_tr)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_em_tr = TestResourcesEmulationTracesSuite.get_ex_em_tr()
        ex_em_tr_dict = ex_em_tr.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_em_tr_dict[k]
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_trace",
                     side_effect=get_em_tr_none)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        for k in response_data_dict:
            assert response_data_dict[k] == ex_em_tr_dict[k]
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_traces_ids",
                     side_effect=get_em_tr_none)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE

    def test_emulation_traces_ids_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                         logged_in, logged_in_as_admin, get_em_tr, get_em_tr_none, remove) -> None:
        """
        Testing the DELETE HTTPS method for the /emulation-traces/id
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param list_em_trac_ids: the list_em_trac_ids fixture
        :param list_em_trac: the list_em_trac fixture
        :param remove: the remove fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_trace",
                     side_effect=get_em_tr)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_emulation_trace",
                     side_effect=remove)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}/10")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}
