import requests
from bs4 import BeautifulSoup
import pandas as pd
import pandas as pd

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
print(df2)

# 將 DataFrame 寫入 CSV 檔案
df2.to_csv("C:\Users\User\Desktop\oil1.csv", index=False)

import matplotlib.pyplot as plt
import pandas as pd

# 分別保留1、2欄的資料 1、3欄的資料 1、4欄的資料 以及 1、5欄的資料
df2_12 = df2.iloc[:, [0, 1]].dropna()
df2_13 = df2.iloc[:, [0, 2]].dropna()
df2_14 = df2.iloc[:, [0, 3]].dropna()
df2_15 = df2.iloc[:, [0, 4]].dropna()

# 刪除 YYYY/MM/DD 下午 hh:mm:ss 格式的資料
df2_12 = df2_12[~df2_12.iloc[:, 0].str.contains('下午')]
df2_13 = df2_13[~df2_13.iloc[:, 0].str.contains('下午')]
df2_14 = df2_14[~df2_14.iloc[:, 0].str.contains('下午')]
df2_15 = df2_15[~df2_15.iloc[:, 0].str.contains('下午')]

# 把所有第1欄的資料型態轉成datetime
df2_12.iloc[:, 0] = pd.to_datetime(df2_12.iloc[:, 0])
df2_13.iloc[:, 0] = pd.to_datetime(df2_13.iloc[:, 0])
df2_14.iloc[:, 0] = pd.to_datetime(df2_14.iloc[:, 0])
df2_15.iloc[:, 0] = pd.to_datetime(df2_15.iloc[:, 0])

# 使用matplotlib 繪製折線圖 x軸是日期 y軸是油價
plt.figure(figsize=(12, 8))

plt.plot(df2_12.iloc[:, 0], df2_12.iloc[:, 1], label='無鉛汽油92')
plt.plot(df2_13.iloc[:, 0], df2_13.iloc[:, 1], label='無鉛汽油95')
plt.plot(df2_14.iloc[:, 0], df2_14.iloc[:, 1], label='無鉛汽油98')
plt.plot(df2_15.iloc[:, 0], df2_15.iloc[:, 1], label='超級/高級柴油')

plt.xlabel('日期')
plt.ylabel('油價')
plt.title('油價走勢圖')
plt.legend(loc='lower right', frameon=False)

#將字體改為微軟正黑體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']

plt.show()