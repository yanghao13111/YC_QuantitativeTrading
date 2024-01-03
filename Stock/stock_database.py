from FinMind.data import DataLoader
import pandas as pd
import os
from datetime import datetime, timedelta

class StockDatabase:
    # # account: (user_id, password)
    def __init__(self, user_id, password):
        self.data_loader = DataLoader()
        self.data_loader.login(user_id=user_id, password=password)

    # # token
    # def __init__(self, token):
    #     self.data_loader = DataLoader()
    #     self.data_loader.login_by_token(api_token=token)

    def get_stock_price(self, stock_id, start_date, end_date):
        return self.data_loader.taiwan_stock_daily(stock_id, start_date, end_date)

    def fetch_and_save_stock_data(self, stock_list, start_date, end_date, folder_path):
        for stock_id in stock_list:
            try:
                stock_data = self.get_stock_price(stock_id, start_date, end_date)
                stock_data['date'] = pd.to_datetime(stock_data['date'])
                required_columns = ['date', 'open', 'close', 'max', 'min', 'Trading_Volume']
                if all(column in stock_data.columns for column in required_columns):
                    file_name = f"{stock_id}.csv"
                    file_path = os.path.join(folder_path, file_name)
                    stock_data.to_csv(file_path, index=False)
                    print(f"為 {stock_id} 儲存資料於 {file_path}")
                else:
                    print(f"{stock_id} 的資料缺少所需的欄位")
            except Exception as e:
                print(f"提取 {stock_id} 資料時出錯：{e}")

    def update_stock_data(self, stock_list, folder_path):
        for stock_id in stock_list:
            file_path = os.path.join(folder_path, f"{stock_id}.csv")
            try:
                if os.path.exists(file_path):
                    # 讀取現有數據並找到最後一筆數據的日期
                    existing_data = pd.read_csv(file_path)
                    existing_data['date'] = pd.to_datetime(existing_data['date'])
                    last_date = existing_data['date'].max()

                    # 設置更新的起始日期為最後一筆數據日期的次日
                    start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
                else:
                    # 如果文件不存在，從較早的日期開始更新
                    start_date = "2008-01-01"
                
                # 設置結束日期為今天
                end_date = datetime.now().strftime('%Y-%m-%d')

                # 獲取新數據
                new_data = self.get_stock_price(stock_id, start_date, end_date)
                new_data['date'] = pd.to_datetime(new_data['date'])

                # 檢查並儲存最新一筆數據
                if not new_data.empty:
                    latest_data = new_data.iloc[-1:]  # 獲取最新一筆數據
                    if os.path.exists(file_path):
                        latest_data.to_csv(file_path, mode='a', header=False, index=False)
                    else:
                        latest_data.to_csv(file_path, index=False)
                    print(f"為 {stock_id} 追加最新資料至 {file_path}")
                else:
                    print(f"{stock_id} 沒有新的數據可更新")
            except Exception as e:
                print(f"更新 {stock_id} 資料時出錯：{e}")

def read_stock_ids_from_excel(file_path):
    data = pd.read_csv(file_path)
    stock_ids = data['StockID'].tolist()
    return stock_ids

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

