from csle_collector.ossec_ids_manager.dao.ossec_ids_alert import OSSECIDSAlert
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters


class TestOSSECIdsManagerDaoSuite:
    """
    Test suite for datasets data access objects (DAOs) in ossec_ids_manager
    """

    def test_ossec_ids_alert(self, example_ossec_ids_alert: OSSECIDSAlert) -> None:
        """
        Tests creation and dict conversion of the OSSECIDSAlert DAO

        :param example_ossec_ids_alert: an example OSSECIDSAlert
        :return: None
        """
        assert isinstance(example_ossec_ids_alert.to_dict(), dict)
        assert isinstance(OSSECIDSAlert.from_dict(example_ossec_ids_alert.to_dict()),
                          OSSECIDSAlert)
        assert (OSSECIDSAlert.from_dict(example_ossec_ids_alert.to_dict()).to_dict()
                == example_ossec_ids_alert.to_dict())
        assert (OSSECIDSAlert.from_dict(example_ossec_ids_alert.to_dict())
                == example_ossec_ids_alert)

    def test_ossec_ids_alert_counters(self, example_ossec_ids_alert_counters: OSSECIdsAlertCounters) -> None:
        """
        Tests creation and dict conversion of the OSSECIdsAlertCounters DAO

        :param example_ossec_ids_alert_counters: an example OSSECIdsAlertCounters
        :return: None
        """
        assert isinstance(example_ossec_ids_alert_counters.to_dict(), dict)
        assert isinstance(OSSECIdsAlertCounters.from_dict(example_ossec_ids_alert_counters.to_dict()),
                          OSSECIdsAlertCounters)
        assert (OSSECIdsAlertCounters.from_dict(example_ossec_ids_alert_counters.to_dict()).to_dict()
                == example_ossec_ids_alert_counters.to_dict())
        assert (OSSECIdsAlertCounters.from_dict(example_ossec_ids_alert_counters.to_dict())
                == example_ossec_ids_alert_counters)
