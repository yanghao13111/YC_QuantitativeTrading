# indicators.py

# Moving Averages
ema5_h = "self.data.close[-1] > self.ema5[-1]"
ema10_h = "self.data.close[-1] > self.ema10[-1]"
ema22_h = "self.data.close[-1] > self.ema22[-1]"
ema66_h = "self.data.close[-1] > self.ema66[-1]"
ema5_l = "self.data.close[-1] < self.ema5[-1]"
ema10_l = "self.data.close[-1] < self.ema10[-1]"
ema22_l = "self.data.close[-1] < self.ema22[-1]"
ema66_l = "self.data.close[-1] < self.ema66[-1]"

ema66_check = "self.data.low[-1] > self.ema66[-1]"

ema_uptrend_5 = 'self.ema5[-1] > self.ema5[-2]'
ema_uptrend_10 = 'self.ema10[-1] > self.ema10[-2]'
ema_uptrend_22 = 'self.ema22[-1] > self.ema22[-2]'
ema_uptrend_66 = 'self.ema66[-1] > self.ema66[-2]'
ema_uptrend_264 = 'self.ema264[-1] > self.ema264[-2]'

ema_downtrend_5 = 'self.ema5[-1] < self.ema5[-2]'
ema_downtrend_10 = 'self.ema10[-1] < self.ema10[-2]'
ema_downtrend_22 = 'self.ema22[-1] < self.ema22[-2]'
ema_downtrend_66 = 'self.ema66[-1] < self.ema66[-2]'
ema_downtrend_264 = 'self.ema264[-1] < self.ema264[-2]'

# ------------- need to be rectified ----------------

all_uptrend = 'self.ema5[0] > self.ema5[-1] and self.ema10[0] > self.ema10[-1] and self.ema22[0] > self.ema22[-1] and self.ema66[0] > self.ema66[-1]'
all_downtrend = 'self.ema5[0] < self.ema5[-1] and self.ema10[0] < self.ema10[-1] and self.ema22[0] < self.ema22[-1]'
no_5ma = 'self.ema10[0] > self.ema10[-1] and self.ema22[0] > self.ema22[-1] and self.ema66[0] > self.ema66[-1]'

ema_downtrend_5 = 'self.ema5[0] < self.ema5[-1]'
ema_downtrend_10 = 'self.ema10[0] < self.ema10[-1]'
ema_downtrend_22 = 'self.ema22[0] < self.ema22[-1]'
ema_downtrend_66 = 'self.ema66[0] < self.ema66[-1]'

# 檢查是否存在均線多頭排列：5日均線 > 10日均線 > 22日均線 > 66日均線
bullish_alignment = 'self.ema5[0] > self.ema10[0] and self.ema10[0] > self.ema22[0] and self.ema22[0] > self.ema66[0]'
# 檢查是否存在均線空頭排列：5日均線 < 10日均線 < 22日均線 < 66日均線
bearish_alignment = 'self.ema5[0] < self.ema10[0] and self.ema10[0] < self.ema22[0] and self.ema22[0] < self.ema66[0]'

divergence2_5_10l = 'abs((self.ema5[0] - self.ema10[0]) / self.ema10[0]) < 0.02'
divergence2_10_22l = 'abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) < 0.02'
divergence2_22_66l = 'abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) < 0.02'
# divergence2_22_264l = 'abs((self.ema22[0] - self.ema264[0]) / self.ema264[0]) < 0.02'

divergence5_5_10l = 'abs((self.ema5[0] - self.ema10[0]) / self.ema10[0]) < 0.05'
divergence5_10_22l = 'abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) < 0.05'
divergence5_22_66l = 'abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) < 0.05'
# divergence5_22_264l = 'abs((self.ema22[0] - self.ema264[0]) / self.ema264[0]) < 0.05'

divergence10_5_10l = 'abs((self.ema5[0] - self.ema10[0]) / self.ema10[0]) < 0.1'
divergence10_10_22l = 'abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) < 0.1'
divergence10_22_66l = 'abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) < 0.1'
# divergence10_22_264l = 'abs((self.ema22[0] - self.ema264[0]) / self.ema264[0]) < 0.1'

divergence2_5_10h = 'abs((self.ema5[0] - self.ema10[0]) / self.ema10[0]) > 0.02'
divergence2_10_22h = 'abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) > 0.02'
divergence2_22_66h = 'abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) > 0.02'
# divergence2_22_264h = 'abs((self.ema22[0] - self.ema264[0]) / self.ema264[0]) > 0.02'

divergence5_5_10h = 'abs((self.ema5[0] - self.ema10[0]) / self.ema10[0]) > 0.05'
divergence5_10_22h = 'abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) > 0.05'
divergence5_22_66h = 'abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) > 0.05'
# divergence5_22_264h = 'abs((self.ema22[0] - self.ema264[0]) / self.ema264[0]) > 0.05'

divergence10_5_10h = 'abs((self.ema5[0] - self.ema10[0]) / self.ema10[0]) > 0.1'
divergence10_10_22h = 'abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) > 0.1'
divergence10_22_66h = 'abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) > 0.1'
# divergence10_22_264h = 'abs((self.ema22[0] - self.ema264[0]) / self.ema264[0]) > 0.1'

angle20_ema5h = 'math.atan((self.ema5[0] - self.ema5[-1])) * (180 / math.pi) > 20'  
angle20_ema10h = 'math.atan((self.ema10[0] - self.ema10[-1])) * (180 / math.pi) > 20'
angle20_ema22h = 'math.atan((self.ema22[0] - self.ema22[-1])) * (180 / math.pi) > 20' 
angle20_ema66h = 'math.atan((self.ema66[0] - self.ema66[-1])) * (180 / math.pi) > 20'

