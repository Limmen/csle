from config import default_config


class TestEmulationConfigSuite:
    """
    Test suite for the emulation configuration for 'level-14'
    """

    def test_create_config(self) -> None:
        """
        Tests creation of the emulation configuration

        :return: None
        """
        config = default_config(name="csle-level14-070", network_id=14, level=14, version="0.5.0",
                                time_step_len_seconds=15)
        assert config.vuln_config is not None
        assert config.containers_config is not None
        assert config.flags_config is not None
        assert config.resources_config is not None
        assert config.topology_config is not None
        assert config.traffic_config is not None
        assert config.users_config is not None
        assert config.vuln_config is not None
        assert config.kafka_config is not None
        assert config.services_config is not None
        assert config.static_attacker_sequences is not None
        assert config.ovs_config is not None
        assert config.host_manager_config is not None
        assert config.snort_ids_manager_config is not None
        assert config.ossec_ids_manager_config is not None
        assert config.docker_stats_manager_config is not None
        assert config.elk_config is not None
        assert config.beats_config is not None
