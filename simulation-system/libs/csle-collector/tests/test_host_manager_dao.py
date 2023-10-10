from csle_collector.host_manager.dao.failed_login_attempt import FailedLoginAttempt


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
