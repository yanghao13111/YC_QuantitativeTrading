# indicators.py

# Moving Averages
sma5_h = "self.data.close[0] > self.sma5[0]"
sma10_h = "self.data.close[0] > self.sma10[0]"
sma20_h = "self.data.close[0] > self.sma20[0]"
sma5_l = "self.data.close[0] < self.sma5[0]"
sma10_l = "self.data.close[0] < self.sma10[0]"
sma20_l = "self.data.close[0] < self.sma20[0]"

ema5_h = "self.data.close[0] > self.ema5[0]"
ema10_h = "self.data.close[0] > self.ema10[0]"
ema20_h = "self.data.close[0] > self.ema20[0]"
ema5_l = "self.data.close[0] < self.ema5[0]"
ema10_l = "self.data.close[0] < self.ema10[0]"
ema20_l = "self.data.close[0] < self.ema20[0]"
ema60_l = "self.data.close[0] < self.ema60[0]"

ema_uptrend_5_10 = 'self.ema5[0] > self.ema10[0]'
ema_uptrend_5_20 = 'self.ema5[0] > self.ema20[0]'
ema_uptrend_10_20 = 'self.ema10[0] > self.ema20[0]'

ema_downtrend_5_10 = 'self.ema5[0] < self.ema10[0]'
ema_downtrend_5_20 = 'self.ema5[0] < self.ema20[0]'
ema_downtrend_10_20 = 'self.ema10[0] < self.ema20[0]'

# MACD
macd_g = "self.macd.macd[0] > self.macd.signal[0]" # 快線上穿慢線，買進
macd_d = "self.macd.macd[0] < self.macd.signal[0]" # 快線下穿慢線，賣出

# KDJ
kdj_b = "self.k[0] > self.j[0] and self.d[0] > self.j[0]" # K線、D線上穿j線，買進
kdj_s = "self.k[0] < self.j[0] and self.d[0] < self.j[0]" # K線、D線下穿j線，賣出
kd_g = "self.k[0] > self.d[0] and self.k[0] < 20 and self.d < 20" # 金叉，買進
kd_d = "self.k[0] < self.d[0] and self.k[0] > 80 and self.d > 80" # 死叉，賣出


# RSI
rsi_b = "self.rsi[0] < 30"  # 超賣，買進
rsi_s = "self.rsi[0] > 70"  # 超買，賣出

# DMI (ADX)
dmi_pdi = "self.dmi.plusDI[0] > self.dmi.minusDI[0] and self.dmi.adx[0] > 20" # 多頭，買進
dmi_mdi = "self.dmi.plusDI[0] < self.dmi.minusDI[0] and self.dmi.adx[0] > 20" # 空頭，賣出

# BBI
BBI_h = "self.data.close[0] > (self.sma5[0]+self.sma10[0]+self.sma20[0]+self.sma60[0])/4"
BBI_l= "self.data.close[0] < (self.sma5[0]+self.sma10[0]+self.sma20[0]+self.sma60[0])/4"
