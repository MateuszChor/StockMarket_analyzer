import pandas as pd
import pandas_ta as ta
from pandas_ta import volume
import yfinance, ccxt
import json
from sender import send_telegram_message

from secret import telegram_api, chat_id, bot_token, group_id


exchange_binance = ccxt.binance()
exchange_bybit = ccxt.bybit()

tab = ['ONDO/USDT', 'BTC/USDT', 'ETH/USDT', "GAL/USDT", "IDEX/USDT", "CFX/USDT", "TOKEN/USDT", "ACH/USDT", "OP/USDT",
       "LDO/USDT", "ICP/USDT", "ALGO/USDT"]

# "ETHDYDX/USDT"
pairs_list = [
    "CYBER/USDT", "DAI/USDT", "DCR/USDT", "DECHAT/USDT", "DEFI/USDT", "DEFY/USDT", "DEVT/USDT", "DFI/USDT",
    "DGB/USDT", "DICE/USDT", "DLC/USDT", "DMAIL/USDT", "DOGE/EUR", "DOGE/USDC", "DOGE/USDT", "DOME/USDT",
    "DOT/BTC", "DOT/USDC", "DOT/USDT", "DPX/USDT", "DSRUN/USDT", "DUEL/USDT", "DYM/USDT", "DZOO/USDT",
    "ECOX/USDT", "EGLD/USDT", "EGO/USDT", "ELDA/USDT", "ELT/USDT", "ENJ/USDT", "ENS/USDT", "EOS/USDC",
    "EOS/USDT", "ERTHA/USDT", "ETC/USDT", "ETH/BTC", "ETH/DAI", "ETH/EUR", "ETH/USDC", "ETH/USDT",
    "ETHFI/USDT", "ETHW/USDT", "EVER/USDT", "FAME/USDT", "FAR/USDT", "FB/USDT", "FET/USDT",
    "FIDA/USDT", "FIL/USDC", "FIL/USDT", "FIRE/USDT", "FITFI/USDT", "FLIP/USDT", "FLOKI/USDT", "FLOW/USDT",
    "FLR/USDT", "FMB/USDT", "FMC/USDT", "FON/USDT", "FORT/USDT", "FTM/USDT", "FTT/USDT", "FXS/USDT",
    "GAL/USDT", "GCAKE/USDT", "GENE/USDT", "GG/USDT", "GGM/USDT", "GLMR/USDT", "GM/USDT", "GNS/USDT",
    "GODS/USDT", "GRAPE/USDT", "GRT/USDT", "GALA/USDT", "GST/USDT", "GSWIFT/USDT", "GTAI/USDT", "HBAR/USDT",
    "HERO/USDT", "HFT/USDT", "HNT/USDT", "HON/USDT", "HOOK/USDT", "HOT/USDT", "HTX/USDT", "HVH/USDT",
    "ICP/USDC", "ICP/USDT", "ICX/USDT", "ID/USDT", "IMX/USDT", "INJ/USDT", "INSP/USDT"
]



class ThresholdCrossDetector:
    def __init__(self):
        self.active = False  # Czy warunek aktywacji już był spełniony
        self.state = 'low'  # Aktualny stan: 'low' = a < b, 'high' = a >= b

    def check(self, a, b):
        if self.state == 'low' and a > b:
            self.state = 'high'  # Zmiana stanu na 'high' gdy a przekroczy b
            if not self.active:
                self.active = True  # Aktywacja tylko raz
                return True
        elif a < b:
            self.state = 'low'  # Reset stanu na 'low' gdy a spadnie poniżej b
            self.active = False  # Reset aktywacji
        return False