if __name__ == "__main__":
    # 讀取股票代號
    excel_path = 'Stock/trainDataSet/taiwan_stock_codes.csv'
    stock_list = read_stock_ids_from_excel(excel_path)

    # 將股票代號分成三等份
    stock_lists = split_list(stock_list, 3)

    # 檢查每一個part的數量
    for i, part in enumerate(stock_lists):
        print(f"第 {i+1} 部分有 {len(part)} 個股票代號。")

    # 檢查每一個part的股票代號
    print(stock_lists[1])
    # for i, part in enumerate(stock_lists):
    #     print(f"第 {i+1} 部分的股票代號：{part}")

    # 為每個部分創建一個 StockDatabase 實例並登錄
    accounts = [
        ('YC_Company', '@qazwsxedc123'),
        ('YC_Company2', '@qazwsxedc123'),
        ('YC_Company3', '@qazwsxedc123')
    ]

    # api_tokens = [
    #     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyNC0wMS0wMiAxNjowNzoxOCIsInVzZXJfaWQiOiJZQ19Db21wYW55IiwiaXAiOiIxMTQuMzMuNy4xMTYifQ.4KDQU_-oQiy5eKDek3-4EyBCA7EEdRwbCjXvkdi9UTM',  # 將這些值替換為您的實際 API 令牌
    #     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyNC0wMS0wMiAxNjowNjozNiIsInVzZXJfaWQiOiJZQ19Db21wYW55MiIsImlwIjoiMTE0LjMzLjcuMTE2In0.5DmMY73riuTlRBCbT2N4v0RmCQLMCJbSfM7cagWMNkU',
    #     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyNC0wMS0wMiAxNTo0NjowNyIsInVzZXJfaWQiOiJZQ19Db21wYW55MyIsImlwIjoiMTE0LjMzLjcuMTE2In0.z-uIQoQbsEp40EcXzCkSapMb2rMB1U743E3OY2ss5Aw'
    # ]

    stock_db = StockDatabase('YC_Company2', '@qazwsxedc123')
    stock_db.fetch_and_save_stock_data([3045, 3046, 3047, 3048, 3049, 3050, 3051, 3052, 3054, 3055, 3056, 3057, 3058, 3059, 3060, 3062, 3064, 3066, 3067, 3071, 3073, 3078, 3081, 3083, 3085, 3086, 3088, 3090, 3092, 3093, 3094, 3095, 3105, 3114, 3115, 3118, 3122, 3128, 3130, 3131, 3138, 3141, 3147, 3149, 3152, 3162, 3163, 3164, 3167, 3169, 3171, 3176, 3178, 3188, 3189, 3191, 3202, 3205, 3206, 3207, 3209, 3211, 3213, 3217, 3218, 3219, 3221, 3224, 3226, 3227, 3228, 3229, 3230, 3231, 3232, 3234, 3236, 3252, 3257, 3259, 3260, 3264, 3265, 3266, 3268, 3272, 3276, 3284, 3285, 3287, 3288, 3289, 3290, 3293, 3294, 3296, 3297, 3303, 3305, 3306, 3308, 3310, 3311, 3312, 3313, 3317, 3321, 3322, 3323, 3324, 3325, 3332, 3338, 3339, 3346, 3349, 3354, 3356, 3357, 3360, 3362, 3363, 3372, 3373, 3374, 3376, 3379, 3380, 3388, 3390, 3402, 3406, 3413, 3416, 3419, 3426, 3430, 3432, 3434, 3437, 3438, 3441, 3444, 3447, 3450, 3454, 3455, 3465, 3466, 3479, 3481, 3483, 3484, 3489, 3490, 3491, 3492, 3494, 3498, 3499, 3501, 3504, 3508, 3511, 3512, 3515, 3516, 3518, 3520, 3521, 3522, 3523, 3526, 3527, 3528, 3530, 3531, 3532, 3533, 3535, 3537, 3540, 3541, 3543, 3545, 3546, 3548, 3550, 3551, 3552, 3555, 3556, 3557, 3558, 3563, 3564, 3567, 3570, 3576, 3577, 3580, 3581, 3583, 3587, 3588, 3591, 3592, 3593, 3594, 3596, 3597, 3605, 3607, 3609, 3611, 3615, 3617, 3622, 3623, 3624, 3625, 3628, 3629, 3630, 3631, 3632, 3645, 3646, 3652, 3653, 3663, 3664, 3665, 3666, 3669, 3672, 3673, 3675, 3679, 3680, 3684, 3685, 3686, 3687, 3689, 3691, 3693, 3694, 3701, 3702, 3703, 3704, 3705, 3706, 3707, 3708, 3709, 3710, 3711, 3712, 3713, 3714, 3715, 4102, 4104, 4105, 4106, 4107, 4108, 4109, 4111, 4113, 4114, 4116, 4119, 4120, 4121, 4123, 4126, 4127, 4128, 4129, 4130, 4131, 4133, 4137, 4138, 4139, 4142, 4147, 4148, 4153, 4154, 4155, 4157, 4160, 4161, 4162, 4163, 4164, 4167, 4168, 4171, 4173, 4174, 4175, 4183, 4188, 4190, 4192, 4198, 4205, 4207, 4303, 4304, 4305, 4306, 4401, 4402, 4406, 4413, 4414, 4416, 4417, 4419, 4420, 4426, 4430, 4432, 4433, 4438, 4439, 4440, 4442, 4502, 4503, 4506, 4510, 4513, 4523, 4526, 4527, 4528, 4529, 4530, 4532, 4533, 4534, 4535, 4536, 4538, 4540, 4541, 4542, 4543, 4545, 4549, 4550, 4551, 4552, 4554, 4555, 4556, 4557, 4558, 4560, 4561, 4562, 4563, 4564, 4566, 4568, 4569, 4571, 4572, 4576, 4577, 4580, 4581, 4583, 4584, 4609, 4702, 4706, 4707, 4711, 4712, 4714, 4716, 4720, 4721, 4722, 4726, 4728, 4729, 4735, 4736, 4737, 4739, 4741, 4743, 4744, 4745, 4746, 4747, 4754, 4755, 4760, 4763, 4764, 4766, 4767, 4768, 4770, 4804, 4806, 4807, 4903, 4904, 4905, 4906, 4907, 4908, 4909, 4911, 4912, 4915, 4916, 4919, 4923, 4924, 4927, 4930, 4931, 4933, 4934, 4935, 4938, 4939, 4942, 4943, 4945, 4946, 4951, 4952, 4953, 4956, 4958, 4960, 4961, 4966, 4967, 4968, 4971, 4972, 4973, 4974, 4976, 4977, 4979, 4987, 4989, 4991, 4994, 4995, 4999, 5007, 5009, 5011, 5013, 5014, 5015, 5016, 5201, 5202, 5203, 5205, 5206, 5209, 5210, 5211, 5212, 5213, 5215, 5220, 5222, 5223, 5225, 5227, 5228, 5230, 5234, 5236, 5243, 5244, 5245, 5251, 5258, 5263, 5272, 5276, 5278, 5283, 5284, 5285, 5287, 5288, 5289, 5291, 5292, 5299, 5301, 5302, 5306, 5309, 5310, 5312, 5314, 5315, 5321, 5324, 5328, 5340, 5344, 5345, 5347, 5348, 5351, 5353, 5355, 5356, 5364, 5371, 5381, 5383, 5386, 5388, 5392, 5398, 5403, 5410, 5425, 5426, 5432, 5434, 5438, 5439, 5443, 5450, 5452, 5455, 5457, 5460, 5464, 5465, 5468, 5469, 5471, 5474, 5475, 5478, 5481, 5483, 5484, 5487, 5488, 5489, 5490, 5493, 5498, 5508, 5511, 5512, 5514, 5515, 5516, 5519, 5520, 5521, 5522, 5523, 5525, 5529, 5530, 5531, 5533, 5534, 5536, 5538, 5543, 5546], "2008-01-01", "2024-01-02", "Stock/trainDataSet")

    # 分批抓取資料
    # for i, part in enumerate(stock_lists):
    #     if i == 0 or i == 2:
    #         continue
    #     user_id, password = accounts[i]
    #     stock_db = StockDatabase(user_id, password)
    #     stock_db.fetch_and_save_stock_data(part, "2008-01-01", "2024-01-02", "Stock/trainDataSet")
    #     # stock_db.update_stock_data(part, "Stock/trainDataSet")
    #     print(f"已完成第 {i+1} 批的資料抓取。")
