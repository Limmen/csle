from csle_common.util.import_util import ImportUtil

if __name__ == '__main__':
    # ImportUtil.import_emulation_traces_from_disk_json(input_file="/media/lagring/traces_31_oct/1.json",
    #                                                   emulation_name="csle-level9-070")
    for i in range(1, 64):
        ImportUtil.import_emulation_traces_from_disk_json(
            input_file=f"/media/lagring/traces_31_oct/{i}.json", emulation_name="csle-level9-070")
