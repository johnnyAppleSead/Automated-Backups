

def empty(obj):
    is_null = (obj is None)
    is_empty = (obj == '')

    return is_null or is_empty


def log(log_message, verbosity=None):
    if log_message is None or log_message == "":
        return

    if verbosity == "HIGH":
        print(log_message)

    log_file = "C:\\Users\\johna\\Documents\\automated_backup_log.txt"

    try:
        file = open(log_file, "a")
        file.write(log_message + "\n")
        file.close()
    except FileNotFoundError:
        print("WARN:Unable to log due to a file issue: " + log_message)

