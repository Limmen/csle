from csle_collector.snort_ids_manager.dao.snort_ids_alert import SnortIdsAlert
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_collector.snort_ids_manager.dao.snort_ids_fast_log_alert import SnortIdsFastLogAlert


class TestSnortIDSManagerDaoSuite:
    """
    Test suite for datasets data access objects (DAOs) in snort_ide_manager
    """

    def test_snort_ids_alert(self, example_snort_ids_alert: SnortIdsAlert) -> None:
        """
        Tests creation and dict conversion of the SnortIdsAlert DAO

        :param example_snort_ids_alert: an example SnortIdsAlert
        :return: None
        """
        assert isinstance(example_snort_ids_alert.to_dict(), dict)
        assert isinstance(SnortIdsAlert.from_dict(example_snort_ids_alert.to_dict()),
                          SnortIdsAlert)
        assert (SnortIdsAlert.from_dict(example_snort_ids_alert.to_dict()).to_dict()
                == example_snort_ids_alert.to_dict())
        assert (SnortIdsAlert.from_dict(example_snort_ids_alert.to_dict())
                == example_snort_ids_alert)

    def test_snort_ids_alert_counters(self, example_snort_ids_alert_counters: SnortIdsAlertCounters) -> None:
        """
        Tests creation and dict conversion of the SnortIdsAlertCounters DAO

        :param example_snort_ids_alert_counters: an example SnortIdsAlertCounters
        :return: None
        """
        assert isinstance(example_snort_ids_alert_counters.to_dict(), dict)
        assert isinstance(SnortIdsAlertCounters.from_dict(example_snort_ids_alert_counters.to_dict()),
                          SnortIdsAlertCounters)
        assert (SnortIdsAlertCounters.from_dict(example_snort_ids_alert_counters.to_dict()).to_dict()
                == example_snort_ids_alert_counters.to_dict())
        assert (SnortIdsAlertCounters.from_dict(example_snort_ids_alert_counters.to_dict())
                == example_snort_ids_alert_counters)

    def test_snort_ids_ip_alert_counters(self, example_snort_ids_ip_alert_counters: SnortIdsIPAlertCounters) -> None:
        """
        Tests creation and dict conversion of the SnortIdsIPAlertCounters DAO

        :param example_snort_ids_ip_alert_counters: an example SnortIdsIPAlertCounters
        :return: None
        """
        assert isinstance(example_snort_ids_ip_alert_counters.to_dict(), dict)
        assert isinstance(SnortIdsIPAlertCounters.from_dict(example_snort_ids_ip_alert_counters.to_dict()),
                          SnortIdsIPAlertCounters)
        assert (SnortIdsIPAlertCounters.from_dict(example_snort_ids_ip_alert_counters.to_dict()).to_dict()
                == example_snort_ids_ip_alert_counters.to_dict())
        assert (SnortIdsIPAlertCounters.from_dict(example_snort_ids_ip_alert_counters.to_dict())
                == example_snort_ids_ip_alert_counters)

    def test_snort_ids_rule_counters(self, example_snort_ids_rule_counters: SnortIdsRuleCounters) -> None:
        """
        Tests creation and dict conversion of the SnortIdsRuleCounters DAO

        :param example_snort_ids_rule_counters: an example SnortIdsRuleCounters
        :return: None
        """
        assert isinstance(example_snort_ids_rule_counters.to_dict(), dict)
        assert isinstance(SnortIdsRuleCounters.from_dict(example_snort_ids_rule_counters.to_dict()),
                          SnortIdsRuleCounters)
        assert (SnortIdsRuleCounters.from_dict(example_snort_ids_rule_counters.to_dict()).to_dict()
                == example_snort_ids_rule_counters.to_dict())
        assert (SnortIdsRuleCounters.from_dict(example_snort_ids_rule_counters.to_dict())
                == example_snort_ids_rule_counters)

    def test_snort_ids_log_alert(self, example_snort_ids_fast_alert: SnortIdsFastLogAlert) -> None:
        """
        Tests creation and dict conversion of the SnortIdsFastLogAlert DAO

        :param example_snort_ids_fast_alert: an example SnortIdsFastLogAlert
        :return: None
        """
        assert isinstance(example_snort_ids_fast_alert.to_dict(), dict)
        assert isinstance(SnortIdsFastLogAlert.from_dict(example_snort_ids_fast_alert.to_dict()),
                          SnortIdsFastLogAlert)
        assert (SnortIdsFastLogAlert.from_dict(example_snort_ids_fast_alert.to_dict()).to_dict()
                == example_snort_ids_fast_alert.to_dict())
        assert (SnortIdsFastLogAlert.from_dict(example_snort_ids_fast_alert.to_dict())
                == example_snort_ids_fast_alert)
