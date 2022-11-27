import engine_util as util
import shutil
from cleaner import Cleaner
from config_util import ConfigUtil
from s3 import S3


class Engine:
    def __init__(self):
        self.files = []

    # The actual copying service
    def copy(self):
        for file in self.files:
            print("target: ", file.targets)
            if util.empty(file.source) or util.empty(file.target):
                raise Exception("Configuration file missing source or target directory data")

            util.log("Beginning copy process for " + file.source + " to " + file.target)

            targets = file.target
            target_type = file.target_type

            for target in targets:
                print(target)

            if target_type == "local":
                shutil.copy(file.source, (file.target + "\\" + file.target_file_name))

            if target_type == "s3":
                s3 = S3(targets)
                s3.upload(file)

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
