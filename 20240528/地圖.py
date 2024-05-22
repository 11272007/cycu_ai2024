import pandas as pd
import glob

# 讀取csv檔案
df1 = pd.read_csv('ETag.csv')
df2 = pd.read_csv('高速公路資訊\\20240101.csv')

# 比較df1中方向為0的里程和df2中方向為0且時間為1的里程
df1 = df1[df1['方向'] == 0].copy()
df2 = df2[(df2['方向'] == 0) & (df2['時間'] == 1)].copy()

# df1和df2只保留里程欄位
df1 = df1[['里程']].copy()
df2 = df2[['里程']].copy()

# 比較df1和df2，列出兩個DataFrame中非重複的資料
df1 = df1.merge(df2, on='里程', how='outer', indicator=True)
df1 = df1[df1['_merge'] != 'both'].copy()

# 打印出df1和df2有幾筆資料相同
print(df1)