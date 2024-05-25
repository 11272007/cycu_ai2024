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

# 只保留ETag編號開頭為01的資料
df = df[df['ETag'].str.startswith('01')]

# 將編號有N的資料排列在前面，有S的資料排列在後面
df['方向'] = df['ETag'].str[-1].replace({'N': 0, 'S': 1})
df.sort_values('方向', inplace=True)

# 重新排列，第一欄為方向，第二欄為ETag，第三欄為經度，第四欄為緯度
df = df[['方向', 'ETag', '經度', '緯度']]
df.reset_index(drop=True, inplace=True)

# 先照方向排序，再照里程排序
df.sort_values(['方向'], inplace=True)

# 將 DataFrame 寫入 CSV 文件
df.to_csv('ETag.csv', index=False, encoding='utf-8-sig')