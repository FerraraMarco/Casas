import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import matplotlib
from pylab import rcParams

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

df = pd.read_csv("HH113-WeightedAVG.csv")
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
y = df.copy()
y.columns = ['Date', 'Lights']
y = y.sort_values('Date')
y = y.groupby('Date')['Lights'].sum().reset_index()
y = y.set_index('Date')
y.plot(figsize=(15, 6))

rcParams['figure.figsize'] = 18, 8
decomposition = sm.tsa.seasonal_decompose(y, model='additive', period=30)
fig = decomposition.plot()
plt.show()
"""p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue"""
mod = sm.tsa.statespace.SARIMAX(y,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])
results.plot_diagnostics(figsize=(16, 8))
plt.show()
pred = results.get_prediction(start=pd.to_datetime('2012-09-15 07:30:00'), dynamic=False)
pred_ci = pred.conf_int()
predicted = pred.predicted_mean
predicted = predicted.reset_index()
predicted.columns = ['Date', 'LightsForecasted']
predicted.loc[predicted['LightsForecasted'] < 0, 'LightsForecasted'] = 0
predicted = predicted.set_index('Date')
ax = y['2011':].plot(label='observed')
predicted.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Light')
plt.legend()
plt.show()

y_forecasted = predicted
y_truth = y['2012-09-15 07:30:00':]
y_forecasted = y_forecasted.reset_index()
y_forecasted.columns = ['Date', 'Lights']
y_truth = y_truth.reset_index()
mse = i = 0
for i in range(len(y_forecasted)):
    mse += ((y_forecasted.loc[i, 'Lights'] - y_truth.loc[i, 'Lights']) ** 2)
mse = mse / i
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))
pred_uc = results.get_forecast(steps=48)
pred_ci = pred_uc.conf_int()
ax = y.plot(label='observed', figsize=(14, 7))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Lights')
plt.legend()
plt.show()
