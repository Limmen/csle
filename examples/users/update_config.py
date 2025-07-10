from csle_common.util.cluster_util import ClusterUtil

if __name__ == '__main__':
    config = ClusterUtil.get_config()
    ClusterUtil.set_config_parameters_from_config_file()
