import csv
import pandas as pd
import numpy
from function import rem, chg, calc, connection, exe

cursor = connection()

queryA = "select id from activity.house"
queryB = "select min(date) from activity.event join activity.sensor on sensor.id=event.sensor " \
         "group by(sensor.house) order by sensor.house"
queryC = "select max(date) from activity.event join activity.sensor on sensor.id=event.sensor " \
         "group by(sensor.house) order by sensor.house"
queryE = "select count(*) from activity.event join activity.sensor on sensor.id=event.sensor group by(sensor.house) " \
         "order by(sensor.house) "
queryG = "select count(distinct(name)) from activity.activity group by(house) order by (house)"
queryH = "select count(*) from activity.activity group by(house) order by(house)"

colA = exe(cursor, queryA)
colB = exe(cursor, queryB)
colC = exe(cursor, queryC)
colE = exe(cursor, queryE)
colG = exe(cursor, queryG)
colH = exe(cursor, queryH)

with open('houseStats.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Houses", "Start Date Test", "End Date Test", "Test Duration (days)", "Total Events",
                     "Average Events (days)", "StdDevEvents", "Different Activities", "Total Activities",
                     "Average Activities (days)", "StdDevActivities"])

df = pd.read_csv("houseStats.csv")

for i in range(len(colA)):
    df.loc[i, 'Houses'] = rem(colA[i])
    df.loc[i, 'Start Date Test'] = chg(colB[i]).date()
    df.loc[i, 'End Date Test'] = chg(colC[i]).date()
    df.loc[i, 'Test Duration (days)'] = calc(colB[i], colC[i])
    df.loc[i, 'Total Events'] = rem(colE[i])
    df.loc[i, 'Average Events (days)'] = round(float(rem(colE[i])) / float(calc(colB[i], colC[i])), 2)

    stdDevEv = "select  count(*) from activity.event join activity.sensor on sensor.id = event.sensor " \
               "where house = '" + rem(colA[i]) + "'group by(house, event.onlyDate)"
    colStdDevEV = exe(cursor, stdDevEv)
    stdVetEV = []
    for k in range(len(colStdDevEV)):
        stdVetEV.append(int(rem(colStdDevEV[k])))

    df.loc[i, 'StdDevEvents'] = round(numpy.std(stdVetEV), 4)
    df.loc[i, 'Different Activities'] = rem(colG[i])
    df.loc[i, 'Total Activities'] = rem(colH[i])
    df.loc[i, 'Average Activities (days)'] = round(float(rem(colH[i])) / float(calc(colB[i], colC[i])), 2)

    stdDevAct = "select count(date) from activity.activity where house = '" + rem(colA[i]) + \
                "' group by(house, date) order by(house, date) "
    colStdDevAct = exe(cursor, stdDevAct)
    stdVetAct = []
    for k in range(len(colStdDevAct)):
        stdVetAct.append(int(rem(colStdDevAct[k])))

    df.loc[i, 'StdDevActivities'] = round(numpy.std(stdVetAct), 4)

df.to_csv("houseStats.csv")
