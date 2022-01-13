import zipfile as z
import os
import re
from csle_common.util.experiments_util import util

# Utility script for merging zip files
if __name__ == '__main__':
    zip_files_paths = []
    zip_files_names = []
    path = util.default_output_dir()
    for f in os.listdir(path):
        if re.search(".zip", f) and not re.search(".py", f):
            zip_files_paths.append(os.path.join(path, f))
            zip_files_names.append(f)
    merge_name = zip_files_names[0]
    merge_fp = zip_files_paths[0]
    merge_zf = z.ZipFile(merge_fp, "a")
    for zf in zip_files_paths[1:]:
        print(zf)
        zip = z.ZipFile(zf, "r")
        [merge_zf.writestr(t[0], t[1].read()) for t in ((n, zip.open(n)) for n in zip.namelist())]
        zip.close()
    os.rename(merge_fp, os.path.join(path, "merged.zip"))
    merge_zf.close()


