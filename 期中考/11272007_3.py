import pandas as pd
import requests
import pandas as pd
from bs4 import BeautifulSoup

# 從 URL 獲取 XML 數據
response = requests.get('https://tisvcloud.freeway.gov.tw/history/motc20/ETag.xml')

# 使用 BeautifulSoup 解析 XML 數據
soup = BeautifulSoup(response.content, 'lxml')

# 創建一個空的 DataFrame
df = pd.DataFrame(columns=["ETag", "經度", "緯度"])

# 遍歷每個 ETag 節點
for etag in soup.find_all('etag'):
    id_node = etag.find('etaggantryid')
    lon_node = etag.find('positionlon')
    lat_node = etag.find('positionlat')

    if id_node and lon_node and lat_node:
        id = id_node.text
        lon = lon_node.text
        lat = lat_node.text

        # 將數據添加到 DataFrame
        df.loc[len(df)] = [id, lon, lat]

# 讀取csv檔並轉成DataFrame
df_data = pd.read_csv('高速公路資訊(特徵化)\\M05A_20240429_feature.csv')

# 添加新的欄位，將GantryFrom對應到df中的ETag，若相同則添加經度、緯度，若不同則添加空值
df_data['GantryFrom_Lon'] = df_data['GantryFrom'].map(df.set_index('ETag')['經度'])
df_data['GantryFrom_Lat'] = df_data['GantryFrom'].map(df.set_index('ETag')['緯度'])

# 若經度、緯度為空值，刪除該列
df_data = df_data.dropna(subset=['GantryFrom_Lon', 'GantryFrom_Lat'])

# 相同的TimeInterval下，若GantryFrom有相同值，則保留SpaceMeanSpeed較大的那一列
df_data = df_data.sort_values('SpaceMeanSpeed', ascending=False).drop_duplicates(['TimeInterval', 'GantryFrom'])

# 刪除SpaceMeanSpeed大於199的列
df_data = df_data[df_data['SpaceMeanSpeed'] <= 199]

# 重新排序列，以TimeInterval、WayIDFrom、WayMilageFrom
df_data = df_data.sort_values(['TimeInterval', 'WayIDFrom', 'WayMilageFrom'])

# 留下TimeInterval為20240429 00:00:00到20240429 00:10:00的資料
df_data = df_data[(df_data['TimeInterval'] >= '2024-04-29 00:00:00') & (df_data['TimeInterval'] <= '2024-04-29 23:55:00')]
df_data = df_data.reset_index(drop=True)



# 利用folium套件繪製地圖以及GeoJson建立時間軸
import folium
from folium.plugins import TimestampedGeoJson

# 將TimeInterval轉換為datetime格式
df_data['TimeInterval'] = pd.to_datetime(df_data['TimeInterval'])

# 將GantryFrom_Lon、GantryFrom_Lat轉換為float格式
df_data['GantryFrom_Lon'] = df_data['GantryFrom_Lon'].astype(float)
df_data['GantryFrom_Lat'] = df_data['GantryFrom_Lat'].astype(float)

# 取得台灣地圖中心點
center = [23.5, 121]

# 建立地圖
m = folium.Map(location=center, zoom_start=7)

# 在地圖上標記每個點，並在點擊座標點時顯示該點的資訊，包括TimeInterval、GantryFrom_Lon、GantryFrom_Lat、SpaceMeanSpeed
# 並以TimeInterval為時間軸，將每五分鐘的資料點依序顯示，且在TimeInterval變動時，前一個TimeInterval的資料點會消失
# 座標的顏色依照SpeedClass決定，0為白色、1為紫色、2為紅色、3為橘色、4為黃色、5為綠色
features = []
colors = ['white', 'purple', 'red', 'orange', 'yellow', 'green']
for i in range(len(df_data)):
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [df_data['GantryFrom_Lon'][i], df_data['GantryFrom_Lat'][i]]
        },
        'properties': {
            'time': str(df_data['TimeInterval'][i]),
            'popup': f"""<div style='width: 200px;'>
                            <b>時間:</b> {df_data['TimeInterval'][i]}<br>
                            <b>走向:</b> {df_data['WayDirectionFrom'][i]}<br>
                            <b>門架編號:</b> {df_data['GantryFrom'][i]}<br>
                            <b>門架經度:</b> {df_data['GantryFrom_Lon'][i]}<br>
                            <b>門架緯度:</b> {df_data['GantryFrom_Lat'][i]}<br>
                            <b>小客車平均速度:</b> {df_data['SpaceMeanSpeed'][i]}<br>
                            <b>小客車交通量:</b> {df_data['v31'][i]}<br>
                            <b>小貨車交通量:</b> {df_data['v32'][i]}<br>
                            <b>大客車交通量:</b> {df_data['v41'][i]}<br>
                            <b>大貨車交通量:</b> {df_data['v42'][i]}<br>
                            <b>聯結車交通量:</b> {df_data['v5'][i]}
                        </div>""",
            'icon': 'circle',
            'iconstyle': {
                'fillColor': colors[int(df_data['SpeedClass'][i])],  # 將 SpeedClass 轉換為整數
                'fillOpacity': 1,
                'stroke': 'false',
                'color': 'transparent',
                'radius': 5
            },
        }
    }
    features.append(feature)
    
# 建立時間軸 GeoJson 物件
TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period='PT5M',  # 每個資訊點的間隔為5分鐘
    add_last_point=True,  # 最後一個資訊點會一直顯示
    auto_play=True,  # 自動播放
    loop=False,  # 不循環播放
    max_speed=1,  # 播放速度為1
    loop_button=True,  # 顯示循環播放按鈕
    time_slider_drag_update=True,  # 拖動時間軸時更新資訊點
    duration='P1D',  # 時間軸的總長度為1天
    date_options='YYYY-MM-DD HH:mm:ss'  # 日期格式
).add_to(m)

# 顯示地圖
m.save('20240429_map.html')