angle30_ema5h = 'math.atan((self.ema5[0] - self.ema5[-1])) * (180 / math.pi) > 30'  
angle30_ema10h = 'math.atan((self.ema10[0] - self.ema10[-1])) * (180 / math.pi) > 30'
angle30_ema22h = 'math.atan((self.ema22[0] - self.ema22[-1])) * (180 / math.pi) > 30' 
angle30_ema66h = 'math.atan((self.ema66[0] - self.ema66[-1])) * (180 / math.pi) > 30'

angle50_ema5h = 'math.atan((self.ema5[0] - self.ema5[-1])) * (180 / math.pi) > 50'  
angle50_ema10h = 'math.atan((self.ema10[0] - self.ema10[-1])) * (180 / math.pi) > 50'
angle50_ema22h = 'math.atan((self.ema22[0] - self.ema22[-1])) * (180 / math.pi) > 50' 
angle50_ema66h = 'math.atan((self.ema66[0] - self.ema66[-1])) * (180 / math.pi) > 50'

angle20_ema5l = 'math.atan((self.ema5[0] - self.ema5[-1])) * (180 / math.pi) < 20'  
angle20_ema10l = 'math.atan((self.ema10[0] - self.ema10[-1])) * (180 / math.pi) < 20'
angle20_ema22l = 'math.atan((self.ema22[0] - self.ema22[-1])) * (180 / math.pi) < 20' 
angle20_ema66l = 'math.atan((self.ema66[0] - self.ema66[-1])) * (180 / math.pi) < 20'

angle30_ema5l = 'math.atan((self.ema5[0] - self.ema5[-1])) * (180 / math.pi) < 30'  
angle30_ema10l = 'math.atan((self.ema10[0] - self.ema10[-1])) * (180 / math.pi) < 30'
angle30_ema22l = 'math.atan((self.ema22[0] - self.ema22[-1])) * (180 / math.pi) < 30' 
angle30_ema66l = 'math.atan((self.ema66[0] - self.ema66[-1])) * (180 / math.pi) < 30'

angle50_ema5l = 'math.atan((self.ema5[0] - self.ema5[-1])) * (180 / math.pi) < 50'  
angle50_ema10l = 'math.atan((self.ema10[0] - self.ema10[-1])) * (180 / math.pi) < 50'
angle50_ema22l = 'math.atan((self.ema22[0] - self.ema22[-1])) * (180 / math.pi) < 50' 
angle50_ema66l = 'math.atan((self.ema66[0] - self.ema66[-1])) * (180 / math.pi) < 50'

# 判断均线斜率变化是否为负
slope_10 = 'self.ema10[0] - self.ema10[-1] < self.ema10[-1] - self.ema10[-2]'
slope_22 = 'self.ema22[0] - self.ema22[-1] < self.ema22[-1] - self.ema22[-2]'

# 檢查今天的交易量是否至少是昨天交易量的兩倍
double_volume = 'self.data.volume[0] > 2 * self.data.volume[-1]'
volume_5 = 'self.data.volume > self.ema_volume_5'
volume_over_1000 = 'self.data.volume[0] > 1000 * 1000'
volume_over_500 = 'self.data.volume[0] > 1000 * 500'
volume_over_300 = 'self.data.volume[0] > 1000 * 300'

volume_less_500 = 'self.data.volume[0] < 1000 * 500'

red_bar = 'self.data.close[0] > self.data.open[0]'
upper_wick_length = '(self.data.high[0] - self.data.close[0] > self.data.close[0] - self.data.open[0] and self.data.high[0] - self.data.close[0] > self.data.close[0] * 0.05)'

green_bar = 'self.data.open[0] > self.data.close[0]'
green_down = 'self.data.close[0] < self.data.close[-1]'
green_super_down = 'self.data.close[0] < self.data.open[-1]'
green_eat_red = 'self.data.close[0] < self.entry_open_price'

# # MACD
# macd_g = "self.macself.macd[0] > self.macself.signal[0]" # 快線上穿慢線，買進
# macd_d = "self.macself.macd[0] < self.macself.signal[0]" # 快線下穿慢線，賣出

# # KDJ
# kdj_b = "self.k[0] > self.j[0] and self.d[0] > self.j[0]" # K線、D線上穿j線，買進
# kdj_s = "self.k[0] < self.j[0] and self.d[0] < self.j[0]" # K線、D線下穿j線，賣出
# kd_g = "self.k[0] > self.d[0] and self.k[0] < 20 and self.d < 20" # 金叉，買進
# kd_d = "self.k[0] < self.d[0] and self.k[0] > 80 and self.d > 80" # 死叉，賣出

# # RSI
# rsi_b = "self.rsi[0] < 30"  # 超賣，買進
# rsi_s = "self.rsi[0] > 70"  # 超買，賣出
# rsi = 'self.rsi[0] < 70 and self.rsi[0] > 50'

# # DMI (ADX)
# dmi_pdi = "self.dmi.plusDI[0] > self.dmi.minusDI[0] and self.dmi.adx[0] > 20" # 多頭，買進
# dmi_mdi = "self.dmi.plusDI[0] < self.dmi.minusDI[0] and self.dmi.adx[0] > 20" # 空頭，賣出

# # BBI
# BBI_h = "self.data.close[0] > (self.sma5[0]+self.sma10[0]+self.sma22[0]+self.sma66[0])/4"
# BBI_l= "self.data.close[0] < (self.sma5[0]+self.sma10[0]+self.sma22[0]+self.sma66[0])/4"
