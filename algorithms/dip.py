import yfinance as yf
from datetime import datetime, timedelta

# Function to check if current price is 15% lower than the highest price in the past 52 weeks
def check_price_drop(ticker, dip=0.85, days=365):
    try:
        # Fetch historical data for the past 5 years
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days)  # Fetching data for 5 years
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            print(f"No data available for {ticker}.")
            return False
        
        # Calculate the highest price in the past 52 weeks
        highest_price_52weeks = hist['Close'].max()
        
        # Get the current price
        current_price = stock.history(period="1d")['Close'].iloc[0]
        
        # Check if the current price is 15% lower than the highest price in the past 52 weeks
        if current_price <= dip * highest_price_52weeks:
            return True
        else:
            return False
    
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return False

# # List of Dow 30 tickers
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
# dow30_tickers = [
#     "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG",
#     "FB", "BRK-B", "JNJ", "V", "PG",
#     "JPM", "NVDA", "HD", "UNH", "DIS",
#     "PYPL", "MA", "VZ", "ADBE", "CRM",
#     "XOM", "MRK", "NFLX", "CMCSA", "ABT",
#     "PFE", "PEP", "KO", "T", "INTC"
# ]
dow30_tickers = dow_30_tickers

# Scan through Dow 30 tickers
for ticker in dow30_tickers:
    if check_price_drop(ticker):
        print(f"{ticker}: Current price is 15% or more lower than the highest price in the past 365 days.")
    # else:
    #     print(f"{ticker}: Current price is not 15% lower than the highest price in the past 52 weeks.")
print()
for ticker in dow30_tickers:
    if check_price_drop(ticker, .75):
        print(f"{ticker}: Current price is 25% or more lower than the highest price in the past 365 days.")

print()
for ticker in dow30_tickers:
    if check_price_drop(ticker, .15):
        print(f"{ticker}: Current price is 15% or more lower than the highest price in the past 90 days.")