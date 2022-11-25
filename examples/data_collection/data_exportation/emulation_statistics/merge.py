from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    emulation_statistics = MetastoreFacade.list_emulation_statistics()
    if len(emulation_statistics) > 0:
        em_stat = emulation_statistics[0]
        rest_stats = emulation_statistics[1:]
        for stat in rest_stats:
            em_stat.merge(stat)
        MetastoreFacade.save_emulation_statistic(emulation_statistics=em_stat)
