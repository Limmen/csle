from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.emulation_env_manager import EmulationEnvManager
from csle_common.controllers.traffic_manager import TrafficManager

if __name__ == '__main__':
    em =MetastoreFacade.get_emulation("csle-level9-001")
    TrafficManager.start_client_population(emulation_env_config=em)
