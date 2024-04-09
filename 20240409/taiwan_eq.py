import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# 讀取 CSV 文件並轉換為 DataFrame
df = pd.read_csv('C:\\Users\\User\\Desktop\\cycu_ai2024\\20240409\\地震活動彙整_638482871665559548.csv', encoding='cp950')

print(df)

# 第1行為地震時間、第2行為經度、第3行為緯度、第4行為規模、第5行為深度、第6行為相對位置
df.columns = ['地震時間', '經度', '緯度', '規模', '深度', '相對位置']

# 將第1行的地震時間轉換為 datetime 格式
df['地震時間'] = pd.to_datetime(df['地震時間'])

# 將經度、緯度轉換為 float 格式
df['經度'] = df['經度'].astype(float)
df['緯度'] = df['緯度'].astype(float)

# 利用folium套件繪製地圖
import folium

# 取得台灣地圖中心點
center = [23.5, 121]

# 建立地圖
m = folium.Map(location=center, zoom_start=7)

# 在地圖上加入地震資訊，包含地震時間、經度、緯度、規模、深度、相對位置
for idx, row in df.iterrows():
    popup_text = f"地震時間: {row['地震時間'].strftime('%Y-%m-%d %H:%M:%S')}<br>"
    popup_text += f"經度: {row['經度']}<br>"
    popup_text += f"緯度: {row['緯度']}<br>"
    popup_text += f"規模: {row['規模']}<br>"
    popup_text += f"深度: {row['深度']}<br>"
    popup_text += f"相對位置: {row['相對位置']}<br>"
    folium.Marker([row['緯度'], row['經度']], popup=popup_text).add_to(m)
    
   


# 顯示地圖
m.save('C:\\Users\\User\\Desktop\\cycu_ai2024\\20240409\\taiwan_eq.html')


