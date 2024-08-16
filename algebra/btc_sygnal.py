import pandas as pd
import pandas_ta as ta
import yfinance, ccxt
import json
import time
from sender import send_telegram_message

from secret import telegram_api, chat_id, bot_token, group_id

exchange_bybit = ccxt.bybit()

# Zakładam, że i to nazwa instrumentu lub numer iteracji. Można to dostosować.
i = 'BTC/USDT'

while True:
    try:
        bars = exchange_bybit.fetch_ohlcv(i, timeframe='1h', limit=3000)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        print(f"________________________ RSI timeframe 60m ________{i}____________________")
        rsi = df.ta.rsi(length=11)
        print(f"Dla {i} RSI -> {rsi.tail(1).iloc[0]}")

        if float(rsi.tail(1).iloc[0]) <= 30:
            print("Zielone 60m")
            msg = f"{i} RSI (60m) {rsi.tail(1).iloc[0]} LONG, entry {df['high'].tail(1).iloc[0]}"
            send_telegram_message(telegram_api, chat_id, msg)

        elif float(rsi.tail(1).iloc[0]) >= 70:
            print("Czerwone 60m")
            msg = f"{i} RSI (60m) {rsi.tail(1).iloc[0]} SHORT, entry {df['low'].tail(1).iloc[0]}"
            send_telegram_message(telegram_api, chat_id, msg)

        bars = exchange_bybit.fetch_ohlcv(i, timeframe='1m', limit=3000)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        print(f"________________________ RSI timeframe 1m ________{i}____________________")
        rsi = df.ta.rsi(length=11)
        print(f"Dla {i} RSI -> {rsi.tail(1).iloc[0]}")

        if float(rsi.tail(1).iloc[0]) <= 30:
            print("Zielone 1m")
            msg = f"{i} RSI (1m) {rsi.tail(1).iloc[0]} LONG, entry {df['high'].tail(1).iloc[0]}"
            send_telegram_message(telegram_api, chat_id, msg)

        elif float(rsi.tail(1).iloc[0]) >= 70:
            print("Czerwone 1m")
            msg = f"{i} RSI (1m) {rsi.tail(1).iloc[0]} SHORT, entry {df['low'].tail(1).iloc[0]}"
            send_telegram_message(telegram_api, chat_id, msg)

        # Opóźnienie przed kolejnym cyklem pętli (np. 1 minuta)

        time.sleep(60)

    except Exception as e:
        # Logowanie błędów do pliku tekstowego
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"Błąd: {str(e)}\n")
        time.sleep(60)