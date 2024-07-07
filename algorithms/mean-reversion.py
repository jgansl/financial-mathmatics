import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

# Load historical data
data = pd.read_csv('futures_data.csv')
prices = data['Close']

# Estimate parameters of the Ornstein-Uhlenbeck process
returns = np.diff(np.log(prices))
mean_return = np.mean(returns)
volatility = np.std(returns)
theta = 1 / np.mean(np.abs(returns))

# Generate trading signals
window = 30
signals = pd.DataFrame(index=prices.index)
signals['price'] = prices
signals['rolling_mean'] = prices.rolling(window=window).mean()
signals['signal'] = 0
signals['signal'][window:] = np.where(prices[window:] > signals['rolling_mean'][window:], -1, 1)

# Simulate the strategy
signals['position'] = signals['signal'].shift()
signals['strategy_returns'] = signals['position'] * returns
signals['cumulative_returns'] = (1 + signals['strategy_returns']).cumprod()

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(signals['cumulative_returns'], label='Strategy Returns')
plt.plot((1 + returns).cumprod(), label='Market Returns')
plt.legend()
plt.show()
