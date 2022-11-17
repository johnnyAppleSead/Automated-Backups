from datetime import date


def empty(obj):
    is_null = (obj is None)
    is_empty = (obj == '')

    return is_null or is_empty


def get_file_name(dir):
    if empty(dir):
        raise Exception('Empty file path')

    spl = dir.split('\\')
    length = len(spl)
    source_file_name = spl[length - 1]
    spl2 = source_file_name.split('.')
    file_name_base = spl2[0]

    today = date.today()

    return file_name_base + str(today) + '.' + spl2[1]
