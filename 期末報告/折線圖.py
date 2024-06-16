import pandas as pd
import matplotlib.pyplot as plt

# 讀取csv檔
df = pd.read_csv('資料整理.csv')

# 將日期和無鉛汽油95保留為新的DataFrame
df1 = df[['日期', '無鉛汽油95']]
# 將無鉛汽油95為空的列刪除
df1 = df1.dropna(subset=['無鉛汽油95'])
# 將日期轉為日期格式並設為X軸，無鉛汽油95設為Y軸
df1['日期'] = pd.to_datetime(df1['日期'])
df1 = df1.set_index('日期')

# 將日期和國際原油保留為新的DataFrame
df2 = df[['日期', '國際原油']]
# 將國際原油為空的列刪除
df2 = df2.dropna(subset=['國際原油'])
# 將日期轉為日期格式並設為X軸，國際原油設為Y軸
df2['日期'] = pd.to_datetime(df2['日期'])
df2 = df2.set_index('日期')

# 將日期和台股指數保留為新的DataFrame
df3 = df[['日期', '台股指數']]
# 將台股指數為空的列刪除
df3 = df3.dropna(subset=['台股指數'])
# 將日期轉為日期格式並設為X軸，台股指數設為Y軸
df3['日期'] = pd.to_datetime(df3['日期'])
df3 = df3.set_index('日期')

# 將日期和道瓊指數保留為新的DataFrame
df4 = df[['日期', '道瓊指數']]
# 將道瓊指數為空的列刪除
df4 = df4.dropna(subset=['道瓊指數'])
# 將日期轉為日期格式並設為X軸，道瓊指數設為Y軸
df4['日期'] = pd.to_datetime(df4['日期'])
df4 = df4.set_index('日期')

# 繪製一張折線圖，裡面包含四條線，分別是無鉛汽油95、國際原油、台股指數、道瓊指數
fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:red'
ax1.set_xlabel('日期')
ax1.set_ylabel('價格 (台幣)')
ax1.plot(df1, color=color, label='無鉛汽油')  # Add label here
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(0, 500)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('')  # we already handled the x-label with ax1
ax2.plot(df2, label='國際原油')
ax2.plot(df3, label='台股指數')
ax2.plot(df4, label='道瓊指數')
ax2.tick_params(axis='y')

fig.tight_layout()  # otherwise the right y-label is slightly clipped

# 將字體放大
plt.xticks(fontsize='large')
plt.yticks(fontsize='large')
plt.title('趨勢折線圖')
fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9), fontsize='large')  # Adjust the position and font size of the legend
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Set the font to support Chinese characters
plt.show()
