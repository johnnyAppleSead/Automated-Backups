class Logger:
    def __init__(self, disable_logger=False):
        self.disable_logger = disable_logger

    def log(self, log_message, verbosity=None):
        if log_message is None or log_message == "":
            return

        if self.disable_logger:
            print("Logger disabled.")
            return

        if verbosity == "HIGH":
            print(log_message)

        log_file = "C:\\Users\\johna\\Documents\\automated_backup_log.txt" # Need to update this from static to dynamic

        try:
            file = open(log_file, "a")
            file.write(log_message + "\n")
            file.close()
        except FileNotFoundError:
            print("WARN:Unable to log due to a file issue: " + log_message)

