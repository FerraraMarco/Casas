import pandas as pd
import traces
from function import read_all

tsList = read_all("HH113-AllLight.csv")
start = pd.to_datetime("2011-06-15 7:30:00")
end = pd.to_datetime("2012-11-04 18:00:00")
delta = pd.to_timedelta("00:30:00")
iteration = int((end - start) / delta)
count = traces.TimeSeries.merge(tsList, operation=sum)
df = pd.DataFrame(columns=["Date", "WeightAVG"])

for i in range(0, iteration):
    histogram = count.distribution(start, start + delta)
    df.loc[i, "Date"] = start
    df.loc[i, "WeightAVG"] = histogram.mean()
    start = start + delta

df.to_csv("HH113-WeightedAVG.csv", index=False)
