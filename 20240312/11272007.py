import pandas as pd
import matplotlib.pyplot as plt

# 讀取CSV文件
df = pd.read_csv('/workspaces/cycu_ai2024/20240312/112年1-10月交通事故簡訊通報資料.csv')

# 留下"國道名稱"欄位中有 "1" 且"方向"欄為中有 "南" 的資料
filtered_df = df[(df['國道名稱'].str.contains('3')) & (df['方向'].str.contains('南'))]

# 將 '年', '月', '日', '時', '分' 這幾個欄位合併成一個欄位 '事件開始'，並且轉換成日期格式
filtered_df['事件開始'] = filtered_df['年'].astype(str) + '-' + filtered_df['月'].astype(str) + '-' + filtered_df['日'].astype(str) + ' ' + filtered_df['時'].astype(str) + ':' + filtered_df['分'].astype(str)
filtered_df['事件開始'] = pd.to_datetime(filtered_df['事件開始'])

# 將 '年', '月', '日', '事件排除' 這幾個欄位合併成一個欄位 '事件排除'，並且轉換成日期格式
filtered_df['事件排除'] = filtered_df['年'].astype(str) + '-' + filtered_df['月'].astype(str) + '-' + filtered_df['日'].astype(str) + ' ' + filtered_df['事件排除'].astype(str)
filtered_df['事件排除'] = pd.to_datetime(filtered_df['事件排除'])

# 只留下 '事件開始', '事件排除', '里程'
filtered_df = filtered_df[['事件開始', '事件排除', '里程']]

#將 '事件開始' '事件排除' 兩個欄位轉換成 unix time stamp 並使用整數表示
filtered_df['事件開始1'] = filtered_df['事件開始'].apply(lambda x: int(x.timestamp()))
filtered_df['事件排除1'] = filtered_df['事件排除'].apply(lambda x: int(x.timestamp()))

import matplotlib.font_manager as fm

# 設定中文字體
plt.rcParams['font.family'] = 'Arial Unicode MS'

# 將 '事件開始1' 為 X軸起點 ， '事件排除1' 為X軸終點 繪製線段，'里程' 為Y軸
for index, row in filtered_df.iterrows():
    plt.plot([row['事件開始1'], row['事件排除1']], [row['里程'], row['里程']])
plt.xlabel('事故處理時間')
plt.ylabel('里程')
plt.title('國道3號南向 事故處理時間-里程 (11272007)')

# 顯示中文
plt.rcParams['axes.unicode_minus'] = False

plt.show()


