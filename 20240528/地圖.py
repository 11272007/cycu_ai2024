import pandas as pd
import glob

# 讀取csv檔案
df1 = pd.read_csv('ETag.csv')
df2 = pd.read_csv('D:\\download\\TDCS_M05A_20240522_235500.csv')

# 保留df1的ETag欄位
df1 = df1[['ETag']]

# 保留df2的第二欄並轉換為DataFrame
df2 = df2.iloc[:, 1].to_frame()
# 命名為ETag
df2.columns = ['ETag']
# 將重複的資料刪除
df2 = df2.drop_duplicates()

# 將df1與df2重複的資料列出
df = pd.merge(df1, df2, on='ETag', how='inner')

# 將結果寫入csv檔案
df.to_csv('result.csv', index=False, encoding='utf-8-sig')


