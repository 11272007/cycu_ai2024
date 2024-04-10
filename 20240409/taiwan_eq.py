import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# 讀取 CSV 文件並轉換為 DataFrame
df = pd.read_csv('C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\20240409\\地震活動彙整_638482871665559548.csv', encoding='cp950')

# 第1行為地震時間、第2行為經度、第3行為緯度、第4行為規模、第5行為深度、第6行為相對位置
df.columns = ['地震時間', '經度', '緯度', '規模', '深度', '相對位置']

# 將第1行的地震時間轉換為 datetime 格式
df['地震時間'] = pd.to_datetime(df['地震時間'])

# 將經度、緯度轉換為 float 格式
df['經度'] = df['經度'].astype(float)
df['緯度'] = df['緯度'].astype(float)

# 利用folium套件繪製地圖
import folium
from folium.plugins import TimestampedGeoJson

# 取得台灣地圖中心點
center = [23.5, 121]

# 建立地圖
m = folium.Map(location=center, zoom_start=7)

# 在地圖上加入地震資訊，包含地震時間、經度、緯度、規模、深度、相對位置
# 並且將各項資訊換行顯示
# 將地震資訊轉換為 GeoJson 格式
features = []
for i in range(len(df)):
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [df['經度'][i], df['緯度'][i]]
        },
        'properties': {
            'time': str(df['地震時間'][i]),
            'popup': f"""<div style='width: 200px;'>
                            <b>地震時間:</b> {df['地震時間'][i]}<br>
                            <b>經度:</b> {df['經度'][i]}<br>
                            <b>緯度:</b> {df['緯度'][i]}<br>
                            <b>規模:</b> {df['規模'][i]}<br>
                            <b>深度:</b> {df['深度'][i]}<br>
                            <b>相對位置:</b> {df['相對位置'][i]}
                        </div>""",
            'icon': 'marker'
        }
    }
    features.append(feature)

# 建立時間軸 GeoJson 物件
TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period='P1D',  # 每個資訊點的間隔為1天
    duration='P7D',  # 時間軸的總長度為7天
    auto_play=True,  # 自動播放
    loop=True,  # 循環播放
    max_speed=1,  # 播放速度為1
    loop_button=True,  # 顯示循環播放按鈕
    date_options='YYYY-MM-DD',  # 日期顯示格式
    time_slider_drag_update=True  # 可以拖動時間軸
).add_to(m)

# 給一個時間軸，將資訊點按照隨地震時間，隨時間軸依序顯示，且可以暫停、播放




    
   


# 顯示地圖
m.save('C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\20240409\\taiwan_eq.html')


