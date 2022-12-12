import engine_util as util
import shutil
from cleaner import Cleaner
from config_util import ConfigUtil
from s3 import S3
import os
from datetime import date


class Engine:
    def __init__(self):
        self.files = []

    # The actual copying service
    def copy(self):
        for file in self.files:
            if util.empty(file.source) or util.empty(file.targets):
                raise Exception("Configuration file missing source or target directory data")

            util.log("Beginning copy process for " + file.source)

            print(str(file.targets))

            for target in file.targets:
                target_type = target["type"]
                target_endpoint = target["target"]

                if target_type == "local":
                    calculated_endpoint = self.__generate_calculated_directory_path(
                                            target_endpoint,
                                            self.__generate_calculated_directory_name())

                    if self.__does_calculated_directory_exist(target_endpoint) is False:
                        util.log("Creating new directory" + calculated_endpoint, "HIGH")
                        os.makedirs(calculated_endpoint)

                    shutil.copy(file.source, os.path.join(calculated_endpoint, file.target_file_name))

                if target_type == "s3":
                    s3 = S3(target_endpoint)
                    s3.upload(file)

            util.log("Copy process ended for " + file.source + " to " + file.target_file_name)

    def __does_calculated_directory_exist(self, endpoint):
        dir_name = self.__generate_calculated_directory_path(endpoint, self.__generate_calculated_directory_name())
        return os.path.exists(dir_name) and os.path.isdir(dir_name)

    def __generate_calculated_directory_path(self, endpoint, name):
        return os.path.join(endpoint, name)

    def __generate_calculated_directory_name(self):
        base_dir_name = "Backup"
        today = str(date.today())

        return base_dir_name + " - " + today

    # Starts the importer, parser, and copying services
    def start(self):
        try:
            self.files = ConfigUtil().load()
            self.copy()
        except Exception as e:
            util.log(str(e.args))


Engine().start()  # Performs the automated processes for automated backups
Cleaner().start()  # Handles automatic cleanup for old files. Disabled via config file
