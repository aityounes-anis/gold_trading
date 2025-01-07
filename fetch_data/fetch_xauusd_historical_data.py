import yfinance as yf
import pandas as pd

# Define the ticker symbol for XAUUSD
ticker_symbol = "GC=F"

# Define the date range
start_date = "2015-01-01"
end_date = "2025-01-07"

# Download the historical data
data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Exclude the 'Volume' column
data = data.drop(columns=['Volume'])

# Save the data to a CSV file (optional)
data.to_csv("./data/xauusd_historical_data.csv")