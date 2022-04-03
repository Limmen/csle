import sys
import time
from confluent_kafka import KafkaError, KafkaException
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
import csle_collector.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation("csle-level9-001")
    s = EmulationEnvState(emulation_env_config=emulation_env_config)
    while True:
        time.sleep(10)
        print(s.defender_obs_state.docker_stats)