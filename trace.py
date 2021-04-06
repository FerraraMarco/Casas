from datetime import datetime
import traces
from function import connection, read_all
import pandas.io.sql as sqlio

conn = connection(1)
sqlCon = "select name, id from activity.sensor where house = 'HH113' and name like 'L0__'"
dfC = sqlio.read_sql_query(sqlCon, conn)

for i in range(len(dfC)):
    print(dfC.loc[i, "name"])
    sql = "select date, state from activity.event where sensor = '" + str(dfC.loc[i, "id"]) + "' order by(date)"
    dataframe = sqlio.read_sql_query(sql, conn)
    dataframe.to_csv("HH113-" + str(dfC.loc[i, "name"]) + ".csv")

ts_list = read_all('HH113-L0**.csv')
count = traces.TimeSeries.merge(ts_list, operation=sum)
histogram = count.distribution(start=datetime(2012, 2, 1,  8,  0,  0), end=datetime(2012, 2, 1,  12 + 6,  0,  0))
print(histogram.median())
