import urllib3
import requests
import pandas as pd
from io import StringIO


# 網頁 URL
base_url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240429"

# 儲存所有的 DataFrame
dfs = []

# 遍歷每個小時
for hour in range(24):
    # 遍歷每個五分鐘的時間段
    for minute in range(0, 60, 5):
        # 建立 URL
        url = f"{base_url}/{str(hour).zfill(2)}/TDCS_M05A_20240429_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
            
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
df.to_csv(f"C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\20240514\\o.csv", encoding='utf-8-sig')

# 讀取 CSV 文件並轉換為 DataFrame
df = pd.read_csv('C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\20240514\\o.csv')

# 保留上游偵測站編號和下游偵測站編號開頭都有01的資料
df = df[df['上游偵測站編號'].str.startswith('01') & df['下游偵測站編號'].str.startswith('01')].copy()
df.reset_index(drop=True, inplace=True)

# 將時間欄位第一個5分鐘定義為1，第二個5分鐘定義為2，以此類推
df['時間'] = pd.to_datetime(df['時間'])
df['時間'] = df['時間'].dt.floor('5T')
df['時間'] = (df['時間'] - df['時間'].iloc[0]).dt.total_seconds() // 300 + 1
df['時間'] = df['時間'].astype(int)

# 將上游偵測站編號和下游偵測站編號前三個字元刪除顯示在新欄位
df['上游偵測站'] = df['上游偵測站編號'].str[3:-1]
df['下游偵測站'] = df['下游偵測站編號'].str[3:-1]
# 將上游偵測站和下游偵測站兩組數字小數點往前移一位，並做平均
df['上游偵測站'] = df['上游偵測站'].astype(float) / 10
df['下游偵測站'] = df['下游偵測站'].astype(float) / 10
df['里程'] = round((df['上游偵測站'] + df['下游偵測站']) / 2, 2)

# 上游偵測站編號若最後一個字為N，定義為0；若為S，定義為1
df['方向'] = df['上游偵測站編號'].str[-1].replace({'N': 0, 'S': 1})

# 刪除上游偵測站編號、下游偵測站編號、上游偵測站、下游偵測站欄位
df.drop(columns=['上游偵測站編號', '下游偵測站編號', '上游偵測站', '下游偵測站'], inplace=True)

# 將同一時間、同一里程、同一方向的資料改為同一列，格式為時間、里程、方向、5個車種、5個車種之車速、5個車種之交通量
df = df.pivot_table(index=['時間', '里程', '方向'], columns='車種', values=['車速', '交通量'], aggfunc='first')
df.columns = [f'{col[1]}_{col[0]}' for col in df.columns]
df.reset_index(inplace=True)
df.columns.name = None

# 在5_交通量欄位前插入5_車種、31_車種、32_車種、41_車種、42_車種，裡面的值分別為5、31、32、41、42
df.insert(3, '5_車種', 5)
df.insert(4, '31_車種', 31)
df.insert(5, '32_車種', 32)
df.insert(6, '41_車種', 41)
df.insert(7, '42_車種', 42)

# 改以時間、方向、里程排序
df.sort_values(by=['時間', '方向', '里程'], inplace=True)
df.reset_index(drop=True, inplace=True)

# 特徵化車速 -100~0，1~20，21~40，41~60，61~80，81~200分別定義為0，1，2，3，4，5
df['5_車速'] = pd.cut(df['5_車速'], bins=[-100, 0, 20, 40, 60, 80, 200], labels=False)
df['31_車速'] = pd.cut(df['31_車速'], bins=[-100, 0, 20, 40, 60, 80, 200], labels=False)
df['32_車速'] = pd.cut(df['32_車速'], bins=[-100, 0, 20, 40, 60, 80, 200], labels=False)
df['41_車速'] = pd.cut(df['41_車速'], bins=[-100, 0, 20, 40, 60, 80, 200], labels=False)
df['42_車速'] = pd.cut(df['42_車速'], bins=[-100, 0, 20, 40, 60, 80, 200], labels=False)

# 輸出為一個新的 CSV 檔案
df.to_csv(f"C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\20240514\\20240429.csv", encoding='utf-8-sig')

# 利用cube spline對時間1的里程和31_交通量做擬合
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame as  df
from pandas import read_csv
from scipy.interpolate import CubicSpline

# 讀取 CSV 文件並轉換為 DataFrame
df = pd.read_csv('C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\20240514\\20240429.csv')

# 對時間為1的里程和交通量做 cubic spline 擬合
mileage = df[(df['時間'] == 1)]['里程'].values
traffic_volume = df[(df['時間'] == 1)]['31_交通量'].values

# 確保里程數據是嚴格遞增的
sort_indices = np.argsort(mileage)
mileage = mileage[sort_indices]
traffic_volume = traffic_volume[sort_indices]

cs = CubicSpline(mileage, traffic_volume)

# 產生新的里程數據
new_mileage = np.linspace(mileage.min(), mileage.max(), 100)
new_traffic_volume = cs(new_mileage)

# 繪製 cubic spline 曲線
plt.plot(new_mileage, new_traffic_volume, label='Cubic Spline')
plt.scatter(mileage, traffic_volume, color='red', label='Data')
plt.xlabel('Mileage')
plt.ylabel('Traffic Volume')
plt.legend()

plt.show()
    





