import traces
from function import connection, read_all
import pandas.io.sql as sqlio
import matplotlib.pyplot as plt
import pandas as pd

start_time = pd.to_datetime('2012-06-15 00:00:00.0000')
end_time = pd.to_datetime('2012-06-16 23:59:59.9999')

conn = connection(1)
sqlCon = "select name, id from activity.sensor where house = 'HH113' and name like 'L0__'"
dfC = sqlio.read_sql_query(sqlCon, conn)

for i in range(len(dfC)):
    sql = "select date, state from activity.event where sensor = '" \
          + str(dfC.loc[i, "id"]) + "' order by(date)"
    dataframe = sqlio.read_sql_query(sql, conn)
    dataframe.to_csv("HH113-" + str(dfC.loc[i, "name"]) + ".csv", index=False)

ts_list = read_all('HH113-L0**.csv')
count = traces.TimeSeries.merge(ts_list, operation=sum)

start = pd.to_datetime("2011-06-15 07:30:00")
end = pd.to_datetime("2011-06-15 08:00:00")
histogram = count.distribution(start, end)
print(histogram)

dfTime = pd.DataFrame(count)
dfTime.columns = ['Date', 'Value']
dfTime.to_csv('HH113-AllLight.csv', index=False)
df = dfTime.loc[(dfTime['Date'] >= start_time) & (dfTime['Date'] < end_time)]
plt.plot(df[['Date']], df[['Value']])
plt.show()