def rsi_30_70_1h():
    tab = [
        "CYBER/USDT", "DAI/USDT", "DCR/USDT", "DECHAT/USDT", "DEFI/USDT", "DEFY/USDT", "DEVT/USDT", "DFI/USDT",
        "DGB/USDT", "DICE/USDT", "DLC/USDT", "DMAIL/USDT", "DOGE/EUR", "DOGE/USDC", "DOGE/USDT", "DOME/USDT",
        "DOT/BTC", "DOT/USDC", "DOT/USDT", "DPX/USDT", "DSRUN/USDT", "DUEL/USDT", "DYM/USDT", "DZOO/USDT",
        "ECOX/USDT", "EGLD/USDT", "EGO/USDT", "ELDA/USDT", "ELT/USDT", "ENJ/USDT", "ENS/USDT", "EOS/USDC",
        "EOS/USDT", "ERTHA/USDT", "ETC/USDT", "ETH/BTC", "ETH/DAI", "ETH/EUR", "ETH/USDC", "ETH/USDT",
        "ETHFI/USDT", "ETHW/USDT", "EVER/USDT", "FAME/USDT", "FAR/USDT", "FB/USDT", "FET/USDT",
        "FIDA/USDT", "FIL/USDC", "FIL/USDT", "FIRE/USDT", "FITFI/USDT", "FLIP/USDT", "FLOKI/USDT", "FLOW/USDT",
        "FLR/USDT", "FMB/USDT", "FMC/USDT", "FON/USDT", "FORT/USDT", "FTM/USDT", "FTT/USDT", "FXS/USDT",
        "GAL/USDT", "GCAKE/USDT", "GENE/USDT", "GG/USDT", "GGM/USDT", "GLMR/USDT", "GM/USDT", "GNS/USDT",
        "GODS/USDT", "GRAPE/USDT", "GRT/USDT", "GALA/USDT", "GST/USDT", "GSWIFT/USDT", "GTAI/USDT", "HBAR/USDT",
        "HERO/USDT", "HFT/USDT", "HNT/USDT", "HON/USDT", "HOOK/USDT", "HOT/USDT", "HTX/USDT", "HVH/USDT",
        "ICP/USDC", "ICP/USDT", "ICX/USDT", "ID/USDT", "IMX/USDT", "INJ/USDT", "INSP/USDT"
    ]
    layer = 10
    for i in tab:
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
            msg = f"{i} RSI (60m) {rsi.tail(1).iloc[0]} SHORT, entry {df['low'].tail(1).iloc[0]}"
            send_telegram_message(telegram_api, chat_id, msg)


def rsi_30_70_15m():
    tab = [
        "CYBER/USDT", "DAI/USDT", "DCR/USDT", "DECHAT/USDT", "DEFI/USDT", "DEFY/USDT", "DEVT/USDT", "DFI/USDT",
        "DGB/USDT", "DICE/USDT", "DLC/USDT", "DMAIL/USDT", "DOGE/EUR", "DOGE/USDC", "DOGE/USDT", "DOME/USDT",
        "DOT/BTC", "DOT/USDC", "DOT/USDT", "DPX/USDT", "DSRUN/USDT", "DUEL/USDT", "DYM/USDT", "DZOO/USDT",
        "ECOX/USDT", "EGLD/USDT", "EGO/USDT", "ELDA/USDT", "ELT/USDT", "ENJ/USDT", "ENS/USDT", "EOS/USDC",
        "EOS/USDT", "ERTHA/USDT", "ETC/USDT", "ETH/BTC", "ETH/DAI", "ETH/EUR", "ETH/USDC", "ETH/USDT",
        "ETHFI/USDT", "ETHW/USDT", "EVER/USDT", "FAME/USDT", "FAR/USDT", "FB/USDT", "FET/USDT",
        "FIDA/USDT", "FIL/USDC", "FIL/USDT", "FIRE/USDT", "FITFI/USDT", "FLIP/USDT", "FLOKI/USDT", "FLOW/USDT",
        "FLR/USDT", "FMB/USDT", "FMC/USDT", "FON/USDT", "FORT/USDT", "FTM/USDT", "FTT/USDT", "FXS/USDT",
        "GAL/USDT", "GCAKE/USDT", "GENE/USDT", "GG/USDT", "GGM/USDT", "GLMR/USDT", "GM/USDT", "GNS/USDT",
        "GODS/USDT", "GRAPE/USDT", "GRT/USDT", "GALA/USDT", "GST/USDT", "GSWIFT/USDT", "GTAI/USDT", "HBAR/USDT",
        "HERO/USDT", "HFT/USDT", "HNT/USDT", "HON/USDT", "HOOK/USDT", "HOT/USDT", "HTX/USDT", "HVH/USDT",
        "ICP/USDC", "ICP/USDT", "ICX/USDT", "ID/USDT", "IMX/USDT", "INJ/USDT", "INSP/USDT"
    ]
    layer = 10
    for i in tab:
        bars = exchange_bybit.fetch_ohlcv(i, timeframe='15m', limit=3000)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        print(f"________________________ RSI timeframe 15m ________{i}____________________")
        rsi = df.ta.rsi(length=11)
        print(f"Dla {i} RSI -> {rsi.tail(1).iloc[0]}")
        if float(rsi.tail(1).iloc[0]) <= 30:
            print("Zielone 15m")
            msg = f" {i} RSI (15m) LONG entry {df['high'].tail(1).iloc[0]}"
            # msg = f"{i} RSI (15m) {rsi.tail(1).iloc[0]} LONG, entry {df['high'].tail(1).iloc[0]}"
            send_telegram_message(telegram_api, chat_id, msg)

        elif float(rsi.tail(1).iloc[0]) >= 70:
            msg = f" {i} RSI (15m) SHORT entry {df['high'].tail(1).iloc[0]}"
            # send_telegram_message(telegram_api, chat_id, msg)


