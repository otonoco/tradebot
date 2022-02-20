import datetime


def dictMerge(dict1, dict2):
    return {**dict1, **dict2}


def addDate(date):
    return date + datetime.timedelta(1)
