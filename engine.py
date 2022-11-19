import engine_util as util
import shutil
from cleaner import Cleaner
from config_util import ConfigUtil


class Engine:
    def __init__(self):
        self.files = []

    # The actual copying service
    def copy(self):
        for file in self.files:
            if util.empty(file.source) or util.empty(file.target):
                raise Exception("Configuration file missing source or target directory data")

            util.log("Beginning copy process for " + file.source + " to " + file.target)
            shutil.copy(file.source, (file.target + "\\" + file.target_file_name))
            util.log("Copy process ended for " + file.source + " to " + file.target)

    # Starts the importer, parser, and copying services
    def start(self):
        try:
            self.files = ConfigUtil().load()
            self.copy()
        except Exception as e:
            util.log(str(e.args))


Engine().start()  # Performs the automated processes for automated backups
Cleaner().start()  # Handles automatic cleanup for old files. Disabled via config file
