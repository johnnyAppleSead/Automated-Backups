from file import File
import json
import engine_util as util
import shutil


class Engine:
    def __init__(self):
        self.config = ""
        self.files = []
        
    def import_config(self, file_path):
        try:
            print("Attempting to open filepath: " + file_path)
            file = open(file_path)
            self.config = json.loads(file.read())
        except:
            print("An error occurred while attempting to import the config file")

    def parse(self):
        file_configs = self.config['files']
        if not util.empty(file_configs):
            for config in file_configs:
                source = config["source"]
                target = config["target"]

                if util.empty(source) == False and util.empty(target) == False:
                    copied_file_name = util.get_file_name(source)
                    file = File(source, target, copied_file_name)
                    self.files.append(file)
                else:
                    print("File config has empty source or target")

    def copy(self):
        for file in self.files:
            print("Beginning copy process for " + file.source + " to " + file.target)
            shutil.copy(file.source, (file.target + "\\" + file.target_file_name))
            print("Copy process ended for " + file.source + " to " + file.target)

    def start(self):
        self.import_config("D:\\Github Projects\\Automated Backups\\config.json")
        #self.import_config("D:\Projects\Python\Automated Backups\config.json")
        self.parse()
        self.copy()


engine = Engine()
engine.start()
