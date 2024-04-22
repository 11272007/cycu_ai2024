# 讀取csv檔並轉成dataframe

import pandas as pd
df = pd.read_csv('C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\研究\\map.csv')
print(df)

# 第1行為地區、第2行為土壤資訊
df.columns = ['地區', '土壤資訊']

# 利用folium套件繪製地圖
import folium
from folium.plugins import TimestampedGeoJson
import geopy
from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="myGeocoder")

features = []
for i in range(len(df)):
    try:
        location = geolocator.geocode(df['地區'][i], timeout=10)
        # 如果找到了位置，則加入到 features 列表中
        if location:
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [location.longitude, location.latitude]
                },
                'properties': {
                    'popup': df['地區'][i],
                    'icon': 'circle',
                    'iconstyle': {
                        'fillColor': 'green',
                        'fillOpacity': 0.6,
                        'stroke': 'false',
                        'radius': 5
                    }
                }
            })
    except Exception as e:
        print(f"Error: {e}")
    # 每次請求之後暫停一秒
    time.sleep(1)

# 建立地圖
m = folium.Map(location=[23.5, 121], zoom_start=7)

# 顯示地圖
for feature in features:
    folium.Marker(
        location=feature['geometry']['coordinates'],
        popup=feature['properties']['popup'],
        icon=folium.Icon(color='blue', icon=feature['properties']['icon'])
    ).add_to(m)

m.save('C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\研究\\map.html')





