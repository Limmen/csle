import numpy as np
import random
import csle_collector.constants.constants as constants
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_common.consumer_threads.host_metrics_consumer_thread import HostMetricsConsumerThread
from csle_common.consumer_threads.aggregated_host_metrics_thread import AggregatedHostMetricsThread
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_common.consumer_threads.aggregated_ossec_ids_log_consumer_thread import AggregatedOSSECIdsLogConsumerThread
from csle_common.consumer_threads.aggregated_snort_ids_log_consumer_thread import AggregatedSnortIdsLogConsumerThread
from csle_common.consumer_threads.aggregated_snort_ids_rule_log_consumer_thread \
    import AggregatedSnortIdsRuleLogConsumerThread
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.consumer_threads.attacker_actions_consumer_thread import AttackerActionsConsumerThread
from csle_common.dao.emulation_observation.defender.emulation_defender_machine_observation_state import \
    EmulationDefenderMachineObservationState
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_common.consumer_threads.avg_host_metrics_thread import AvgHostMetricsThread
from csle_common.consumer_threads.client_population_consumer_thread import ClientPopulationConsumerThread
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.consumer_threads.defender_actions_consumer_thread import DefenderActionsConsumerThread
from csle_common.consumer_threads.docker_host_stats_consumer_thread import DockerHostStatsConsumerThread
from csle_common.consumer_threads.docker_stats_consumer_thread import DockerStatsConsumerThread
from csle_common.consumer_threads.ossec_ids_log_consumer_thread import OSSECIdsLogConsumerThread
from csle_common.consumer_threads.snort_ids_log_consumer_thread import SnortIdsLogConsumerThread


