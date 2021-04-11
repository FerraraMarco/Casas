import glob
import psycopg2
from datetime import datetime
import traces
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

name_db = "casas"
username_db = "postgres"
password_db = "marco"
host_db = "127.0.0.1"
port_db = "5432"


def read_all(pattern):
    # Read all of the CSVs in a directory matching the filename pattern as TimeSeries.
    result = []
    for filename in glob.iglob(pattern):
        ts = traces.TimeSeries.from_csv(filename, time_column=0, value_column=1, value_transform=int, default=0)
        ts.compact()
        result.append(ts)
    return result


def connection(val):  # create a connection with the db
    if val is None:
        connect = psycopg2.connect(user=username_db, password=password_db,
                                   database=name_db, host=host_db, port=port_db)
        cursor = connect.cursor()
        connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return cursor
    else:
        connect = psycopg2.connect(user=username_db, password=password_db,
                                   database=name_db, host=host_db, port=port_db)
        return connect


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
    if len(date.split(",")) <= 7:
        return datetime.strptime(str(date), "(datetime.datetime(%Y, %m, %d, %H, %M, %S),)")
    else:
        return datetime.strptime(str(date), "(datetime.datetime(%Y, %m, %d, %H, %M, %S, %f),)")


def calc(s, e):  # difference between dates expressed in days
    return str((chg(e) - chg(s)).days)
