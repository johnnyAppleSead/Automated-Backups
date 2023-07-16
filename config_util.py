import json

from engine_util import Util
from file import File
import os


class ConfigUtil:
    def __init__(self, config_override=None):
        self.__config = ""
        self.__env_var = "automated_backup_config"
        self.util = Util()

        if config_override is None:
            # directory of config file
            self.config_dir = self.util.getEnvVariable(self.__env_var)
        else:
            self.config_dir = config_override

        if self.util.empty(self.config_dir):
            raise KeyError("Invalid configuration file. Check the environment variable: " + self.__env_var)

    def load(self):
        self.__config = self.__import_config(self.config_dir)
        files = self.__parse()

        return files

    def get_value(self, key):
        if self.util.empty(key):
            self.util.log("Cannot get config value for empty key")
            return

        if self.util.empty(self.__config):
            self.load()

        return self.__config[key]

    def __import_config(self, file_path):
        try:
            self.util.log("Attempting to open filepath: " + file_path)
            file = open(file_path, 'r')
            self.config = json.loads(file.read())
            file.close()

            if not self.util.empty(self.config):
                self.util.log("Filepath " + file_path + " successfully opened")
                return self.config
        except FileNotFoundError:
            self.util.log("An error occurred while attempting to import the config file")

    def __parse(self):
        files = []
        file_configs = self.config['files']
        if not self.util.empty(file_configs):
            target_dirs = self.config['target_directories']
            for config in file_configs:
                source = config["source"]
                targets = config["target"]
                file_targets = []

                for target in targets:
                    if not self.util.empty(target_dirs):
                        if target.startswith("dir:"):
                            target_key = target.split("dir:")[1]
                            target_dir = target_dirs[target_key]

                            if not self.util.empty(target_dir):
                                file_targets.append(target_dir)
                        else:
                            file_targets.append({
                                "target": target,
                                "type": "local",
                                "subtype": "local"
                            })
                            # Later need to append unmanaged target directories
                if self.util.empty(source) is False and self.util.empty(target) is False:
                    file = File(source, file_targets)
                    files.append(file)
                else:
                    self.util.log("File config has empty source or target")

            return files
