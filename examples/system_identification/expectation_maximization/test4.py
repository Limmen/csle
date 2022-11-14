from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.emulation_env_controller import EmulationEnvController
from csle_common.controllers.traffic_controller import TrafficController

if __name__ == '__main__':
    em =MetastoreFacade.get_emulation_by_name("csle-level9-001")
    TrafficController.start_client_population(emulation_env_config=em)
