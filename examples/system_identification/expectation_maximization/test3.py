from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
import json

if __name__ == '__main__':
    stat = EmulationStatistics.from_json_file("/home/kim/stat_backup_4_may.json")
    # MetastoreFacade.save_emulation_statistic(stat)
