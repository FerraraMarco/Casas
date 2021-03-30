import csv
import psycopg2
import pandas as pd
import numpy
from houseData import rem
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from time import strftime, gmtime

name_db = "casas"
username_db = "postgres"
password_db = "marco"
host_db = "127.0.0.1"
port_db = "5432"

connection = psycopg2.connect(user=username_db, password=password_db, database=name_db, host=host_db, port=port_db)
cursor = connection.cursor()
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

with open('houseActivityStats.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Houses", "Activity", "Occurred", "Average Duration",
                     "Avg Duration Dev Std", "Avg Duration Dev Std (min)", "Average occurred (days)"])
df = pd.read_csv("houseActivityStats.csv")
df1 = pd.read_csv("houseStats.csv")

queryAB = 'select distinct(house, name) from activity.activity order by(house, name)'
queryCount = "select count (*) from activity.activity group by(house, name) order by(house, name)"
cursor.execute(queryAB)
colAB = cursor.fetchall()
cursor.execute(queryCount)
colCount = cursor.fetchall()

for i in range(len(colAB)):
    houseAc = str(colAB[i]).split(",")
    df.loc[i, 'Houses'] = rem(str(houseAc[0]))
    df.loc[i, 'Activity'] = rem(str(houseAc[1]))
    df.loc[i, 'Occurred'] = rem(str(colCount[i]))
    queryDur = "select duration from activity.activity where house ='" + rem(str(houseAc[0])) + "' and name = '" \
               + rem(str(houseAc[1])) + "'"
    cursor.execute(queryDur)
    colDur = cursor.fetchall()
    tot = 0
    stdVetAVG = []
    for k in range(len(colDur)):
        tot += float(rem(str(colDur[k])))
        stdVetAVG.append(int(rem(str(colDur[k]))))
    inSec = (tot / float(rem(str(colCount[i])))) / 1000

    df.loc[i, 'Average Duration'] = strftime("%H:%M:%S", gmtime(inSec))
    df.loc[i, 'Avg Duration Dev Std'] = round(numpy.std(stdVetAVG), 4)
    df.loc[i, 'Avg Duration Dev Std (min)'] = strftime("%H:%M:%S", gmtime(round(numpy.std(stdVetAVG), 4) / 1000))
    df.loc[i, "Average occurred (days)"] = round(float(df.loc[i, "Occurred"]) /
                                                 float(df1.loc[df1["Houses"] == rem(str(houseAc[0])),
                                                               "Test Duration (days)"]), 2)

df.to_csv("houseActivityStats.csv")
