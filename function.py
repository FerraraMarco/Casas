from datetime import datetime


def rem(text):                          # remove extra characters when pulling out from db
    text = str(text.replace("(", ""))
    text = str(text.replace(")", ""))
    text = str(text.replace(",", ""))
    text = str(text.replace("'", ""))
    text = str(text.replace("[", ""))
    text = str(text.replace("]", ""))
    return text


def chg(val):                           # convert string into dd/mm/yyyy hh:mm:ss.
    if len(str(val)) < 45:
        return datetime.strptime(str(val), "(datetime.datetime(%Y, %m, %d, %H, %M, %S),)")
    else:
        return datetime.strptime(str(val), "(datetime.datetime(%Y, %m, %d, %H, %M, %S, %f),)")


def calc(s, e):                         # difference between dates expressed in days
    return str((chg(e) - chg(s)).days)
