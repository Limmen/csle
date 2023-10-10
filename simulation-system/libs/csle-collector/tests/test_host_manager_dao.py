from csle_collector.host_manager.dao.failed_login_attempt import FailedLoginAttempt
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_collector.host_manager.dao.successful_login import SuccessfulLogin


class TestHostManagerDaoSuite:
    """
    Test suite for datasets data access objects (DAOs) in client_manager
    """

    def test_failed_login_attempt(self, example_failed_login_attempt: FailedLoginAttempt) -> None:
        """
        Tests creation and dict conversion of the FailedLoginAttempt DAO

        :param example_failed_login_attempt: an example FailedLoginAttempt
        :return: None
        """
        assert isinstance(example_failed_login_attempt.to_dict(), dict)
        assert isinstance(FailedLoginAttempt.from_dict(example_failed_login_attempt.to_dict()),
                          FailedLoginAttempt)
        assert (FailedLoginAttempt.from_dict(example_failed_login_attempt.to_dict()).to_dict()
                == example_failed_login_attempt.to_dict())
        assert (FailedLoginAttempt.from_dict(example_failed_login_attempt.to_dict())
                == example_failed_login_attempt)

    def test_host_metrics(self, example_host_metrics: HostMetrics) -> None:
        """
        Tests creation and dict conversion of the HostMetrics DAO

        :param example_host_metrics: an example HostMetrics
        :return: None
        """
        assert isinstance(example_host_metrics.to_dict(), dict)
        assert isinstance(HostMetrics.from_dict(example_host_metrics.to_dict()),
                          HostMetrics)
        assert (HostMetrics.from_dict(example_host_metrics.to_dict()).to_dict()
                == example_host_metrics.to_dict())
        assert (HostMetrics.from_dict(example_host_metrics.to_dict())
                == example_host_metrics)

    def test_sucessful_login(self, example_successful_login: SuccessfulLogin) -> None:
        """
        Tests creation and dict conversion of the SuccessfulLogin DAO

        :param example_successful_login: an example SuccessfulLogin
        :return: None
        """
        assert isinstance(example_successful_login.to_dict(), dict)
        assert isinstance(SuccessfulLogin.from_dict(example_successful_login.to_dict()),
                          SuccessfulLogin)
        assert (SuccessfulLogin.from_dict(example_successful_login.to_dict()).to_dict()
                == example_successful_login.to_dict())
        assert (SuccessfulLogin.from_dict(example_successful_login.to_dict())
                == example_successful_login)
