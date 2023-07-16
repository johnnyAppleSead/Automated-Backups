import os
import time
from config_util import ConfigUtil
from engine_util import Util
import shutil


class Cleaner:
    def __init__(self):
        self.util = Util()

        self.config = ConfigUtil()
        options = self.config.get_value(key="options")
        if not self.util.empty(options):
            self.__days_to_preserve = options['days_to_preserve']
            self.disable_cleaner = options["disable_cleaner"]

        self.util.log("Cleaner initialized")

    def __delete_directory(self, file_dir):
        if not self.util.empty(file_dir) and os.path.isdir(file_dir):
            try:
                shutil.rmtree(file_dir)
            except OSError as e:
                print("Cleaner error deleting file: %s : %s" % (file_dir, e.strerror))

    def __process(self):
        if self.disable_cleaner:
            self.util.log("Cleaner disabled and will not start.")
            return

        now = time.time()
        target_directories = self.config.get_value(key="target_directories")

        for target in target_directories:
            target_obj = target_directories[target]
            if target_obj["type"] == "local":
                directory = target_obj["target"]

                for f in os.listdir(directory):

                    if "Backup" in f:
                        f = os.path.join(directory, f)
                        if os.stat(f).st_mtime < now - (86400 * self.__days_to_preserve):
                            self.__delete_directory(f)

    def start(self):
        try:
            self.util.log("Beginning cleaning process", "HIGH")
            self.__process()
            self.util.log("Cleaning process complete", "HIGH")
        except KeyError:
            self.util.log("Config file missing key")
        except FileNotFoundError:
            self.util.log("FileNotFoundError thrown")
