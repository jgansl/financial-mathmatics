import time
from ib_insync import *

# Connect to IBKR API
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Define the stock and option parameters
stock_symbol = 'SPY'
expiry = '20240809'
strike = 550
right = 'C'  # 'C' for Call, 'P' for Put

# Define the stock and option contracts
stock = Stock(stock_symbol, 'SMART', 'USD')
option = Option(stock_symbol, expiry, strike, right, 'SMART')

# Function to place an order
def place_order(contract, action, quantity):
   order = MarketOrder(action, quantity)
   trade = ib.placeOrder(contract, order)
   return trade

# Function to check profit/loss and adapt strategy
def check_profit_and_adapt():
   # Placeholder for profit/loss calculation and strategy adaptation
   # This would involve complex logic and data analysis
   pass

# Main trading loop
try:
   while True:
      # Request market data for the stock and option
      ib.qualifyContracts(stock)
      ib.qualifyContracts(option)
      stock_data = ib.reqMktData(stock)
      option_data = ib.reqMktData(option)

      # Example trading logic (simplified)
      if stock_data.last > 150:
         # Buy a call option if stock price is above 150
         place_order(option, 'BUY', 1)
      elif stock_data.last < 140:
         # Sell a call option if stock price is below 140
         place_order(option, 'SELL', 1)

      # Check profit/loss and adapt strategy
      check_profit_and_adapt()

      # Wait for a while before the next iteration
      time.sleep(60)

except KeyboardInterrupt:
   print("Trading bot stopped by user")

finally:
   ib.disconnect()
