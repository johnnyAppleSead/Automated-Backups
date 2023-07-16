from logger import Logger
import os
#from config_util import ConfigUtil


class Util:
    def __init__(self):
        #self.config = ConfigUtil()
        #self.__options = self.config.get_value("options")
        #disable_logger = self.__options["disable_logger"]

        self.logger = Logger(False)

    def log(self, msg, verbosity="High"):
        if not self.empty(msg):
            self.logger.log(msg, verbosity)

    def empty(self, obj):
        is_null = (obj is None)
        is_empty = (obj == '')

        return is_null or is_empty

    def getEnvVariable(self, key):
        if self.empty(key):
            self.log("Unable to retrieve env variable: Empty Environment Variable Key")

        try:
            return os.environ.get(key)
        except:
            print("Error retrieving env variable")
            return ""
