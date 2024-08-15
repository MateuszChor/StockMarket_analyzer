import numpy as np
import pandas as pd

# Funkcja obliczająca RSI
def rsi(close, length=11):
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Funkcja obliczająca Bollinger Bands
def bollinger_bands(close, length=11, mult=2.0):
    basis = close.rolling(window=length).mean()
    dev = mult * close.rolling(window=length).std()
    upper_band = basis + dev
    lower_band = basis - dev
    return upper_band, lower_band

# Funkcja obliczająca średnie kroczące
def moving_average(close, length):
    return close.rolling(window=length).mean()

# Wczytanie danych wejściowych (np. z pliku CSV)
# Zakładamy, że dane zawierają kolumnę 'Close' z cenami zamknięcia
# close_prices = pd.read_csv('dane.csv')['Close']
# Można też zbudować dane symulujące scenariusz
close_prices = pd.Series(np.random.rand(1000) * 100)

# Parametry
length_rsi = 11
mult_bb = 2.0
length_ma_1 = 9
length_ma_2 = 60

# Obliczenia
rsi_values = rsi(close_prices, length_rsi)
upper_band, lower_band = bollinger_bands(close_prices, length_rsi, mult_bb)
ma_1 = moving_average(close_prices, length_ma_1)
ma_2 = moving_average(close_prices, length_ma_2)

# Sygnały kupna i sprzedaży na podstawie RSI
buy_signal = (rsi_values < 30) & (rsi_values.shift(1) >= 30)
sell_signal = (rsi_values > 80) & (rsi_values.shift(1) <= 80)

# Sygnały kupna i sprzedaży na podstawie crossoverów MA
long_signal = (ma_1 > ma_2) & (ma_1.shift(1) <= ma_2.shift(1))
short_signal = (ma_1 < ma_2) & (ma_1.shift(1) >= ma_2.shift(1))

# Wyświetlanie sygnałów
signals = pd.DataFrame({
    'Close': close_prices,
    'RSI': rsi_values,
    'Upper Band': upper_band,
    'Lower Band': lower_band,
    'MA 1': ma_1,
    'MA 2': ma_2,
    'Buy Signal': buy_signal,
    'Sell Signal': sell_signal,
    'Long Signal': long_signal,
    'Short Signal': short_signal
})

print(signals)