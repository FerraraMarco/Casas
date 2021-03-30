import csv
import psycopg2
import pandas as pd
import numpy
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime


def rem(text):
    text = str(text.replace("(", ""))
    text = str(text.replace(")", ""))
    text = str(text.replace(",", ""))
    text = str(text.replace("'", ""))
    text = str(text.replace("[", ""))
    text = str(text.replace("]", ""))
    return text


def chg(val):
    return datetime.strptime(str(val), "(datetime.datetime(%Y, %m, %d, %H, %M, %S, %f),)")


def calc(s, e):
    return str((chg(e) - chg(s)).days)


name_db = "casas"
username_db = "postgres"
password_db = "marco"
host_db = "127.0.0.1"
port_db = "5432"

connection = psycopg2.connect(user=username_db, password=password_db, database=name_db, host=host_db, port=port_db)
cursor = connection.cursor()
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

queryA = "select id from activity.house"
queryB = "select min(date) from activity.event join activity.sensor on sensor.id=event.sensor " \
         "group by(sensor.house) order by sensor.house"
queryC = "select max(date) from activity.event join activity.sensor on sensor.id=event.sensor " \
         "group by(sensor.house) order by sensor.house"
queryE = "select count(*) from activity.event join activity.sensor on sensor.id=event.sensor group by(sensor.house) " \
         "order by(sensor.house) "
queryG = "select count(distinct(name)) from activity.activity group by(house) order by (house)"
queryH = "select count(*) from activity.activity group by(house) order by(house)"
cursor.execute(queryA)
colA = cursor.fetchall()
cursor.execute(queryB)
colB = cursor.fetchall()
cursor.execute(queryC)
colC = cursor.fetchall()
cursor.execute(queryE)
colE = cursor.fetchall()
cursor.execute(queryG)
colG = cursor.fetchall()
cursor.execute(queryH)
colH = cursor.fetchall()

with open('houseStats.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Houses", "Start Date Test", "End Date Test", "Test Duration (days)", "Total Events",
                     "Average Events (days)", "StdDevEvents", "Different Activities", "Total Activities",
                     "Average Activities (days)", "StdDevActivities"])

df = pd.read_csv("houseStats.csv")

for i in range(len(colA)):
    df.loc[i, 'Houses'] = rem(str(colA[i]))
    df.loc[i, 'Start Date Test'] = chg(colB[i]).date()
    df.loc[i, 'End Date Test'] = chg(colC[i]).date()
    df.loc[i, 'Test Duration (days)'] = calc(colB[i], colC[i])
    df.loc[i, 'Total Events'] = rem(str(colE[i]))
    df.loc[i, 'Average Events (days)'] = round(float(rem(str(colE[i]))) / float(calc(colB[i], colC[i])), 2)

    stdDevEv = "select  count(*) from activity.event join activity.sensor on sensor.id = event.sensor " \
               "where house = '" + rem(str(colA[i])) + "'group by(house, event.onlyDate)"
    cursor.execute(stdDevEv)
    colStdDevEV = cursor.fetchall()
    stdVetEV = []
    for k in range(len(colStdDevEV)):
        stdVetEV.append(int(rem(str(colStdDevEV[k]))))

    df.loc[i, 'StdDevEvents'] = round(numpy.std(stdVetEV), 4)
    df.loc[i, 'Different Activities'] = rem(str(colG[i]))
    df.loc[i, 'Total Activities'] = rem(str(colH[i]))
    df.loc[i, 'Average Activities (days)'] = round(float(rem(str(colH[i]))) / float(rem(str(colG[i]))), 2)

    stdDevAct = "select count(date) from activity.activity where house = '" + rem(str(colA[i])) + \
                "' group by(house, date) order by(house, date) "
    cursor.execute(stdDevAct)
    colStdDevAct = cursor.fetchall()
    stdVetAct = []
    for k in range(len(colStdDevAct)):
        stdVetAct.append(int(rem(str(colStdDevAct[k]))))

    df.loc[i, 'StdDevActivities'] = round(numpy.std(stdVetAct), 4)

df.to_csv("houseStats.csv")
