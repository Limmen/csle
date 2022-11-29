import yaml
import csle_collector.constants.constants as constants

if __name__ == '__main__':



    with open(r'./elastic_test.yml', 'w') as file:
        yaml.dump(elastic_config, file)

    with open(r'./snort_test.yml', 'w') as file:
        yaml.dump(snort_config, file)