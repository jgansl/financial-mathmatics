import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from decimal import Decimal, getcontext

# # Set the precision for Decimal
getcontext().prec = 10

# Define log file
log_file = "../.data/trading_log.txt"

# Define the DOW 30 ticker symbols
dow_30_tickers = [
   "AAPL",
   "AMD", #
   "AMGN",
   "AMZN",
   "AXP",
   "BA",
   "CAT",
   "CRM",
   "CSCO",
   "CVX",
   "DIS",
   "DOW",
   "GS",
   "HD",
   "HON",
   "IBM",
   "INTC",
   "JNJ",
   "JPM",
   "KO",
   "MCD",
   "MMM",
   "MRK",
   "MSFT",
   "NKE",
   "PG",
   "TRV",
   "UNH",
   "V",
   "VZ",
   "WBA", #
   "WMT"
]

# Define trading parameters
drop_threshold = Decimal('0.15')
profit_target = Decimal('0.10')
loss_cut = Decimal('0.05')

# Define logging function
def log(message):
   with open(log_file, "a") as f:
      f.write(message + "\n")


# Fetch historical data (5 years)
data = {}
for ticker in dow_30_tickers:
   stock = yf.Ticker(ticker)
   hist = stock.history(period="2y")
   data[ticker] = hist
   log(f"Fetched data for {ticker}")

# Track positions and portfolio value
positions = {}
portfolio_value = []
cash = Decimal('100000.00')  # Starting with $100,000

# Function to calculate portfolio value
def calculate_portfolio_value(date):
   total_value = cash
   # for ticker, pos in positions.items():
   #    if date in data[ticker].index:
   #       current_price = Decimal(data[ticker].loc[date, 'Close'])
   #       stock_value = pos['quantity'] * current_price
   #       total_value += stock_value
   return total_value

# Function to check trading conditions
def check_conditions(date):
   global cash
   for ticker, hist in data.items():
      # Skip if we don't have data for the date
      if date not in hist.index:
         continue
        
      current_price = Decimal(hist.loc[date, 'Close'])
      #   if ticker in positions:
      #       buy_price = positions[ticker]['buy_price']
      #       # Check for sell conditions
      #       if current_price >= buy_price * (1 + profit_target):
      #           cash += positions[ticker]['quantity'] * current_price
      #           log(f"Selling {positions[ticker]['quantity']} shares of {ticker} at ${current_price:.2f} on {date} for profit")
      #           del positions[ticker]
      #       elif current_price <= buy_price * (1 - loss_cut):
      #           cash += positions[ticker]['quantity'] * current_price
      #           log(f"Selling {positions[ticker]['quantity']} shares of {ticker} at ${current_price:.2f} on {date} for loss")
      #           del positions[ticker]
      #   else:
      # Check for buy conditions
      start_date_52w = date - timedelta(weeks=52)
      hist_52w = hist[start_date_52w:date]  # Slice data for the past 52 weeks including current date
      max_price_52w = Decimal(hist_52w['Close'].max())
      if current_price <= max_price_52w * (1 - drop_threshold):
         max_investment = cash * Decimal('0.15')  # Maximum investment adjusted to 15% of cash
         quantity = (max_investment // current_price).quantize(Decimal('1'))
         if quantity > 0:
            max_price_date = hist_52w[hist_52w['Close'] == max_price_52w].index[0]
            positions[ticker] = {
               'buy_price': current_price,
               'quantity': quantity,
               '52w_high_date': max_price_date
            }
            cash -= quantity * current_price
            log(f"Buying {quantity} shares of {ticker} at ${current_price:.2f} on {date} for a total of ${quantity * current_price:.2f}")
            log(f"  52-week high for {ticker}: ${max_price_52w:.2f} on {max_price_date.strftime('%Y-%m-%d')}")

   # Output portfolio value and positions at each step
   port_val = calculate_portfolio_value(date)
   portfolio_value.append(port_val)
   log(f"Portfolio value on {date}: ${port_val:.2f}")
   # log("Current positions:")
   # for ticker, pos in positions.items():
   #    log(f"  {ticker}: {pos['quantity']} shares at ${pos['buy_price']:.2f} each, bought at 52w high on {pos['52w_high_date'].strftime('%Y-%m-%d')}")

# Simulate trading
start_date = max([hist.index.min() for hist in data.values()])
end_date = min([hist.index.max() for hist in data.values()])
dates = pd.date_range(start=start_date, end=end_date)

# Clear log file before running
with open(log_file, "w") as f:
   f.write("")

for date in dates:
   check_conditions(date)

# Output final results
final_value = calculate_portfolio_value(end_date)
log(f"Final Portfolio Value: ${final_value:.2f}")
log("Final Positions:")
for ticker, pos in positions.items():
   log(f"{ticker}: {pos['quantity']} shares at ${pos['buy_price']:.2f} each, bought at 52w high on {pos['52w_high_date'].strftime('%Y-%m-%d')}")

# Plot portfolio value over time
plt.plot(dates, portfolio_value)
plt.xlabel("Date")
plt.ylabel("Portfolio Value ($)")
plt.title("Portfolio Value Over Time")
plt.show()