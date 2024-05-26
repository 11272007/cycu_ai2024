import pandas as pd
import os

# 設定一個日期範圍
dates = pd.date_range(start='2024-01-01', end='2024-01-01', freq='D')

# 設定特定資料夾路徑
folder_path = '高速公路資訊'

# 讀取資料夾中的檔案
for date in dates:
    filename = f"M05A_{date.strftime('%Y%m%d')}.csv"
    file_path = os.path.join(folder_path, filename)
    
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
    else:
        print(f"File {filename} does not exist.")

    # 添加
