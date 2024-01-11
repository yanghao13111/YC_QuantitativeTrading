# indicators.py

# Moving Averages
sma5_h = "self.data.close[0] > self.sma5[0]"
sma10_h = "self.data.close[0] > self.sma10[0]"
sma22_h = "self.data.close[0] > self.sma22[0]"
sma5_l = "self.data.close[0] < self.sma5[0]"
sma10_l = "self.data.close[0] < self.sma10[0]"
sma22_l = "self.data.close[0] < self.sma22[0]"

ema5_h = "self.data.close[0] > self.ema5[0]"
ema10_h = "self.data.close[0] > self.ema10[0]"
ema22_h = "self.data.close[0] > self.ema22[0]"
ema66_h = "self.data.close[0] > self.ema66[0]"
ema5_l = "self.data.close[0] < self.ema5[0]"
ema10_l = "self.data.close[0] < self.ema10[0]"
ema22_l = "self.data.close[0] < self.ema22[0]"
ema66_l = "self.data.close[0] < self.ema66[0]"

ema66_check = "self.data.low[0] > self.ema66[0]"

ema_uptrend_5 = 'self.ema5[0] > self.ema5[-1]'
ema_uptrend_10 = 'self.ema10[0] > self.ema10[-1]'
ema_uptrend_22 = 'self.ema22[0] > self.ema22[-1]'
ema_uptrend_66 = 'self.ema66[0] > self.ema66[-1]'

allup = 'self.ema5[0] > self.ema5[-1] and self.ema10[0] > self.ema10[-1] and self.ema22[0] > self.ema22[-1] and self.ema66[0] > self.ema66[-1]'
no_5ma = 'self.ema10[0] > self.ema10[-1] and self.ema22[0] > self.ema22[-1] and self.ema66[0] > self.ema66[-1]'

ema_downtrend_5 = 'self.ema5[0] < self.ema5[-1]'
ema_downtrend_10 = 'self.ema10[0] < self.ema10[-1]'
ema_downtrend_22 = 'self.ema22[0] < self.ema22[-1]'
ema_downtrend_66 = 'self.ema66[0] < self.ema66[-1]'

# 檢查是否存在均線多頭排列：5日均線 > 10日均線 > 22日均線 > 66日均線
bullish_alignment = 'self.ema5[0] > self.ema10[0] and self.ema10[0] > self.ema22[0] and self.ema22[0] > self.ema66[0]'
# 檢查是否存在均線空頭排列：5日均線 < 10日均線 < 22日均線 < 66日均線
bearish_alignment = 'self.ema5[0] < self.ema10[0] and self.ema10[0] < self.ema22[0] and self.ema22[0] < self.ema66[0]'

is_divergence_less_than_5_percent_5_10 = 'abs((self.ema5[0] - self.ema10[0]) / self.ema10[0]) < 0.05'
is_divergence_less_than_5_percent_10_22 = 'abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) < 0.05'
is_divergence_less_than_5_percent_22_66 = 'abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) < 0.05'

is_divergence_less_than_3_percent_5_10 = 'abs((self.ema5[0] - self.ema10[0]) / self.ema10[0]) < 0.03'
is_divergence_less_than_3_percent_10_22 = 'abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) < 0.03'
is_divergence_less_than_3_percent_22_66 = 'abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) < 0.03'

angle_ema5 = 'angle_ema5 >= 30'
angle_ema10 = 'angle_ema10 >= 30'
angle_ema22 = 'angle_ema22 >= 30'


# 檢查今天的交易量是否至少是昨天交易量的兩倍
volume_indicator = 'self.volume[0] > 2 * self.volume[-1]'

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
BBI_h = "self.data.close[0] > (self.sma5[0]+self.sma10[0]+self.sma22[0]+self.sma66[0])/4"
BBI_l= "self.data.close[0] < (self.sma5[0]+self.sma10[0]+self.sma22[0]+self.sma66[0])/4"
