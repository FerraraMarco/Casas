import traces
from function import connection, read_all
import pandas.io.sql as sqlio
import matplotlib.pyplot as plt
import pandas as pd

conn = connection(1)
sqlCon = "select name, id from activity.sensor where house = 'HH113' and name like 'L0__'"
dfC = sqlio.read_sql_query(sqlCon, conn)

for i in range(len(dfC)):
    sql = "select date, state from activity.event where sensor = '" + str(dfC.loc[i, "id"]) + "' order by(date)"
    dataframe = sqlio.read_sql_query(sql, conn)
    dataframe.to_csv("HH113-" + str(dfC.loc[i, "name"]) + ".csv", index=False)

ts_list = read_all('HH113-L0**.csv')
count = traces.TimeSeries.merge(ts_list, operation=sum)
dfTime = pd.DataFrame(count)
dfTime.columns = ['Date', 'Value']
# histogram = count.distribution(start=datetime(2011, 6, 15,  16, 00, 00), end=datetime(2011, 6, 15,  17, 00, 00))
plt.plot(dfTime[['Date']], dfTime[['Value']])
plt.show()
