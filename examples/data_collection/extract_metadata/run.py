from csle_common.util.export_util import ExportUtil
from csle_common.dao.datasets.traces_dataset import TracesDataset

if __name__ == '__main__':
    # ExportUtil.extract_emulation_traces_dataset_metadata(dir_path="/home/kim/traces_2_aug_22")
    ExportUtil.zipdir(dir_path="/home/kim/traces_2_aug_22", file_path="/home/kim/traces_2_aug_22.zip")
