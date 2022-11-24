import shutil
import os, time
import engine_util as util
from config_util import ConfigUtil


class Cleaner:
    def __init__(self):
        self.config = ConfigUtil()
        options = self.config.get_value(key="options")
        if not util.empty(options):
            self.__days_to_preserve = options['days_to_preserve']

        self.disable_cleaner = options["disable_cleaner"]

        util.log("Cleaner initialized")

    def __delete(self, file_dir):
        if not util.empty(file_dir) and os.path.isfile(file_dir):
            util.log("Cleaner deleting file: " + file_dir, "HIGH")
            os.remove(file_dir)

    def __process(self):
        if self.disable_cleaner:
            util.log("Clean disabled. Cleaner stopped", "HIGH")
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
            util.log("Beginning cleaning process", "HIGH")
            self.__process()
            util.log("Cleaning process complete", "HIGH")
        except KeyError:
            util.log("Config file missing key")
        except FileNotFoundError:
            util.log("FileNotFoundError thrown")
