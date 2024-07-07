import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define the DOW 30 ticker symbols
dow_30_tickers = [
    "MMM", "AXP", "AMGN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", 
    "DOW", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", 
    "MSFT", "NKE", "PG", "TRV", "UNH", "VZ", "V", "WBA", "WMT"
]

# Define trading parameters
drop_threshold = 0.15
profit_target = 0.10
loss_cut = 0.05

# Fetch historical data
data = {}
for ticker in dow_30_tickers:
   stock = yf.Ticker(ticker)
   hist = stock.history(period="1y")
   data[ticker] = hist

# Track positions
positions = {}

# Function to check trading conditions
def check_conditions(ticker, row):
   global positions
   # Calculate 52 week high
   high_52week = data[ticker]["High"].max()
   current_price = row["Close"]
   
   # Check if the stock dropped 15% from its 52 week high
   if current_price <= high_52week * (1 - drop_threshold):
      # Buy condition
      if ticker not in positions:
         positions[ticker] = {"buy_price": current_price, "date_bought": row.name}
         print(f"Buying {ticker} at {current_price} on {row.name}")
   elif ticker in positions:
      # Check if we should sell the stock
      buy_price = positions[ticker]["buy_price"]
      if current_price >= buy_price * (1 + profit_target):
         # Sell condition for profit
         print(f"Selling {ticker} at {current_price} on {row.name} for profit")
         del positions[ticker]
      elif current_price <= buy_price * (1 - loss_cut):
         # Sell condition for loss
         print(f"Selling {ticker} at {current_price} on {row.name} for loss")
         del positions[ticker]

# Simulate trading over the past year
for date in data[dow_30_tickers[0]].index:
   for ticker in dow_30_tickers:
      row = data[ticker].loc[date]
      check_conditions(ticker, row)