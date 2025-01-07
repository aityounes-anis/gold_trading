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

# Calculate realized volatility over 5 days
window_realized = 5
df['Realized_Volatility'] = df['Log_Return'].rolling(window=window_realized, min_periods=1).std() * np.sqrt(window_realized)

# Determine volatility regimes
window_quartile = 22
rolling_vol = df['Realized_Volatility'].rolling(window=window_quartile, min_periods=1)
q1 = rolling_vol.quantile(0.25)
q3 = rolling_vol.quantile(0.75)

df['vol_regime'] = 0  # Default to medium volatility
df.loc[df['Realized_Volatility'] >= q3, 'vol_regime'] = 1  # High volatility
df.loc[df['Realized_Volatility'] <= q1, 'vol_regime'] = -1  # Low volatility

# Calculate range expansion/compression
df['Daily_Range'] = df['High'] - df['Low']

window_range = 5
df['Rolling_Range_Mean'] = df['Daily_Range'].rolling(window=window_range, min_periods=1).mean()

df['Normalized_Range'] = df['Daily_Range'] / df['Rolling_Range_Mean']

df['Range_Regime'] = 0
df.loc[df['Normalized_Range'] > 1.5, 'Range_Regime'] = 1  # High range (expansion)
df.loc[df['Normalized_Range'] < 0.75, 'Range_Regime'] = -1  # Low range (compression)

# Calculate daily z-scores for log returns
rolling_mean = df['Log_Return'].rolling(window=window_realized, min_periods=1).mean()
rolling_std = df['Log_Return'].rolling(window=window_realized, min_periods=1).std()
df['Z_Score'] = (df['Log_Return'] - rolling_mean) / rolling_std

# Handle NaN values if necessary
df.ffill(inplace=True)

# Debugging: Check columns
print(df.columns)

# Print Z_Score to verify calculation
print(df['Z_Score'].head())

# Create a DataFrame with the desired features
features_df = df[['Log_Return', 'Z_Score', 'Realized_Volatility', 'vol_regime', 'Normalized_Range', 'Range_Regime']].copy()

# Save the features to a CSV file
features_df.to_csv("./data/features_engineering.csv")

print("Features engineering completed and saved to features_engineering.csv")