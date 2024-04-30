# 讀取 CSV 文件並轉換為 DataFrame
import pandas as pd
df = pd.read_csv('C:\\Users\\User\\Desktop\\cycu_ai2024\\20240430\\1.csv')

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

# 刪除上游偵測站編號、下游偵測站編號、上游偵測站、、旅行時間下游偵測站欄位
df.drop(columns=['上游偵測站編號', '下游偵測站編號', '上游偵測站', '下游偵測站', '旅行時間'], inplace=True)

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

print(df)
# 輸出為一個新的 CSV 檔案
df.to_csv("C:\\Users\\User\\Desktop\\cycu_ai2024\\20240430\\2.csv", encoding='utf-8-sig')