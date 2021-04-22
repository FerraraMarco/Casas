from pylab import rcParams
import warnings
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import matplotlib

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

dfTime = pd.read_csv('HH113-WeightedAVG.csv')
dfTime['Date'] = pd.to_datetime(dfTime['Date'], format='%Y-%m-%d %H:%M:%S.%f')
dfTimeResample = dfTime.resample('30T', on='Date').mean()
dfTimeResample = dfTimeResample.fillna(0)
dfTimeResample.to_csv('HH113-LightResampled.csv')
dfTimeResample.plot(figsize=(15, 6))
rcParams['figure.figsize'] = 18, 8
decomposition = sm.tsa.seasonal_decompose(dfTimeResample, period=30, model='additive')
fig = decomposition.plot()
plt.show()

dfSeasonal = pd.DataFrame(columns=["Order", "Seasonal order", "Result"])

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
i = 0
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(dfTimeResample, order=param, seasonal_order=param_seasonal,
                                            enforce_stationarity=False, enforce_invertibility=False)
            results = mod.fit()
            dfSeasonal.loc[i, 'Order'] = param
            dfSeasonal.loc[i, 'Seasonal order'] = param_seasonal
            dfSeasonal.loc[i, 'Result'] = results.aic
            i += 1
        except:
            continue
dfSeasonal.to_csv("ARIMA.csv", index=False)
df = pd.read_csv("ARIMA.csv")
row = df.loc[df['Result'] == df['Result'].min()]
mod = sm.tsa.statespace.SARIMAX(dfTimeResample, order=(1, 0, 1), seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False, enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

results.plot_diagnostics(figsize=(16, 8))
plt.show()
