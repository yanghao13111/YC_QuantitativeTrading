# indicators.py

# Moving Averages
A = "self.data.close[0] > self.sma5[0]"
B = "self.data.close[0] > self.sma10[0]"
C = "self.data.close[0] > self.sma20[0]"
D = "self.data.close[0] < self.sma5[0]"
E = "self.data.close[0] < self.sma10[0]"
F = "self.data.close[0] < self.sma20[0]"


G = "self.data.close[0] > self.ema5[0]"
H = "self.data.close[0] > self.ema10[0]"
I = "self.data.close[0] > self.ema20[0]"
J = "self.data.close[0] < self.ema5[0]"
K = "self.data.close[0] < self.ema10[0]"
L = "self.data.close[0] < self.ema20[0]"

# MACD
M = "self.macd.macd[0] > self.macd.signal[0]"
N = "self.macd.macd[0] < self.macd.signal[0]"

# RSI
O = "self.rsi[0] > 70"
P = "self.rsi[0] < 30"

# Stochastic Oscillator
Q = "self.stoch[0] > 80"
R = "self.stoch[0] < 20"