def macd():
    layer = 10
    for i in tab:
        bars = exchange_binance.fetch_ohlcv(i, timeframe='15m', limit=3000)
        # bars = exchange_bybit.fetch_ohlcv(i, timeframe='15m', limit=1000)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        print(f"________________________ macd ________{i}____________________")
        macd = df.ta.macd()
        print(f"Dla {i} macd -> {macd.tail(1).iloc[0]}")
        macd = macd.tail(1).iloc[0]
        msg = f"" \
              f"{i} ANALIZA macd ---------------------\n" \
              f"{macd} \n " \
              f"--------------------------------------\n"
        print(msg)
        send_telegram_message(telegram_api, chat_id, msg)


def check_sma_ema_15():
    tab = [
        "CYBER/USDT", "DAI/USDT", "DCR/USDT", "DECHAT/USDT", "DEFI/USDT", "DEFY/USDT", "DEVT/USDT", "DFI/USDT",
        "DGB/USDT", "DICE/USDT", "DLC/USDT", "DMAIL/USDT", "DOGE/EUR", "DOGE/USDC", "DOGE/USDT", "DOME/USDT",
        "DOT/BTC", "DOT/USDC", "DOT/USDT", "DPX/USDT", "DSRUN/USDT", "DUEL/USDT", "DYM/USDT", "DZOO/USDT",
        "ECOX/USDT", "EGLD/USDT", "EGO/USDT", "ELDA/USDT", "ELT/USDT", "ENJ/USDT", "ENS/USDT", "EOS/USDC",
        "EOS/USDT", "ERTHA/USDT", "ETC/USDT", "ETH/BTC", "ETH/DAI", "ETH/EUR", "ETH/USDC", "ETH/USDT",
        "ETHFI/USDT", "ETHW/USDT", "EVER/USDT", "FAME/USDT", "FAR/USDT", "FB/USDT", "FET/USDT",
        "FIDA/USDT", "FIL/USDC", "FIL/USDT", "FIRE/USDT", "FITFI/USDT", "FLIP/USDT", "FLOKI/USDT", "FLOW/USDT",
        "FLR/USDT", "FMB/USDT", "FMC/USDT", "FON/USDT", "FORT/USDT", "FTM/USDT", "FTT/USDT", "FXS/USDT",
        "GAL/USDT", "GCAKE/USDT", "GENE/USDT", "GG/USDT", "GGM/USDT", "GLMR/USDT", "GM/USDT", "GNS/USDT",
        "GODS/USDT", "GRAPE/USDT", "GRT/USDT", "GALA/USDT", "GST/USDT", "GSWIFT/USDT", "GTAI/USDT", "HBAR/USDT",
        "HERO/USDT", "HFT/USDT", "HNT/USDT", "HON/USDT", "HOOK/USDT", "HOT/USDT", "HTX/USDT", "HVH/USDT",
        "ICP/USDC", "ICP/USDT", "ICX/USDT", "ID/USDT", "IMX/USDT", "INJ/USDT", "INSP/USDT"
    ]
    for i in tab:
        #bars = exchange_binance.fetch_ohlcv(i, timeframe='15m', limit=3000)
        bars = exchange_bybit.fetch_ohlcv(i, timeframe='15m', limit=3000)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        ema = df.ta.ema(length=9, offset=1)
        print(f"Dla  ema -> {ema.tail(1).iloc[0]}")
        sma = df.ta.sma(length=60, offset=1)
        print(f"Dla sma -> {sma.tail(1).iloc[0]}")
        sma = sma.tail(1).iloc[0]
        ema = ema.tail(1).iloc[0]
        if ema > sma:
            msg = f"{i} EMA SMA CROSSOVER 15m entry {df['high'].tail(1).iloc[0]}"
            send_telegram_message(telegram_api, chat_id, msg)


