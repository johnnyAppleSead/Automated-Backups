from engine_util import Util
from datetime import date


# Generates the file name for the copied file
def get_file_name(directory):
    if Util().empty(directory):
        raise Exception('Empty file path')

    spl = directory.split('\\')
    length = len(spl)
    source_file_name = spl[length - 1]
    spl2 = source_file_name.split('.')
    file_name_base = spl2[0]

    today = date.today()

    return file_name_base + ' - ' + str(today) + '.' + spl2[1]


# Maintains file source and target. Data not stored in this file
class File:
    def __init__(self, source_dir, target_dir, target_file_name=None):
        self.source = source_dir
        self.targets = target_dir
        self.target_file_name = target_file_name

        if Util().empty(self.target_file_name):
            self.target_file_name = get_file_name(self.source)


