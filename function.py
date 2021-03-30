import psycopg2
from datetime import datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

name_db = ""
username_db = "postgres"
password_db = ""
host_db = "127.0.0.1"
port_db = "5432"


def connection():  # create a connection with the db
    connect = psycopg2.connect(user=username_db, password=password_db,
                               database=name_db, host=host_db, port=port_db)
    cursor = connect.cursor()
    connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return cursor


def exe(cur, query):  # execute the query and return data
    cur.execute(query)
    col = cur.fetchall()
    return col


def rem(text):  # remove extra characters when pulling out from db
    text = str(text)
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace(",", "")
    text = text.replace("'", "")
    text = text.replace("[", "")
    text = text.replace("]", "")
    return text


def chg(date):  # convert string into dd/mm/yyyy hh:mm:ss.
    if len(str(date)) < 45:
        return datetime.strptime(str(date), "(datetime.datetime(%Y, %m, %d, %H, %M, %S),)")
    else:
        return datetime.strptime(str(date), "(datetime.datetime(%Y, %m, %d, %H, %M, %S, %f),)")


def calc(s, e):  # difference between dates expressed in days
    return str((chg(e) - chg(s)).days)
