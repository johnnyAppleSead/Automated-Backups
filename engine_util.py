from datetime import date


def empty(obj):
    is_null = (obj is None)
    is_empty = (obj == '')

    return is_null or is_empty


def get_file_name(directory):
    if empty(directory):
        raise Exception('Empty file path')

    spl = directory.split('\\')
    length = len(spl)
    source_file_name = spl[length - 1]
    spl2 = source_file_name.split('.')
    file_name_base = spl2[0]

    today = date.today()

    return file_name_base + ' - ' + str(today) + '.' + spl2[1]


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

