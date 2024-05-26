import os
import pandas as pd

def merge_csv_files(directory):
    dfs = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(directory, filename))
            df['filename'] = os.path.splitext(filename)[0]
            dfs.append(df)
    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df

directory = "高速公路資訊"
merged_data = merge_csv_files(directory)

print(merged_data)

# 定義最後一欄為時間欄，並將其轉換為時間格式，年月日
merged_data['時間'] = pd.to_datetime(merged_data['時間'], format='%Y-%m-%d %H:%M:%S')

# 利用folium套件繪製地圖
import folium

# 取得地圖中心點