import requests
import pandas as pd
import tarfile
import os
import glob
import shutil
import urllib3
from io import StringIO

# 創建一個新的資料夾
os.makedirs("高速公路資訊", exist_ok=True)

# 設定日期範圍
dates = pd.date_range(start="2024-01-01", end="2024-04-30")

# 對每一個日期進行處理
for date in dates:
    date_str = date.strftime("%Y%m%d")  # 將日期轉換為字串格式

    # 下載檔案
    url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_{date_str}.tar.gz"
    response = requests.get(url)
    
    # 若下載失敗，則跳過該日期
    if response.status_code != 200:
        print(f"下載失敗：{date_str}")
        continue

    # 將下載的內容寫入到硬碟
    with open(f"M05A_{date_str}.tar.gz", "wb") as file:
        file.write(response.content)
        # 如果下載的檔案大小為0，則跳過該日期
        if file.tell() == 0:
            print(f"檔案大小為0：{date_str}")
            continue

    # 解壓縮
    with tarfile.open(f"M05A_{date_str}.tar.gz", "r:gz") as tar:
        tar.extractall("test")

    # 刪除原始壓縮檔
    os.remove(f"M05A_{date_str}.tar.gz")

    # 取得所有csv檔案
    files = glob.glob(f"test\\M05A\\{date_str}\\*\\*.csv")

    # 讀取所有csv檔案
    dfs = []
    for file in files:
        df = pd.read_csv(file, usecols=[0, 1, 2, 3, 4, 5], 
                         names=['時間', '上游偵測站編號', '下游偵測站編號', '車種', '車速', '交通量'], 
                         index_col=0, parse_dates=True)
        dfs.append(df)

    # 將dfs中的所有DataFrame合併成一個DataFrame
    df = pd.concat(dfs)

    # 將同一時間、同一里程、同一方向的資料改為同一列，格式為時間、里程、方向、5個車種、5個車種之車速、5個車種之交通量
    df = df.pivot_table(index=['時間', '上游偵測站編號', '下游偵測站編號'], columns='車種', values=['車速', '交通量'], aggfunc='first')
    df.columns = [f'{col[1]}_{col[0]}' for col in df.columns]
    df.reset_index(inplace=True)
    df.columns.name = None

    # 刪除5_車速、32_車速、41_車速、42_車速欄位
    df.drop(columns=['5_車速', '32_車速', '41_車速', '42_車速'], inplace=True)
    # 將31_車速移至下游偵測站編號後面
    df = df[['時間', '上游偵測站編號', '下游偵測站編號', '31_車速', '31_交通量', '32_交通量', '41_交通量', '42_交通量', '5_交通量']]
    # 將31_交通量、32_交通量、41_交通量、42_交通量、5_交通量欄位名稱改為v31、v32、v41、v42、v5
    df.rename(columns={'時間': 'TimeInterval', '上游偵測站編號': 'GantryFrom', '下游偵測站編號': 'GantryTo', '31_車速': 'SpaceMeanSpeed', '31_交通量': 'v31', '32_交通量': 'v32', '41_交通量': 'v41', '42_交通量': 'v42', '5_交通量': 'v5'}, inplace=True)

    # 刪除資料夾
    shutil.rmtree(f"test")

    # 輸出為一個新的 CSV 檔案
    df.to_csv(f"高速公路資訊\\M05A_{date_str}.csv", index=False, encoding='utf-8-sig')
    

# 檢查輸出的檔案名稱是否與日期範圍一致，並列出缺少的日期
output_files = glob.glob("高速公路資訊\\M05A_*.csv")
output_dates = [file.split('_')[1].split('.')[0] for file in output_files]
missing_dates = set(dates.strftime("%Y%m%d")) - set(output_dates)
if len(missing_dates) > 0:
    print("缺少的日期：", missing_dates)
else:
    print("檔案名稱與日期範圍一致")
    exit()  # 結束程式執行


# 將缺少的日期範圍設定為新的日期範圍
dates = pd.date_range(start=min(missing_dates), end=max(missing_dates))

for date in dates:
    date_str = date.strftime("%Y%m%d")  # 將日期轉換為字串格式

    # 儲存所有的 DataFrame
    dfs = []

    # 遍歷每個小時
    for hour in range(24):
        # 遍歷每個五分鐘的時間段
        for minute in range(0, 60, 5):
            # 建立 URL
            url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/{date_str}/{str(hour).zfill(2)}/TDCS_M05A_{date_str}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
            
            # 嘗試下載 CSV 檔案
            try:
                response = requests.get(url, verify=False)
                df = pd.read_csv(StringIO(response.text), usecols=[0, 1, 2, 3, 4, 5], 
                                names=['時間', '上游偵測站編號', '下游偵測站編號', '車種', '車速', '交通量'], 
                                index_col=0, parse_dates=True)
                dfs.append(df)
            except Exception as e:
                print(f"Failed to download {url}: {e}")

    # 將dfs中的所有DataFrame合併成一個DataFrame
    df = pd.concat(dfs)

    # 將同一時間、同一里程、同一方向的資料改為同一列，格式為時間、里程、方向、5個車種、5個車種之車速、5個車種之交通量
    df = df.pivot_table(index=['時間', '上游偵測站編號', '下游偵測站編號'], columns='車種', values=['車速', '交通量'], aggfunc='first')
    df.columns = [f'{col[1]}_{col[0]}' for col in df.columns]
    df.reset_index(inplace=True)
    df.columns.name = None

    # 刪除5_車速、32_車速、41_車速、42_車速欄位
    df.drop(columns=['5_車速', '32_車速', '41_車速', '42_車速'], inplace=True)
    # 將31_車速移至下游偵測站編號後面
    df = df[['時間', '上游偵測站編號', '下游偵測站編號', '31_車速', '31_交通量', '32_交通量', '41_交通量', '42_交通量', '5_交通量']]
    # 將31_交通量、32_交通量、41_交通量、42_交通量、5_交通量欄位名稱改為v31、v32、v41、v42、v5
    df.rename(columns={'時間': 'TimeInterval', '上游偵測站編號': 'GantryFrom', '下游偵測站編號': 'GantryTo', '31_車速': 'SpaceMeanSpeed', '31_交通量': 'v31', '32_交通量': 'v32', '41_交通量': 'v41', '42_交通量': 'v42', '5_交通量': 'v5'}, inplace=True)

    # 輸出為一個新的 CSV 檔案
    df.to_csv(f"高速公路資訊\\M05A_{date_str}.csv", index=False, encoding='utf-8-sig')




