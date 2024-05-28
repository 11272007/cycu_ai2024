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

# 存取新的csv檔


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

# 以GantryFrom_Lon、GantryFrom_Lat作為座標，在地圖上加入高速公路資訊
  
# 建立時間軸 GeoJson 物件
features = []
    
for i, row in df_data.iterrows():
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [row['GantryFrom_Lon'], row['GantryFrom_Lat']]
        },
        'properties': {
            'time': str(row['TimeInterval']),
            'popup': f"""<div style='width: 200px;'>
                            <b>TimeInterval:</b> {row['TimeInterval']}<br>
                            <b>GantryFrom:</b> {row['GantryFrom']}<br>
                            <b>GantryFrom_Lon:</b> {row['GantryFrom_Lon']}<br>
                            <b>GantryFrom_Lat:</b> {row['GantryFrom_Lat']}<br>
                            <b>SpaceMeanSpeed:</b> {row['SpaceMeanSpeed']}<br>
                            <b>v31:</b> {row['v31']}<br>
                            <b>v32:</b> {row['v32']}<br>
                            <b>v41:</b> {row['v41']}<br>
                            <b>v42:</b> {row['v42']}<br>
                            <b>v5:</b> {row['v5']}<br>
                            <b>weekday:</b> {row['weekday']}<br>
                            <b>holiday:</b> {row['holiday']}<br>
                            <b>WayDirectionFrom:</b> {row['WayDirectionFrom']}<br>
                            <b>WayDirectionTo:</b> {row['WayDirectionTo']}
                        </div>""",
            'icon': 'marker'
        }
    }
    features.append(feature)
        
TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period='P1D',  # 每個資訊點的間隔為1天
    duration='P7D',  # 時間軸的總長度為7天
    auto_play=True,  # 自動播放
    loop=True,  # 循環播放
    max_speed=1,  # 播放速度為1
    loop_button=True,  # 顯示循環播放按鈕
    ).add_to(m)
    
    
    
# 將地圖儲存為html檔
m.save('20240429.html')

# 在地圖上加入高速公路資訊，包含TimeInterval、GantryFrom、GantryFrom_Lon、GantryFrom_Lat、SpaceMeanSpeed、v31、v32、v41、v42、v5、weekday、holiday、WayDirectionFrom、WayDirectionTo
# 並且將各項資訊換行顯示
# 將高速公路資訊轉換為 GeoJson 格式