def check_sma_ema_60():
    tab = [
        "CYBER/USDT", "DAI/USDT", "DCR/USDT", "DECHAT/USDT", "DEFI/USDT", "DEFY/USDT", "DEVT/USDT", "DFI/USDT",
        "DGB/USDT", "DICE/USDT", "DLC/USDT", "DMAIL/USDT", "DOGE/EUR", "DOGE/USDC", "DOGE/USDT", "DOME/USDT",
        "DOT/BTC", "DOT/USDC", "DOT/USDT", "DPX/USDT", "DSRUN/USDT", "DUEL/USDT", "DYM/USDT", "DZOO/USDT",
        "ECOX/USDT", "EGLD/USDT", "EGO/USDT", "ELDA/USDT", "ELT/USDT", "ENJ/USDT", "ENS/USDT", "EOS/USDC",
        "EOS/USDT", "ERTHA/USDT", "ETC/USDT", "ETH/BTC", "ETH/DAI", "ETH/EUR", "ETH/USDC", "ETH/USDT",
        "ETHFI/USDT", "ETHW/USDT", "EVER/USDT", "FAME/USDT", "FAR/USDT", "FB/USDT", "FET/USDT",
        "FIDA/USDT", "FIL/USDC", "FIL/USDT", "FIRE/USDT", "FITFI/USDT", "FLIP/USDT", "FLOKI/USDT", "FLOW/USDT",
        "FLR/USDT", "FMB/USDT", "FMC/USDT", "FON/USDT", "FORT/USDT", "FTM/USDT", "FTT/USDT", "FXS/USDT",
        "GAL/USDT", "GCAKE/USDT", "GENE/USDT", "GG/USDT", "GGM/USDT", "GLMR/USDT", "GM/USDT", "GNS/USDT",
        "GODS/USDT", "GRAPE/USDT", "GRT/USDT", "GALA/USDT", "GST/USDT", "GSWIFT/USDT", "GTAI/USDT", "HBAR/USDT",
        "HERO/USDT", "HFT/USDT", "HNT/USDT", "HON/USDT", "HOOK/USDT", "HOT/USDT", "HTX/USDT", "HVH/USDT",
        "ICP/USDC", "ICP/USDT", "ICX/USDT", "ID/USDT", "IMX/USDT", "INJ/USDT", "INSP/USDT"
    ]
    for i in tab:
        #bars = exchange_binance.fetch_ohlcv(i, timeframe='60m', limit=3000)
        bars = exchange_bybit.fetch_ohlcv(i, timeframe='60m', limit=3000)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        ema = df.ta.ema(length=9, offset=1)
        print(f"Dla  ema -> {ema.tail(1).iloc[0]}")
        sma = df.ta.sma(length=60, offset=1)
        print(f"Dla sma -> {sma.tail(1).iloc[0]}")
        if ema > sma:
            msg = f"{i} EMA SMA CROSSOVER 15m entry {df['high'].tail(1).iloc[0]}"
            send_telegram_message(telegram_api, chat_id, msg)


def adx_raport_15m():
    tab = [
        "CYBER/USDT", "DAI/USDT", "DCR/USDT", "DECHAT/USDT", "DEFI/USDT", "DEFY/USDT", "DEVT/USDT", "DFI/USDT",
        "DGB/USDT", "DICE/USDT", "DLC/USDT", "DMAIL/USDT", "DOGE/EUR", "DOGE/USDC", "DOGE/USDT", "DOME/USDT",
        "DOT/BTC", "DOT/USDC", "DOT/USDT", "DPX/USDT", "DSRUN/USDT", "DUEL/USDT", "DYM/USDT", "DZOO/USDT",
        "ECOX/USDT", "EGLD/USDT", "EGO/USDT", "ELDA/USDT", "ELT/USDT", "ENJ/USDT", "ENS/USDT", "EOS/USDC",
        "EOS/USDT", "ERTHA/USDT", "ETC/USDT", "ETH/BTC", "ETH/DAI", "ETH/EUR", "ETH/USDC", "ETH/USDT",
        "ETHFI/USDT", "ETHW/USDT", "EVER/USDT", "FAME/USDT", "FAR/USDT", "FB/USDT", "FET/USDT",
        "FIDA/USDT", "FIL/USDC", "FIL/USDT", "FIRE/USDT", "FITFI/USDT", "FLIP/USDT", "FLOKI/USDT", "FLOW/USDT",
        "FLR/USDT", "FMB/USDT", "FMC/USDT", "FON/USDT", "FORT/USDT", "FTM/USDT", "FTT/USDT", "FXS/USDT",
        "GAL/USDT", "GCAKE/USDT", "GENE/USDT", "GG/USDT", "GGM/USDT", "GLMR/USDT", "GM/USDT", "GNS/USDT",
        "GODS/USDT", "GRAPE/USDT", "GRT/USDT", "GALA/USDT", "GST/USDT", "GSWIFT/USDT", "GTAI/USDT", "HBAR/USDT",
        "HERO/USDT", "HFT/USDT", "HNT/USDT", "HON/USDT", "HOOK/USDT", "HOT/USDT", "HTX/USDT", "HVH/USDT",
        "ICP/USDC", "ICP/USDT", "ICX/USDT", "ID/USDT", "IMX/USDT", "INJ/USDT", "INSP/USDT"
    ]
    for i in tab:
        bars = exchange_bybit.fetch_ohlcv(i, timeframe='15m', limit=3000)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        adx = df.ta.adx(length=14)  # , lensig= ,mamode=, scalar=, drift=, offset=)
        adx = adx.tail(1).iloc[0]
        print(f"--------------------  {i}  ------------------------------------------")
        dmp = adx['DMP_14']
        dmn = adx['DMN_14']
        if dmp > dmn:
            msg = f"{i}/LONG DMP DMI     15m  {df['high'].tail(1).iloc[0]}"
            print(f" {dmp}  >  {dmn}")
            send_telegram_message(telegram_api, chat_id, msg)
            print(f"________________________ timeframe 15m ________{i}____________________")


