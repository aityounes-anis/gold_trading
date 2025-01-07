import yfinance as yf
import pandas as pd

# Define the ticker symbol for XAUUSD
ticker_symbol = "GC=F"

# Define the File path
file_path = "./data/xauusd_historical_data.csv"

# Define the date range
start_date = "2015-01-01"
end_date = "2025-01-07"

# Download the historical data
data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Exclude the 'Volume' column
data = data.drop(columns=['Volume'])


data = pd.read_csv(file_path, skiprows=3)

data.columns = ["Date", "Close", "High", "Low", "Open"]

# Set the 'Date' column as the index
data.set_index("Date", inplace=True)

# Convert the index to a datetime format
data.index = pd.to_datetime(data.index)

# Save the cleaned data to a new CSV file (optional)
data.to_csv(file_path)

# Save the data to a CSV file (optional)
data.to_csv(file_path)