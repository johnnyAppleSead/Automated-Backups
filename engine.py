import shutil
from cleaner import Cleaner
from config_util import ConfigUtil
from s3 import S3
import os
from datetime import date
from engine_util import Util

disallow_cleaner = False


class Engine:
    def __init__(self):
        global disallow_cleaner

        self.files = []
        self.config = ConfigUtil()
        self.__options = self.config.get_value("options")

        disallow_cleaner = self.__options['disable_logging']

        self.util = Util()

    # The actual copying service
    def copy(self):
        for file in self.files:
            if self.util.empty(file.source) or self.util.empty(file.targets):
                raise Exception("Configuration file missing source or target directory data")

            self.util.log("Beginning copy process for " + file.source)

            for target in file.targets:
                target_type = target["type"]
                target_subtype = target["subtype"]
                target_endpoint = target["target"]

                target_status = target["status"]

                if target_status == "disabled":
                    self.util.log("Target Endpoint (" + target_endpoint + ") is disabled")
                    continue

                target_directory_name = self.__generate_calculated_directory_name()

                if target_type == "local":
                    calculated_endpoint = self.__generate_calculated_directory_path(
                        target_endpoint,
                        target_directory_name)

                    if self.__does_calculated_directory_exist(target_endpoint) is False:
                        self.util.log("Creating new directory: " + calculated_endpoint)
                        os.makedirs(calculated_endpoint)
                    try:
                        shutil.copy(file.source, os.path.join(calculated_endpoint, file.target_file_name))
                    except FileNotFoundError:
                        self.util.log("Unable to copy file: File Does Not Exist")

                if target_type == "remote" and target_subtype == "s3":
                    s3 = S3(target_endpoint)
                    s3.upload(file, target_directory_name)


            self.util.log("Copy process ended for " + file.source + " to " + file.target_file_name)

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
            self.files = self.config.load()
            self.copy()
        except Exception as e:
            self.util.log(str(e.args))


Engine().start()  # Performs the automated processes for automated backups

if not disallow_cleaner:
    Cleaner().start()  # Handles automatic cleanup for old files. Disabled via config file
