import os
import requests
from bs4 import BeautifulSoup

# 定義網頁URL
base_url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/20240325/{:02d}/"

# 抓取網頁上的所有.csv檔案連結
csv_links = []
for i in range(24):
    url = base_url.format(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = [a['href'] for a in soup.find_all('a', href=True)]
    csv_links.extend([link for link in links if link.endswith('.csv')])

# 創建一個目錄來存儲下載的檔案
if not os.path.exists('csv_files'):
    os.makedirs('csv_files')

# 下載每個.csv檔案並保存到創建的目錄中
for link in csv_links:
    response = requests.get(base_url.format(i) + link)
    with open('csv_files/' + link, 'wb') as file:
        file.write(response.content)

import pandas as pd
# 讀取所有下載的.csv檔案
files = os.listdir('csv_files')
dfs = [pd.read_csv('csv_files/' + file) for file in files]

# 合併所有檔案
df = pd.concat(dfs)
print(df)

# 將合併後的檔案保存為一個新的.csv檔案
df.to_csv('merged.csv', index=False)

