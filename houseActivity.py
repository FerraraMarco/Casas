import csv
import pandas as pd
import numpy
from function import connection, exe, rem
from time import strftime, gmtime

cursor = connection()

with open('houseActivityStats.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Houses", "Activity", "Occurred", "Average Duration",
                     "Avg Duration Dev Std", "Avg Duration Dev Std (min)", "Average occurred (days)"])

df = pd.read_csv("houseActivityStats.csv")
df1 = pd.read_csv("houseStats.csv")

queryAB = 'select distinct(house, name) from activity.activity order by(house, name)'
queryCount = "select count (*) from activity.activity group by(house, name) order by(house, name)"

colAB = exe(cursor, queryAB)
colCount = exe(cursor, queryCount)

for i in range(len(colAB)):
    houseAc = str(colAB[i]).split(",")
    df.loc[i, 'Houses'] = rem(houseAc[0])
    df.loc[i, 'Activity'] = rem(houseAc[1])
    df.loc[i, 'Occurred'] = rem(colCount[i])
    queryDur = "select duration from activity.activity where house ='" + rem(houseAc[0]) + "' and name = '" \
               + rem(houseAc[1]) + "'"

    colDur = exe(cursor, queryDur)
    tot = 0
    stdVetAVG = []
    for k in range(len(colDur)):
        tot += float(rem(colDur[k]))
        stdVetAVG.append(int(rem(colDur[k])))
    inSec = (tot / float(rem(colCount[i]))) / 1000

    df.loc[i, 'Average Duration'] = strftime("%H:%M:%S", gmtime(inSec))
    df.loc[i, 'Avg Duration Dev Std'] = round(numpy.std(stdVetAVG), 4)
    df.loc[i, 'Avg Duration Dev Std (min)'] = strftime("%H:%M:%S", gmtime(round(numpy.std(stdVetAVG), 4) / 1000))
    df.loc[i, "Average occurred (days)"] = round(float(df.loc[i, "Occurred"]) /
                                                 float(df1.loc[df1["Houses"] == rem(houseAc[0]),
                                                               "Test Duration (days)"]), 2)

df.to_csv("houseActivityStats.csv")
