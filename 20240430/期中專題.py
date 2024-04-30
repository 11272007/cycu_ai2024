import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import pandas as pd
from io import StringIO

# 網頁 URL
base_url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/202404"

# 儲存所有的 DataFrame
dfs = []

# 遍歷每個日期
for day in range(29, 30):
    # 遍歷每個小時
    for hour in range(24):
        # 遍歷每個五分鐘的時間段
        for minute in range(0, 60, 5):
            # 建立 URL
            url = f"{base_url}{str(day).zfill(2)}/{str(hour).zfill(2)}/TDCS_M05A_202404{str(day).zfill(2)}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
            
            # 嘗試下載 CSV 檔案
            try:
                response = requests.get(url, verify=False)
                df = pd.read_csv(StringIO(response.text), usecols=[0, 1, 2, 3, 4, 5], 
                                 names=['時間', '上游偵測站編號', '下游偵測站編號', '車種', '車速', '交通量'], 
                                 index_col=0, parse_dates=True)
                dfs.append(df)
            except Exception as e:
                print(f"Failed to download {url}: {e}")

# 另一個網頁 URL
base_url2 = "https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/202404"

# 儲存所有的 DataFrame
dfs2 = []

# 遍歷每個日期
for day in range(29, 30):
    # 遍歷每個小時
    for hour in range(24):
        # 遍歷每個五分鐘的時間段
        for minute in range(0, 60, 5):
            # 建立 URL
            url = f"{base_url2}{str(day).zfill(2)}/{str(hour).zfill(2)}/TDCS_M04A_202404{str(day).zfill(2)}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
            
            # 嘗試下載 CSV 檔案
            try:
                response = requests.get(url, verify=False)
                df = pd.read_csv(StringIO(response.text), usecols=[0, 1, 2, 3, 4, 5], 
                                 names=['時間', '上游偵測站編號', '下游偵測站編號', '車種', '旅行時間', '交通量'], 
                                 index_col=0, parse_dates=True)
                dfs2.append(df)
            except Exception as e:
                print(f"Failed to download {url}: {e}")


# 將dfs2的旅行時間資料插入dfs的第5欄與第6欄間
for i in range(len(dfs)):
    dfs[i].insert(4, '旅行時間', dfs2[i]['旅行時間'])

# 將dfs中的所有DataFrame合併成一個DataFrame
df_final = pd.concat(dfs)

# 輸出為一個新的 CSV 檔案
df_final.to_csv("C:\\Users\\User\\Desktop\\cycu_ai2024\\20240430\\1.csv")