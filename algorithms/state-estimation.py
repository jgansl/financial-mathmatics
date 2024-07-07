import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.kalman_filter import KalmanFilter

# Parameters
symbol = 'SPY'
start_date = '2020-01-01'
end_date = '2023-01-01'
short_window = 40
long_window = 100
initial_cash = 10000

# Fetch historical data
data = yf.download(symbol, start=start_date, end=end_date)
data['Returns'] = data['Adj Close'].pct_change()

# State Estimation using Moving Averages
data['Short_MA'] = data['Adj Close'].rolling(window=short_window, min_periods=1).mean()
data['Long_MA'] = data['Adj Close'].rolling(window=long_window, min_periods=1).mean()
data.dropna(inplace=True)

# Trading signals
data['Signal'] = 0
data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1, 0)
data['Position'] = data['Signal'].diff()

# Backtesting
cash = initial_cash
position = 0
portfolio_value = []

for index, row in data.iterrows():
   if row['Position'] == 1:  # Buy signal
      position = cash / row['Adj Close']
      cash = 0
   elif row['Position'] == -1:  # Sell signal
      cash = position * row['Adj Close']
      position = 0
   portfolio_value.append(cash + position * row['Adj Close'])

data['Portfolio_Value'] = portfolio_value

# Plotting results
plt.figure(figsize=(12, 6))
plt.plot(data['Adj Close'], label='SPY Adjusted Close')
plt.plot(data['Short_MA'], label='Short Moving Average (40 days)')
plt.plot(data['Long_MA'], label='Long Moving Average (100 days)')
plt.plot(data.index, data['Portfolio_Value'], label='Portfolio Value', color='black', linestyle='--')
plt.legend(loc='best')
plt.title('SPY Moving Average Crossover Backtest')
plt.show()

# Performance metrics
total_return = (data['Portfolio_Value'].iloc[-1] - initial_cash) / initial_cash
annualized_return = ((1 + total_return) ** (252 / len(data))) - 1
print(f'Total Return: {total_return:.2%}')
print(f'Annualized Return: {annualized_return:.2%}')