from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    em_stat = MetastoreFacade.get_emulation_statistic(id=2)
    em_stat.compute_descriptive_statistics_and_distributions()