class TestConsumerThreadsSuiteSuite:
    """
    Test suite for consumer threads
    """

    def test_host_metrics_consumer_thread(self) -> None:
        """
        Tests creation of a host metrics consumer thread and its methods

        :return: None
        """
        example_host_metrics = HostMetrics(num_logged_in_users=1, num_failed_login_attempts=10,
                                           num_open_connections=1, num_login_events=2,
                                           num_processes=5, num_users=1, ip="1.1.1.1", ts=0.5)
        thread = HostMetricsConsumerThread(host_ip="8.8.8.8", kafka_server_ip="8.8.8.8", kafka_port=3030,
                                           host_metrics=example_host_metrics)
        assert thread.host_metrics == example_host_metrics

    def test_aggregated_host_metrics_consumer_thread(self) -> None:
        """
        Tests creation of the aggregated host metrics consumer thread and its methods

        :return: None
        """
        example_host_metrics = HostMetrics(num_logged_in_users=1, num_failed_login_attempts=10,
                                           num_open_connections=1, num_login_events=2,
                                           num_processes=5, num_users=1, ip="1.1.1.1", ts=0.5)
        thread = AggregatedHostMetricsThread(host_metrics=example_host_metrics, machines=[], sleep_time=10)
        assert thread.host_metrics == example_host_metrics
        assert thread.sleep_time == 10
        assert len(thread.machines) == 0

        # Test empty list
        thread.host_metrics_list = []
        averaged_host_metrics = thread.get_average_aggregated_host_metrics()
        assert averaged_host_metrics == example_host_metrics

        # Test singleton list
        thread.host_metrics_list = [example_host_metrics]
        averaged_host_metrics = thread.get_average_aggregated_host_metrics()
        assert averaged_host_metrics == example_host_metrics

        # Test list with 10 identical objects
        thread.host_metrics_list = [example_host_metrics] * 10
        averaged_host_metrics = thread.get_average_aggregated_host_metrics()
        assert averaged_host_metrics.num_logged_in_users == example_host_metrics.num_logged_in_users
        assert averaged_host_metrics.num_failed_login_attempts == example_host_metrics.num_failed_login_attempts
        assert averaged_host_metrics.num_open_connections == example_host_metrics.num_open_connections
        assert averaged_host_metrics.num_login_events == example_host_metrics.num_login_events
        assert averaged_host_metrics.num_processes == example_host_metrics.num_processes
        assert averaged_host_metrics.num_users == example_host_metrics.num_users

        # Test list with two different objects
        example_host_metrics_2 = HostMetrics(num_logged_in_users=2, num_failed_login_attempts=5,
                                             num_open_connections=7, num_login_events=9,
                                             num_processes=11, num_users=3, ip="1.1.1.1", ts=0.5)
        thread.host_metrics_list = [example_host_metrics, example_host_metrics_2]
        averaged_host_metrics = thread.get_average_aggregated_host_metrics()
        assert (averaged_host_metrics.num_logged_in_users ==
                int(round((example_host_metrics.num_logged_in_users + example_host_metrics_2.num_logged_in_users) / 2)))
        assert (averaged_host_metrics.num_failed_login_attempts ==
                int(round((example_host_metrics.num_failed_login_attempts +
                           example_host_metrics_2.num_failed_login_attempts) / 2)))
        assert (averaged_host_metrics.num_open_connections ==
                int(round(
                    (example_host_metrics.num_open_connections + example_host_metrics_2.num_open_connections) / 2)))
        assert (averaged_host_metrics.num_login_events ==
                int(round((example_host_metrics.num_login_events + example_host_metrics_2.num_login_events) / 2)))
        assert (averaged_host_metrics.num_processes ==
                int(round((example_host_metrics.num_processes + example_host_metrics_2.num_processes) / 2)))
        assert (averaged_host_metrics.num_users ==
                int(round((example_host_metrics.num_users + example_host_metrics_2.num_users) / 2)))

    def test_aggregated_ossec_ids_log_consumer_thread(self) -> None:
        """
        Tests creation of a ossec ids log consumer thread and its methods

        :param example_ossec_ids_alert_counters: an object of OSSECIdsAlertCounters
        :return: None
        """
        example_ossec_ids_alert_counters = OSSECIdsAlertCounters()
        example_ossec_ids_alert_counters.level_alerts = list(np.zeros(16))
        for idx in range(16):
            example_ossec_ids_alert_counters.level_alerts[idx] = random.randint(0, 10)

        example_ossec_ids_alert_counters.group_alerts = list(
            np.zeros(len(set(constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values()))))
        for idx in range(len(example_ossec_ids_alert_counters.group_alerts)):
            example_ossec_ids_alert_counters.group_alerts[idx] = random.randint(0, 10)

        example_ossec_ids_alert_counters.severe_alerts = 10
        example_ossec_ids_alert_counters.warning_alerts = 4
        example_ossec_ids_alert_counters.total_alerts = 21
        example_ossec_ids_alert_counters.alerts_weighted_by_level = 0.3

        thread = AggregatedOSSECIdsLogConsumerThread(
            kafka_server_ip="1.2.3.4", kafka_port=1234, ossec_ids_alert_counters=example_ossec_ids_alert_counters.copy()
        )
        assert thread.ossec_ids_alert_counters == example_ossec_ids_alert_counters
        assert thread.kafka_port == 1234
        assert thread.kafka_server_ip == "1.2.3.4"

        # Test empty list
        thread.ossec_ids_alert_counters_list = []
        aggregated_ossec_ids_alert_counters = thread.get_aggregated_ids_alert_counters()
        assert aggregated_ossec_ids_alert_counters == example_ossec_ids_alert_counters

        # Test singleton list
        thread.ossec_ids_alert_counters_list = [example_ossec_ids_alert_counters.copy()]
        aggregated_ossec_ids_alert_counters = thread.get_aggregated_ids_alert_counters()
        assert aggregated_ossec_ids_alert_counters == example_ossec_ids_alert_counters

        # Test list with 10 identical objects
        thread.ossec_ids_alert_counters_list = []
        for i in range(10):
            thread.ossec_ids_alert_counters_list.append(example_ossec_ids_alert_counters.copy())
        aggregated_ossec_ids_alert_counters = thread.get_aggregated_ids_alert_counters()
        assert (aggregated_ossec_ids_alert_counters.severe_alerts ==
                10 * example_ossec_ids_alert_counters.severe_alerts)
        assert (aggregated_ossec_ids_alert_counters.warning_alerts ==
                10 * example_ossec_ids_alert_counters.warning_alerts)
        assert (aggregated_ossec_ids_alert_counters.total_alerts == 10 * example_ossec_ids_alert_counters.total_alerts)
        assert (round(aggregated_ossec_ids_alert_counters.alerts_weighted_by_level, 3) ==
                round(10 * example_ossec_ids_alert_counters.alerts_weighted_by_level, 3))
        for idx in range(len(aggregated_ossec_ids_alert_counters.level_alerts)):
            assert (aggregated_ossec_ids_alert_counters.level_alerts[idx] ==
                    10 * example_ossec_ids_alert_counters.level_alerts[idx])
        for idx in range(len(aggregated_ossec_ids_alert_counters.group_alerts)):
            assert (aggregated_ossec_ids_alert_counters.group_alerts[idx] ==
                    10 * example_ossec_ids_alert_counters.group_alerts[idx])

        # Test list with two different objects
        example_ossec_ids_alert_counters_2 = OSSECIdsAlertCounters()
        example_ossec_ids_alert_counters_2.level_alerts = list(np.zeros(16))
        for idx in range(16):
            example_ossec_ids_alert_counters_2.level_alerts[idx] = random.randint(0, 10)

        example_ossec_ids_alert_counters_2.group_alerts = list(
            np.zeros(len(set(constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values()))))
        for idx in range(len(example_ossec_ids_alert_counters_2.group_alerts)):
            example_ossec_ids_alert_counters_2.group_alerts[idx] = random.randint(0, 10)

        example_ossec_ids_alert_counters_2.severe_alerts = 15
        example_ossec_ids_alert_counters_2.warning_alerts = 1
        example_ossec_ids_alert_counters_2.total_alerts = 18
        example_ossec_ids_alert_counters_2.alerts_weighted_by_level = 0.7

        thread.ossec_ids_alert_counters_list = [example_ossec_ids_alert_counters, example_ossec_ids_alert_counters_2]
        aggregated_ossec_ids_alert_counters = thread.get_aggregated_ids_alert_counters()

        assert (aggregated_ossec_ids_alert_counters.severe_alerts ==
                example_ossec_ids_alert_counters.severe_alerts + example_ossec_ids_alert_counters_2.severe_alerts)
        assert (aggregated_ossec_ids_alert_counters.warning_alerts ==
                example_ossec_ids_alert_counters.warning_alerts + example_ossec_ids_alert_counters_2.warning_alerts)
        assert (aggregated_ossec_ids_alert_counters.total_alerts ==
                example_ossec_ids_alert_counters.total_alerts + example_ossec_ids_alert_counters_2.total_alerts)
        assert (round(aggregated_ossec_ids_alert_counters.alerts_weighted_by_level, 3) ==
                round(example_ossec_ids_alert_counters.alerts_weighted_by_level +
                      example_ossec_ids_alert_counters_2.alerts_weighted_by_level, 3))
        for idx in range(len(aggregated_ossec_ids_alert_counters.level_alerts)):
            assert (aggregated_ossec_ids_alert_counters.level_alerts[idx] ==
                    example_ossec_ids_alert_counters.level_alerts[idx] +
                    example_ossec_ids_alert_counters_2.level_alerts[idx])
        for idx in range(len(aggregated_ossec_ids_alert_counters.group_alerts)):
            assert (aggregated_ossec_ids_alert_counters.group_alerts[idx] ==
                    example_ossec_ids_alert_counters.group_alerts[idx] +
                    example_ossec_ids_alert_counters_2.group_alerts[idx])

    def test_aggregated_snort_ids_log_consumer_thread(self) -> None:
        """
        Tests creation of a snort ids log consumer thread and its methods

        :param example_snort_ids_alert_counters: an object of SnortIdsAlertCounters
        :return: None
        """

        example_snort_ids_alert_counters = SnortIdsAlertCounters()

        example_snort_ids_alert_counters.total_alerts = 10
        example_snort_ids_alert_counters.severe_alerts = 54
        example_snort_ids_alert_counters.warning_alerts = 3
        example_snort_ids_alert_counters.alerts_weighted_by_priority = 0.7
        example_snort_ids_alert_counters.ip = "1.2.3.4"
        example_snort_ids_alert_counters.ts = 1234

        example_snort_ids_alert_counters.priority_alerts = list(np.zeros(4))
        for idx in range(4):
            example_snort_ids_alert_counters.priority_alerts[idx] = random.randint(0, 10)

        example_snort_ids_alert_counters.class_alerts = list(
            np.zeros(len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values()))))
        for idx in range(len(example_snort_ids_alert_counters.class_alerts)):
            example_snort_ids_alert_counters.class_alerts[idx] = random.randint(0, 10)

        thread = AggregatedSnortIdsLogConsumerThread(
            kafka_server_ip="1.2.3.4", kafka_port=1234, snort_ids_alert_counters=example_snort_ids_alert_counters.copy()
        )

        assert thread.snort_ids_alert_counters == example_snort_ids_alert_counters
        assert thread.kafka_port == 1234
        assert thread.kafka_server_ip == "1.2.3.4"

        # Test empty list
        thread.snort_ids_alert_counters_list = []
        aggregated_snort_ids_alert_counters = thread.get_aggregated_ids_alert_counters()
        assert aggregated_snort_ids_alert_counters == example_snort_ids_alert_counters

        # Test singleton list
        thread.snort_ids_alert_counters_list = [example_snort_ids_alert_counters.copy()]
        aggregated_snort_ids_alert_counters = thread.get_aggregated_ids_alert_counters()
        assert aggregated_snort_ids_alert_counters == example_snort_ids_alert_counters

        # Test list with 10 identical objects
        thread.snort_ids_alert_counters_list = []
        for i in range(10):
            thread.snort_ids_alert_counters_list.append(example_snort_ids_alert_counters.copy())
        aggregated_snort_ids_alert_counters = thread.get_aggregated_ids_alert_counters()
        assert (aggregated_snort_ids_alert_counters.total_alerts ==
                10 * example_snort_ids_alert_counters.total_alerts)
        assert (aggregated_snort_ids_alert_counters.severe_alerts ==
                10 * example_snort_ids_alert_counters.severe_alerts)
        assert (aggregated_snort_ids_alert_counters.warning_alerts ==
                10 * example_snort_ids_alert_counters.warning_alerts)
        assert (round(aggregated_snort_ids_alert_counters.alerts_weighted_by_priority, 3) ==
                round(10 * example_snort_ids_alert_counters.alerts_weighted_by_priority, 3))
        for idx in range(len(aggregated_snort_ids_alert_counters.priority_alerts)):
            assert (aggregated_snort_ids_alert_counters.priority_alerts[idx] ==
                    10 * example_snort_ids_alert_counters.priority_alerts[idx])
        for idx in range(len(aggregated_snort_ids_alert_counters.class_alerts)):
            assert (aggregated_snort_ids_alert_counters.class_alerts[idx] ==
                    10 * example_snort_ids_alert_counters.class_alerts[idx])

        # Test list with two different objects
        example_snort_ids_alert_counters_2 = SnortIdsAlertCounters()
        example_snort_ids_alert_counters_2.priority_alerts = list(np.zeros(4))
        for idx in range(4):
            example_snort_ids_alert_counters_2.priority_alerts[idx] = random.randint(0, 10)

        example_snort_ids_alert_counters_2.class_alerts = list(
            np.zeros(len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values()))))
        for idx in range(len(example_snort_ids_alert_counters_2.class_alerts)):
            example_snort_ids_alert_counters_2.class_alerts[idx] = random.randint(0, 10)

        example_snort_ids_alert_counters_2.total_alerts = 15
        example_snort_ids_alert_counters_2.severe_alerts = 1
        example_snort_ids_alert_counters_2.warning_alerts = 18
        example_snort_ids_alert_counters_2.alerts_weighted_by_priority = 0.7

        thread.snort_ids_alert_counters_list = [example_snort_ids_alert_counters,
                                                example_snort_ids_alert_counters_2]
        aggregated_snort_ids_alert_counters = thread.get_aggregated_ids_alert_counters()

        assert (aggregated_snort_ids_alert_counters.severe_alerts ==
                example_snort_ids_alert_counters.severe_alerts + example_snort_ids_alert_counters_2.severe_alerts)
        assert (aggregated_snort_ids_alert_counters.warning_alerts ==
                example_snort_ids_alert_counters.warning_alerts + example_snort_ids_alert_counters_2.warning_alerts)
        assert (aggregated_snort_ids_alert_counters.total_alerts ==
                example_snort_ids_alert_counters.total_alerts + example_snort_ids_alert_counters_2.total_alerts)
        assert (round(aggregated_snort_ids_alert_counters.alerts_weighted_by_priority, 3) ==
                round(example_snort_ids_alert_counters.alerts_weighted_by_priority +
                      example_snort_ids_alert_counters_2.alerts_weighted_by_priority, 3))
        for idx in range(len(aggregated_snort_ids_alert_counters.priority_alerts)):
            assert (aggregated_snort_ids_alert_counters.priority_alerts[idx] ==
                    example_snort_ids_alert_counters.priority_alerts[idx] +
                    example_snort_ids_alert_counters_2.priority_alerts[idx])
        for idx in range(len(aggregated_snort_ids_alert_counters.class_alerts)):
            assert (aggregated_snort_ids_alert_counters.class_alerts[idx] ==
                    example_snort_ids_alert_counters.class_alerts[idx] +
                    example_snort_ids_alert_counters_2.class_alerts[idx])

    def test_aggregated_snort_ids_rule_log_consumer_thread(self) -> None:
        """
        Tests creation of a snort ids rule log consumer thread and its methods

        :param example_snort_ids_rule_alert_counters: an object of SnortIdsRuleAlertCounters
        :return: None
        """
        example_snort_ids_rule_alert_counters = SnortIdsRuleCounters()

        example_snort_ids_rule_alert_counters.rule_alerts = {}
        example_snort_ids_rule_alert_counters.rule_alerts[1] = 10
        example_snort_ids_rule_alert_counters.rule_alerts[2] = 3
        example_snort_ids_rule_alert_counters.ip = "1.2.3.4"
        example_snort_ids_rule_alert_counters.ts = 1234

        thread = AggregatedSnortIdsRuleLogConsumerThread(
            kafka_server_ip="1.2.3.4", kafka_port=1234,
            snort_ids_rule_counters=example_snort_ids_rule_alert_counters.copy()
        )

        assert thread.snort_ids_rule_counters == example_snort_ids_rule_alert_counters
        assert thread.kafka_port == 1234
        assert thread.kafka_server_ip == "1.2.3.4"

        # Test empty list
        thread.snort_ids_rule_counters_list = []
        aggregated_snort_ids_rule_alert_counters = thread.get_aggregated_ids_rule_counters()
        assert aggregated_snort_ids_rule_alert_counters == example_snort_ids_rule_alert_counters

        # Test singleton list
        thread.snort_ids_rule_counters_list = [example_snort_ids_rule_alert_counters.copy()]
        aggregated_snort_ids_rule_alert_counters = thread.get_aggregated_ids_rule_counters()
        assert aggregated_snort_ids_rule_alert_counters == example_snort_ids_rule_alert_counters

        # Test list with 10 identical objects
        thread.snort_ids_rule_counters_list = [example_snort_ids_rule_alert_counters.copy()] * 10
        aggregated_snort_ids_rule_alert_counters = thread.get_aggregated_ids_rule_counters()

        for k, v in aggregated_snort_ids_rule_alert_counters.rule_alerts.items():
            assert (aggregated_snort_ids_rule_alert_counters.rule_alerts[k] ==
                    10 * example_snort_ids_rule_alert_counters.rule_alerts[k])

        # Test list with two different objects
        example_snort_ids_rule_alert_counters_2 = SnortIdsRuleCounters()
        example_snort_ids_rule_alert_counters_2.rule_alerts = {}
        example_snort_ids_rule_alert_counters_2.rule_alerts[1] = 12
        example_snort_ids_rule_alert_counters_2.rule_alerts[2] = 8
        example_snort_ids_rule_alert_counters_2.ip = "1.2.3.4"
        example_snort_ids_rule_alert_counters_2.ts = 1234

        thread.snort_ids_rule_counters_list = [example_snort_ids_rule_alert_counters,
                                               example_snort_ids_rule_alert_counters_2]
        aggregated_snort_ids_rule_alert_counters = thread.get_aggregated_ids_rule_counters()

        for k, v in aggregated_snort_ids_rule_alert_counters.rule_alerts.items():
            assert (aggregated_snort_ids_rule_alert_counters.rule_alerts[k] ==
                    example_snort_ids_rule_alert_counters.rule_alerts[k] +
                    example_snort_ids_rule_alert_counters_2.rule_alerts[k])

    def test_attacker_actions_consumer_thread(self) -> None:
        """
        Tests creation of a attacker action consumer thread and its methods

        :return: None
        """
        example_attacker_actions_consumer = EmulationAttackerAction(
            id=EmulationAttackerActionId.HTTP_ENUM_HOST, name="test1", cmds=["test1"],
            type=EmulationAttackerActionType.CONTINUE, descr="test", ips=["1.1.2.3"], index=1)
        thread = AttackerActionsConsumerThread(kafka_server_ip="1.1.1.1", kafka_port=1234,
                                               attacker_actions=[example_attacker_actions_consumer])
        assert thread.attacker_actions[0] == example_attacker_actions_consumer

    def test_avg_host_metrics_thread(self) -> None:
        """
        Tests creation of a avg host metrics thread and its methods

        :return: None
        """
        example_host_metrics = HostMetrics(num_logged_in_users=1, num_failed_login_attempts=10,
                                           num_open_connections=1, num_login_events=2,
                                           num_processes=5, num_users=1, ip="1.1.1.1", ts=0.5)
        emulation_defender_machine_observation_state_example = EmulationDefenderMachineObservationState(
            ips=["test"], kafka_config=None, host_metrics=example_host_metrics,
            docker_stats=DockerStats(), snort_ids_ip_alert_counters=SnortIdsIPAlertCounters(),
            ossec_ids_alert_counters=OSSECIdsAlertCounters())
        thread = AvgHostMetricsThread(host_metrics=example_host_metrics,
                                      machines=[emulation_defender_machine_observation_state_example], sleep_time=1)
        assert thread.host_metrics == example_host_metrics
        assert thread.machines[0] == emulation_defender_machine_observation_state_example

    def test_client_population_consumer_thread(self) -> None:
        """
        Tests creation of a client population consumer thread and its methods

        :return: None
        """
        example_client_population_metric = ClientPopulationMetrics()
        thread = ClientPopulationConsumerThread(kafka_server_ip="1.1.1.1", kafka_port=1234,
                                                client_population_metrics=example_client_population_metric)
        assert thread.client_population_metrics == example_client_population_metric
        assert thread.kafka_server_ip == "1.1.1.1"
        assert thread.kafka_port == 1234

        # Test empty list
        thread.client_population_metrics_list = []
        avg_client_population_metrics = thread.get_average_client_population_metrics()
        assert avg_client_population_metrics == example_client_population_metric

        # Test singleton list
        thread.client_population_metrics_list = [example_client_population_metric.copy()]
        avg_client_population_metrics = thread.get_average_client_population_metrics()
        assert avg_client_population_metrics == example_client_population_metric

        # Test list with 10 identical objects
        thread.client_population_metrics_list = []
        for i in range(10):
            thread.client_population_metrics_list.append(example_client_population_metric.copy())
        avg_client_population_metrics = thread.get_average_client_population_metrics()

        assert avg_client_population_metrics.num_clients == example_client_population_metric.num_clients
        assert avg_client_population_metrics.rate == example_client_population_metric.rate

        example_client_population_metric_1 = ClientPopulationMetrics(num_clients=10, rate=40)
        thread.client_population_metrics_list = [example_client_population_metric.copy(),
                                                 example_client_population_metric_1]

        avg_client_population_metrics = thread.get_average_client_population_metrics()

        assert (avg_client_population_metrics.num_clients ==
                round((example_client_population_metric.num_clients +
                       example_client_population_metric_1.num_clients) / 2))
        assert (avg_client_population_metrics.rate ==
                round(example_client_population_metric.rate + example_client_population_metric_1.rate) / 2)

    def test_defender_actions_consumer_thread(self) -> None:
        """
        Tests creation of a defender actions consumer thread and its methods

        :return: None
        """
        example_defender_action = EmulationDefenderAction(id=EmulationDefenderActionId.CONTINUE, name="test",
                                                          cmds=["test"], type=EmulationDefenderActionType.CONTINUE,
                                                          descr="test", ips=["1.1.1.1"], index=1)
        thread = DefenderActionsConsumerThread(kafka_server_ip="1.1.1.1", kafka_port=1234,
                                               defender_actions=[example_defender_action])

        assert thread.kafka_server_ip == "1.1.1.1"
        assert thread.kafka_port == 1234
        assert thread.defender_actions[0] == example_defender_action

    def test_docker_host_stats_consumer_thread(self) -> None:
        """
        Tests creation of a docker host stats consumer thread and its methods

        :return: None
        """
        example_docker_host_stats = DockerStats()
        thread = DockerHostStatsConsumerThread(kafka_server_ip="1.1.1.1", kafka_port=1234,
                                               docker_stats=example_docker_host_stats, host_ip="1.2.3.4")

        assert thread.kafka_server_ip == "1.1.1.1"
        assert thread.kafka_port == 1234
        assert thread.docker_stats == example_docker_host_stats
        assert thread.host_ip == "1.2.3.4"

    def test_docker_stats_consumer_thread(self) -> None:
        """
        Tests creation of a docker stats consumer thread and its methods

        :return: None
        """
        example_docker_host_stats = DockerStats()
        thread = DockerStatsConsumerThread(kafka_server_ip="1.1.1.1", kafka_port=1234,
                                           docker_stats=example_docker_host_stats)

        assert thread.kafka_server_ip == "1.1.1.1"
        assert thread.kafka_port == 1234
        assert thread.docker_stats == example_docker_host_stats

    def test_ossec_ids_log_consumer_thread(self) -> None:
        """
        Tests creation of a ossec ids log consumer thread and its methods

        :return: None
        """
        example_ossec_ids_alerts = OSSECIdsAlertCounters()
        thread = OSSECIdsLogConsumerThread(host_ip="1.2.3.4", kafka_server_ip="1.1.1.1", kafka_port=1234,
                                           ossec_ids_alert_counters=example_ossec_ids_alerts)

        assert thread.kafka_server_ip == "1.1.1.1"
        assert thread.kafka_port == 1234
        assert thread.ossec_ids_alert_counters == example_ossec_ids_alerts
        assert thread.host_ip == "1.2.3.4"

    def test_snort_ids_log_consumer_thread(self) -> None:
        """
        Tests creation of a snort ids log consumer thread and its methods

        :return: None
        """
        example_snort_ids_alerts_counter = SnortIdsIPAlertCounters()
        thread = SnortIdsLogConsumerThread(host_ip="1.2.3.4", kafka_server_ip="1.1.1.1", kafka_port=1234,
                                           snort_ids_alert_counters=example_snort_ids_alerts_counter)

        assert thread.kafka_server_ip == "1.1.1.1"
        assert thread.kafka_port == 1234
        assert thread.snort_ids_alert_counters == example_snort_ids_alerts_counter
        assert thread.host_ip == "1.2.3.4"
