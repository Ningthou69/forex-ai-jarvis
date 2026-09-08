import pandas as pd
import numpy as np
import ta
import requests
from config import OANDA_API_KEY, OANDA_ACCOUNT_ID, FOREX_PAIRS, CANDLE_INTERVAL
from datetime import datetime, timedelta

class TradingAnalyzer:
    """Analyzes forex charts and generates trading signals"""
    
    def __init__(self):
        self.base_url = "https://api-fxpractice.oanda.com"
        self.headers = {
            "Authorization": f"Bearer {OANDA_API_KEY}",
            "Content-Type": "application/json"
        }
    
    def get_candles(self, pair, count=100):
        """Fetch candle data from OANDA"""
        try:
            url = f"{self.base_url}/v3/instruments/{pair}/candles"
            params = {
                "count": count,
                "granularity": CANDLE_INTERVAL,
                "price": "MBA"
            }
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_candles(data)
            else:
                return None
        except Exception as e:
            print(f"Error fetching candles for {pair}: {e}")
            return None
    
    def _parse_candles(self, data):
        """Parse OANDA candle data into DataFrame"""
        candles = data.get("candles", [])
        df_data = []
        
        for candle in candles:
            df_data.append({
                "time": candle["time"],
                "open": float(candle["mid"]["o"]),
                "high": float(candle["mid"]["h"]),
                "low": float(candle["mid"]["l"]),
                "close": float(candle["mid"]["c"]),
                "volume": candle["volume"]
            })
        
        df = pd.DataFrame(df_data)
        df["time"] = pd.to_datetime(df["time"])
        return df
    
    def calculate_indicators(self, df):
        """Calculate technical indicators"""
        if df is None or len(df) < 30:
            return None
        
        indicators = {}
        
        # RSI (Relative Strength Index)
        indicators["rsi"] = ta.momentum.rsi(df["close"], window=14).iloc[-1]
        
        # MACD
        macd = ta.trend.macd(df["close"])
        indicators["macd"] = macd.iloc[-1]
        indicators["macd_signal"] = ta.trend.macd_signal(df["close"]).iloc[-1]
        
        # Moving Averages
        indicators["sma_20"] = ta.trend.sma(df["close"], window=20).iloc[-1]
        indicators["sma_50"] = ta.trend.sma(df["close"], window=50).iloc[-1]
        indicators["ema_12"] = ta.trend.ema(df["close"], window=12).iloc[-1]
        
        # Bollinger Bands
        bb = ta.volatility.bollinger_bands(df["close"], window=20)
        indicators["bb_high"] = bb.iloc[-1, 0]
        indicators["bb_mid"] = bb.iloc[-1, 1]
        indicators["bb_low"] = bb.iloc[-1, 2]
        
        # ATR (Average True Range)
        indicators["atr"] = ta.volatility.average_true_range(
            df["high"], df["low"], df["close"], window=14
        ).iloc[-1]
        
        # Current price
        indicators["current_price"] = df["close"].iloc[-1]
        
        return indicators
    
    def generate_signal(self, pair, indicators):
        """Generate trading signal based on indicators"""
        if not indicators:
            return {"signal": "HOLD", "confidence": 0, "reason": "Insufficient data"}
        
        signals = []
        
        # RSI Signal
        if indicators["rsi"] < 30:
            signals.append(("BUY", 0.8, "RSI Oversold"))
        elif indicators["rsi"] > 70:
            signals.append(("SELL", 0.8, "RSI Overbought"))
        
        # MACD Signal
        if indicators["macd"] > indicators["macd_signal"]:
            signals.append(("BUY", 0.6, "MACD Bullish Crossover"))
        else:
            signals.append(("SELL", 0.6, "MACD Bearish Crossover"))
        
        # Moving Average Signal
        if indicators["sma_20"] > indicators["sma_50"]:
            signals.append(("BUY", 0.7, "SMA 20 above SMA 50"))
        else:
            signals.append(("SELL", 0.7, "SMA 20 below SMA 50"))
        
        # Bollinger Bands Signal
        current_price = indicators["current_price"]
        if current_price < indicators["bb_low"]:
            signals.append(("BUY", 0.5, "Price below Bollinger Band"))
        elif current_price > indicators["bb_high"]:
            signals.append(("SELL", 0.5, "Price above Bollinger Band"))
        
        # Calculate final signal
        final_signal = self._aggregate_signals(signals)
        
        return {
            "pair": pair,
            "signal": final_signal["signal"],
            "confidence": final_signal["confidence"],
            "reasons": final_signal["reasons"],
            "indicators": indicators
        }
    
    def _aggregate_signals(self, signals):
        """Aggregate multiple signals into one decision"""
        if not signals:
            return {"signal": "HOLD", "confidence": 0, "reasons": []}
        
        buy_score = sum(conf for sig, conf, _ in signals if sig == "BUY")
        sell_score = sum(conf for sig, conf, _ in signals if sig == "SELL")
        
        reasons = [reason for _, _, reason in signals]
        
        if buy_score > sell_score:
            return {
                "signal": "BUY",
                "confidence": min(buy_score / 3, 1.0),
                "reasons": reasons
            }
        elif sell_score > buy_score:
            return {
                "signal": "SELL",
                "confidence": min(sell_score / 3, 1.0),
                "reasons": reasons
            }
        else:
            return {"signal": "HOLD", "confidence": 0.5, "reasons": reasons}
    
    def analyze_pair(self, pair):
        """Complete analysis for a forex pair"""
        df = self.get_candles(pair)
        if df is None:
            return {"error": f"Could not fetch data for {pair}"}
        
        indicators = self.calculate_indicators(df)
        signal = self.generate_signal(pair, indicators)
        
        return signal
    
    def analyze_all_pairs(self):
        """Analyze all configured forex pairs"""
        results = {}
        for pair in FOREX_PAIRS:
            results[pair] = self.analyze_pair(pair)
        return results