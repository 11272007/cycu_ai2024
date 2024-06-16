import requests
from bs4 import BeautifulSoup
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt

# 獲取網頁內容
response = requests.get('https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil.aspx')

# 解析網頁內容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有的表格元素
tables = soup.find_all('table')

# 將 HTML 表格轉換為 DataFrame
df1 = pd.read_html(str(tables[0]))[0]
df2 = pd.read_html(str(tables[1]))[0]

# 獲取網頁內容
response = requests.get('https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil2019.aspx')

# 解析網頁內容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有的表格元素
tables = soup.find_all('table')

# 將 HTML 表格轉換為 DataFrame
df3 = pd.read_html(str(tables[0]))[0]
df4 = pd.read_html(str(tables[1]))[0]

#將df2和df4合併並打印出來
df2 = pd.concat([df2, df4])

# 保留調價日期、無鉛汽油95
df2 = df2[['調價日期', '無鉛汽油95']]

# 去除無鉛汽油95為空的列
df2 = df2.dropna(subset=['無鉛汽油95'])

# 將調價日期中有下午幾點、上午幾點的資料只取日期
df2['調價日期'] = df2['調價日期'].str.split(' ', expand=True)[0]

print(df2)

# 將 DataFrame 寫入 CSV 檔案
df2.to_csv("oil1.csv", index=False)

# 將日期轉換為日期格式並設為X軸，無鉛汽油95設為Y軸
df2['調價日期'] = pd.to_datetime(df2['調價日期'])
df2 = df2.set_index('調價日期')

# 繪製折線圖
df2.plot()

# 顯示圖表
plt.show()