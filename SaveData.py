import yfinance as yf
import pandas as pd

def download_data(symbol, interval, period, file_name):
    
    data = yf.download(symbol, interval=interval, period=period)
    data = data.dropna()
    data = data.reset_index()
    data.columns = ['Datetime', "Open", 'High', 'Low', 'Close', 'Adj Close', "Volume"]
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    data = data[~data.isin(['BTC-USD']).any(axis=1)]
    data = data.sort_values('Datetime')
    data.set_index('Datetime', inplace=True)
    
    data.to_csv(file_name)
    
    
    print(f"Data saved to {file_name}")
    print(data.head())
    
    return data

data = download_data('BTC-USD', interval='1m', period='max', file_name='btc_usd_data.csv')