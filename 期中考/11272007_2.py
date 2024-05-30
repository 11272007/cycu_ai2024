import pandas as pd
import os

# 創建一個新的資料夾
os.makedirs("高速公路資訊(特徵化)", exist_ok=True)

# 設定一個日期範圍
dates = pd.date_range(start='2024-01-01', end='2024-04-30', freq='D')

# 設定特定資料夾路徑
folder_path = '高速公路資訊'

# 讀取資料夾中的檔案
for date in dates:
    filename = f"M05A_{date.strftime('%Y%m%d')}.csv"
    file_path = os.path.join(folder_path, filename)
    
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
    else:
        print(f"File {filename} does not exist.")

    # 添加欄位，以日期判斷星期幾，0代表星期日、1代表星期一、...、6代表星期六
    df['weekday'] = date.weekday() + 1
    # 若星期日則為0
    if date.weekday() == 6:
        df['weekday'] = 0
    # 假日定義為星期六或星期日，以及中秋節、元旦、春節、清明節、端午節、國慶日、勞動節、雙十節、元宵節、重陽節、除夕
    holidays = ['2024-01-01', '2024-02-09', '2024-02-10','2024-02-12','2024-02-13','2024-02-14', '2024-02-24', '2024-04-04','2024-05-01', '2024-06-10', '2024-09-17',
                 '2024-10-10', '2024-11-11']
    # 添加欄位，日期若為星期六、星期日或上面定義之holidays則定義為假日，1代表假日、0代表非假日
    df['holiday'] = 0
    if date.strftime('%Y-%m-%d') in holidays or date.weekday() == 5 or date.weekday() == 6:
        df['holiday'] = 1
    # 假日前一天為-1
    holidays_before = ['2023-12-31', '2024-02-08', '2024-02-23', '2024-04-03','2024-04-30', '2024-09-16', '2024-10-09']
    if date.strftime('%Y-%m-%d') in holidays_before or date.weekday() == 4:
        df['holiday'] = -1
    # 添加欄位"WayIDFrom"，代表GantryFrom的前三個字元
    df['WayIDFrom'] = df['GantryFrom'].str[:3]
    # 添加欄位"WayIDTo"，代表GantryTo的前三個字元
    df['WayIDTo'] = df['GantryTo'].str[:3]
    # 添加欄位"WayMilageFrom"，代表GantryFrom的中間四位數
    df['WayMilageFrom'] = df['GantryFrom'].str[3:7]
    # 添加欄位"WayMilageTo"，代表GantryTo的中間四位數
    df['WayMilageTo'] = df['GantryTo'].str[3:7]
    # 添加欄位"WayDirectionFrom"，代表GantryFrom的最後一個字元，且N為北、S為南、E為東、W為西，以中文表示
    df['WayDirectionFrom'] = df['GantryFrom'].str[-1]
    df['WayDirectionFrom'] = df['WayDirectionFrom'].replace({'N': '北', 'S': '南', 'E': '東', 'W': '西'})
    # 添加欄位"WayDirectionTo"，代表GantryTo的最後一個字元，且N為北、S為南、E為東、W為西，以中文表示
    df['WayDirectionTo'] = df['GantryTo'].str[-1]
    df['WayDirectionTo'] = df['WayDirectionTo'].replace({'N': '北', 'S': '南', 'E': '東', 'W': '西'})
    # 添加欄位"速度分級 SpeedClass"，代表SpaceMeanSpeed的速度分級，-100~0，1~20，21~40，41~60，61~80，81~200分別定義為0，1，2，3，4，5
    df['SpeedClass'] = pd.cut(df['SpaceMeanSpeed'], bins=[-100, 0, 20, 40, 60, 80, 200], labels=[0, 1, 2, 3, 4, 5])     
    
    # 將資料寫入新的csv檔案
    df.to_csv(f"高速公路資訊(特徵化)\\M05A_{date.strftime('%Y%m%d')}_feature.csv", index=False, encoding='utf-8-sig')    
    