def adx_raport_1h():
    tab = [
        "CYBER/USDT", "DAI/USDT", "DCR/USDT", "DECHAT/USDT", "DEFI/USDT", "DEFY/USDT", "DEVT/USDT", "DFI/USDT",
        "DGB/USDT", "DICE/USDT", "DLC/USDT", "DMAIL/USDT", "DOGE/EUR", "DOGE/USDC", "DOGE/USDT", "DOME/USDT",
        "DOT/BTC", "DOT/USDC", "DOT/USDT", "DPX/USDT", "DSRUN/USDT", "DUEL/USDT", "DYM/USDT", "DZOO/USDT",
        "ECOX/USDT", "EGLD/USDT", "EGO/USDT", "ELDA/USDT", "ELT/USDT", "ENJ/USDT", "ENS/USDT", "EOS/USDC",
        "EOS/USDT", "ERTHA/USDT", "ETC/USDT", "ETH/BTC", "ETH/DAI", "ETH/EUR", "ETH/USDC", "ETH/USDT",
        "ETHFI/USDT", "ETHW/USDT", "EVER/USDT", "FAME/USDT", "FAR/USDT", "FB/USDT", "FET/USDT",
        "FIDA/USDT", "FIL/USDC", "FIL/USDT", "FIRE/USDT", "FITFI/USDT", "FLIP/USDT", "FLOKI/USDT", "FLOW/USDT",
        "FLR/USDT", "FMB/USDT", "FMC/USDT", "FON/USDT", "FORT/USDT", "FTM/USDT", "FTT/USDT", "FXS/USDT",
        "GAL/USDT", "GCAKE/USDT", "GENE/USDT", "GG/USDT", "GGM/USDT", "GLMR/USDT", "GM/USDT", "GNS/USDT",
        "GODS/USDT", "GRAPE/USDT", "GRT/USDT", "GALA/USDT", "GST/USDT", "GSWIFT/USDT", "GTAI/USDT", "HBAR/USDT",
        "HERO/USDT", "HFT/USDT", "HNT/USDT", "HON/USDT", "HOOK/USDT", "HOT/USDT", "HTX/USDT", "HVH/USDT",
        "ICP/USDC", "ICP/USDT", "ICX/USDT", "ID/USDT", "IMX/USDT", "INJ/USDT", "INSP/USDT"
    ]
    for i in tab:
        bars = exchange_bybit.fetch_ohlcv(i, timeframe='1h', limit=3000)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        adx = df.ta.adx(length=14)  # , lensig= ,mamode=, scalar=, drift=, offset=)
        adx = adx.tail(1).iloc[0]
        # print(f"--------------------  {i}  ------------------------------------------")
        dmp = adx['DMP_14']
        dmn = adx['DMN_14']
        if dmp > dmn:
            msg = f"{i}/LONG DMP DMI     60m  {df['high'].tail(1).iloc[0]}"
            print(f" {dmp}  >  {dmn}")
            send_telegram_message(telegram_api, chat_id, msg)
            print(f"________________________ timeframe 1h ________{i}____________________")


test_tab = ["DOT/USDT", "DPX/USDT", "DSRUN/USDT"]

check_sma_ema_15()