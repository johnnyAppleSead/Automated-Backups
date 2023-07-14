import os
import time
from config_util import ConfigUtil
from engine_util import Util


class Cleaner:
    def __init__(self):
        self.util = Util()

        self.config = ConfigUtil()
        options = self.config.get_value(key="options")
        if not self.util.empty(options):
            self.__days_to_preserve = options['days_to_preserve']
            self.disable_cleaner = options["disable_cleaner"]

        self.util.log("Cleaner initialized")

    def __delete(self, file_dir):
        if not self.util.empty(file_dir) and os.path.isfile(file_dir):
            self.util.log("Cleaner deleting file: " + file_dir)
            os.remove(file_dir)

    def __process(self):
        self.disable_cleaner = True
        if self.disable_cleaner:
            self.util.log("Clean disabled. Cleaner stopped")
            return

        now = time.time()
        target_directories = self.config.get_value(key="target_directories")

        for target in target_directories:
            target_obj = target_directories[target]
            if target_obj["type"] == "local":
                key = target_obj["target"]
                directory = target_directories[key]
                for f in os.listdir(directory):
                    f = os.path.join(directory, f)
                    if os.stat(f).st_mtime < now - (86400 * self.__days_to_preserve):
                        if os.path.isfile(f):
                            self.__delete(f)

    def start(self):
        try:
            self.util.log("Beginning cleaning process")
            self.__process()
            self.util.log("Cleaning process complete")
        except KeyError:
            self.util.log("Config file missing key")
        except FileNotFoundError:
            self.util.log("FileNotFoundError thrown")
