import json
import engine_util as util
from file import File
import os


class ConfigUtil:
    def __init__(self):
        self.__config = ""
        self.__env_var = "automated_backup_config"
        self.config_dir = os.environ.get(self.__env_var)

        if util.empty(self.config_dir):
            raise KeyError("Missing environment variable: " + self.__env_var)


    def load(self):
        self.__config = self.__import_config(self.config_dir)
        files = self.__parse()

        return files

    def get_value(self, key):
        print(key)
        if util.empty(key):
            util.log("Cannot get config value for empty key", "HIGH")
            return

        if util.empty(self.__config):
            self.load()

        return self.__config[key]

    def __import_config(self, file_path):
        try:
            util.log("Attempting to open filepath: " + file_path, "HIGH")
            file = open(file_path, 'r')
            self.config = json.loads(file.read())
            file.close()

            if not util.empty(self.config):
                util.log("Filepath " + file_path + " successfully opened")
                return self.config
        except FileNotFoundError:
            util.log("An error occurred while attempting to import the config file", "HIGH")

    def __parse(self):
        files = []
        file_configs = self.config['files']
        if not util.empty(file_configs):
            target_dirs = self.config['target_directories']
            for config in file_configs:
                source = config["source"]
                target = config["target"]
                if not util.empty(target_dirs):
                    if target.startswith("dir:"):
                        target_key = target.split("dir:")[1]
                        target_dir = target_dirs[target_key]

                        if not util.empty(target_dir):
                            target = target_dir["target"]
                if util.empty(source) is False and util.empty(target) is False:
                    copied_file_name = util.get_file_name(source)
                    file = File(source, target, copied_file_name, target_dir["type"])
                    files.append(file)
                else:
                    util.log("File config has empty source or target", "HIGH")

            return files
