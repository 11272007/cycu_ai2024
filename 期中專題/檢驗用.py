import pandas as pd
import glob

# 找出資料夾中所有的 CSV 檔案
csv_files = glob.glob('C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\高速公路資訊\\*.csv')

# 寫出總共有多少筆csv檔
print(f"總共有{len(csv_files)}筆csv檔")

# 如果所有列數一致，則寫OK，如果有不一致，則寫NO
dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

if all(len(df) == len(dfs[0]) for df in dfs):
    print("OK")
    print(f"每個CSV檔案有{len(dfs[0])}列")
else:
    print("NO")

