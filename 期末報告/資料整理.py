import pandas as pd


# 讀取兩個csv檔
df1 = pd.read_csv('95無鉛汽油價格.csv')
df2 = pd.read_csv('國際原油價格.csv')
df3 = pd.read_csv('台股加權指數.csv')
df4 = pd.read_csv('道瓊斯工業指數.csv')

# 將df1的第一欄名稱改為日期，並轉為datetime格式
df1.columns = ['日期', '無鉛汽油95']
df1['日期'] = pd.to_datetime(df1['日期'])
# 保留日期範圍在2000年1月1日至2023年12月31日，並將有空值的列刪除
df1 = df1[(df1['日期'] >= '2000-01-01') & (df1['日期'] <= '2023-12-31')]
df1 = df1.dropna()

# 將df2的第一欄名稱改為日期，並轉為datetime格式
df2.columns = ['日期', '西德州', '杜拜', '北海布蘭特', '匯率']
df2['日期'] = pd.to_datetime(df2['日期'])
# 保留日期、杜拜、匯率，並將有空值的列刪除
df2 = df2[['日期', '杜拜', '匯率']]
df2 = df2.dropna()
# 將杜拜與匯率轉相乘，合併成新的欄位
df2['杜拜'] = df2['杜拜'] * df2['匯率']
df2 = df2.drop(columns=['匯率'])
# 保留日期範圍在2000年1月1日至2023年12月31日
df2 = df2[(df2['日期'] >= '2000-01-01') & (df2['日期'] <= '2023-12-31')]
df2 = df2.dropna()

# 將df3的第一欄名稱改為日期，並轉為datetime格式
df3.columns = ['日期', '開市', '最高', '最低', '收市', '經調收市價', '成交量']
df3['日期'] = pd.to_datetime(df3['日期'])
# 保留日期、收市，並將有空值的列刪除
df3 = df3[['日期', '收市']]
df3 = df3.dropna()
# 保留日期範圍在2000年1月1日至2023年12月31日
df3 = df3[(df3['日期'] >= '2000-01-01') & (df3['日期'] <= '2023-12-31')]
df3 = df3.dropna()

# 將df4的第一欄名稱改為日期，並轉為datetime格式
df4.columns = ['日期', '收市', '開市', '高', '低', '成交量', '升跌（%）']
df4['日期'] = pd.to_datetime(df4['日期'])
# 保留日期、收市，並將有空值的列刪除
df4 = df4[['日期', '收市']]
df4 = df4.dropna()
# 將收市欄位 "" 中的字元取出
df4['收市'] = df4['收市'].str.replace(',', '').str.extract('(\d+)', expand=False)

# 保留日期範圍在2000年1月1日至2023年12月31日
df4 = df4[(df4['日期'] >= '2000-01-01') & (df4['日期'] <= '2023-12-31')]
df4 = df4.dropna()

# 建立新的DataFrame，第一欄為日期，範圍在2000年1月1日至2023年12月31日
df = pd.DataFrame({'日期': pd.date_range(start='2000-01-01', end='2023-12-31')})
# 將df1、df2、df3、df4依照日期填入新的DataFrame，並將空值保留空值，不填入0，欄位依序為日期、無鉛汽油95、國際原油、台股指數、道瓊指數
df = pd.merge(df, df1, on='日期', how='left')
df = pd.merge(df, df2, on='日期', how='left')
df = pd.merge(df, df3, on='日期', how='left')
df = pd.merge(df, df4, on='日期', how='left')

# 欄位名稱依序為日期、無鉛汽油95、國際原油、台股指數、道瓊指數
df.columns = ['日期', '無鉛汽油95', '國際原油', '台股指數', '道瓊指數']

# 將DataFrame寫入CSV檔案
df.to_csv("資料整理.csv", index=False)




