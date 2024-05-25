import requests
import pandas as pd
import tarfile
import os
import glob
import shutil

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

    # 存儲為一個 CSV 檔案
    df.to_csv(f"output.csv", encoding='utf-8-sig')

    # 刪除資料夾
    shutil.rmtree(f"test")

    # 讀取 CSV 文件並轉換為 DataFrame
    df = pd.read_csv('output.csv')

    # 保留上游偵測站編號和下游偵測站編號開頭都有01的資料
    df = df[df['上游偵測站編號'].str.startswith('01') & df['下游偵測站編號'].str.startswith('01')].copy()
    df.reset_index(drop=True, inplace=True)

    # 讀取一個 CSV 檔案，並轉成 DataFrame
    df_ETag = pd.read_csv('result.csv')

    # 若df的上游偵測站編號有在df_ETag的ETag中，則保留該列資料
    df = df[df['上游偵測站編號'].isin(df_ETag['ETag'])].copy()
    df.reset_index(drop=True, inplace=True)
    # 將df_ETag的經緯度資料加入df
    df = pd.merge(df, df_ETag, left_on='上游偵測站編號', right_on='ETag', how='left')

    # 將時間欄位第一個5分鐘定義為1，第二個5分鐘定義為2，以此類推
    df['時間'] = pd.to_datetime(df['時間'])
    df['時間'] = df['時間'].dt.floor('5T')
    df['時間'] = (df['時間'] - df['時間'].iloc[0]).dt.total_seconds() // 300 + 1
    df['時間'] = df['時間'].astype(int)

    # 將上游偵測站編號前三個字元刪除顯示在新欄位
    df['上游偵測站'] = df['上游偵測站編號'].str[3:-1]
    # 將上游偵測站數字小數點往前移一位
    df['上游偵測站'] = df['上游偵測站'].astype(float) / 10
    df['里程'] = df['上游偵測站']

    # 上游偵測站編號若最後一個字為N，定義為0；若為S，定義為1
    df['方向'] = df['上游偵測站編號'].str[-1].replace({'N': 0, 'S': 1})

    # 留下車種為31的資料
    df = df[df['車種'] == 31].copy()
    df.reset_index(drop=True, inplace=True)
    
    # 將欄位重新排序，時間為第一欄，方向為第二欄，里程為第三欄，車速為第四欄，交通量為第五欄，其他欄位刪除
    df = df[['時間', '方向', '里程', '車速', '交通量', '經度', '緯度']].copy()
    
    # 改以時間、方向、里程排序
    df.sort_values(by=['時間', '方向', '里程'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 同一時間、方向下，如果里程相同，則保留車速值最大的資料
    df = df.loc[df.groupby(['時間', '方向', '里程'])['車速'].idxmax()].copy()
    df.reset_index(drop=True, inplace=True)

    # 根據日期判斷星期幾，並將數字寫入第一欄，星期一為1，星期二為2，以此類推
    df.insert(0, '星期', date.weekday() + 1)

    # 輸出為一個新的 CSV 檔案
    df.to_csv(f"{date_str}.csv", encoding='utf-8-sig')
    

# 檢查輸出的檔案名稱是否與日期範圍一致，並列出缺少的日期
output_files = glob.glob("*.csv")
output_dates = [file.split('.')[0] for file in output_files]
missing_dates = set(dates.strftime("%Y%m%d")) - set(output_dates)
if len(missing_dates) > 0:
    print("缺少的日期：", missing_dates)
else:
    print("檔案名稱與日期範圍一致")


import urllib3
from io import StringIO

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

    # 存儲為一個 CSV 檔案
    df.to_csv(f"output.csv", encoding='utf-8-sig')

    # 讀取 CSV 文件並轉換為 DataFrame
    df = pd.read_csv('output.csv')

    # 保留上游偵測站編號和下游偵測站編號開頭都有01的資料
    df = df[df['上游偵測站編號'].str.startswith('01') & df['下游偵測站編號'].str.startswith('01')].copy()
    df.reset_index(drop=True, inplace=True)

    # 讀取一個 CSV 檔案，並轉成 DataFrame
    df_ETag = pd.read_csv('result.csv')

    # 若df的上游偵測站編號有在df_ETag的ETag中，則保留該列資料
    df = df[df['上游偵測站編號'].isin(df_ETag['ETag'])].copy()
    df.reset_index(drop=True, inplace=True)
    # 將df_ETag的經緯度資料加入df
    df = pd.merge(df, df_ETag, left_on='上游偵測站編號', right_on='ETag', how='left')

    # 將時間欄位第一個5分鐘定義為1，第二個5分鐘定義為2，以此類推
    df['時間'] = pd.to_datetime(df['時間'])
    df['時間'] = df['時間'].dt.floor('5T')
    df['時間'] = (df['時間'] - df['時間'].iloc[0]).dt.total_seconds() // 300 + 1
    df['時間'] = df['時間'].astype(int)

    # 將上游偵測站編號前三個字元刪除顯示在新欄位
    df['上游偵測站'] = df['上游偵測站編號'].str[3:-1]
    # 將上游偵測站數字小數點往前移一位
    df['上游偵測站'] = df['上游偵測站'].astype(float) / 10
    df['里程'] = df['上游偵測站']

    # 上游偵測站編號若最後一個字為N，定義為0；若為S，定義為1
    df['方向'] = df['上游偵測站編號'].str[-1].replace({'N': 0, 'S': 1})

    # 留下車種為31的資料
    df = df[df['車種'] == 31].copy()
    df.reset_index(drop=True, inplace=True)
    
    # 將欄位重新排序，時間為第一欄，方向為第二欄，里程為第三欄，車速為第四欄，交通量為第五欄，其他欄位刪除
    df = df[['時間', '方向', '里程', '車速', '交通量', '經度', '緯度']].copy()
    
    # 改以時間、方向、里程排序
    df.sort_values(by=['時間', '方向', '里程'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 同一時間、方向下，如果里程相同，則保留車速值最大的資料
    df = df.loc[df.groupby(['時間', '方向', '里程'])['車速'].idxmax()].copy()
    df.reset_index(drop=True, inplace=True)

    # 根據日期判斷星期幾，並將數字寫入第一欄，星期一為1，星期二為2，以此類推
    df.insert(0, '星期', date.weekday() + 1)

    # 輸出為一個新的 CSV 檔案
    df.to_csv(f"{date_str}.csv", encoding='utf-8-sig')




