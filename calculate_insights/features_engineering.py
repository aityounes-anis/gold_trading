import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv("./data/xauusd_historical_data.csv")

# Set 'Date' as the index and convert to datetime
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Ensure data is sorted by date
df.sort_index(inplace=True)

# Calculate daily log returns
df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))

# Calculate rolling mean and standard deviation over 5 days for log returns
window = 5
rolling_mean = df['Log_Return'].rolling(window=window, min_periods=1).mean()
rolling_std = df['Log_Return'].rolling(window=window, min_periods=1).std()

# Calculate daily z-scores
df['Z_Score'] = (df['Log_Return'] - rolling_mean) / rolling_std

# Calculate realized volatility over the week (5 days)
df['Realized_Volatility'] = df['Log_Return'].rolling(window=window, min_periods=1).std() * np.sqrt(window)

# Create a new DataFrame with the features
features_df = df[['Log_Return', 'Z_Score', 'Realized_Volatility']].copy()

# Save the features to a CSV file
features_df.to_csv("./data/features_engineering.csv")