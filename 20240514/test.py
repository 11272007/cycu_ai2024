import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, griddata

# 讀取 CSV 文件並轉換為 DataFrame
df = pd.read_csv('C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\20240514\\20240429.csv')

for time in range(1, 20):
    data = df[df['時間'] == time].copy()
    mileage = data['里程'].values
    traffic_volume = data['31_交通量'].values

    # 確保里程數據是嚴格遞增的
    sort_indices = np.argsort(mileage)
    mileage = mileage[sort_indices]
    traffic_volume = traffic_volume[sort_indices]

    # 檢查是否有重複的里程值
    _, unique_indices = np.unique(mileage, return_index=True)
    mileage = mileage[unique_indices]
    traffic_volume = traffic_volume[unique_indices]

    # 使用 cubic spline 進行擬合
    cs = CubicSpline(mileage, traffic_volume)

    x = np.linspace(mileage.min(), mileage.max(), 1000)  # 增加擬合點數至1000
    y = cs(x)
    y[y < 0] = 0  # 將小於0的值設為0

    # 暫存擬合的X和Y
    data = np.array([x, y]).T

    # 將擬合的數據保存到 CSV 文件
    df_new = pd.DataFrame(data, columns=['里程', '31_交通量'])
    df_new.to_csv(f'time_{time}_cubic_spline.csv', index=False)

# 合併所有時間的擬合數據，第一欄是時間，第二欄是里程，第三欄是31_交通量
data = np.concatenate([np.full((len(data), 1), time), data], axis=1)
df = pd.DataFrame(data, columns=['時間', '里程', '31_交通量'])
df.to_csv('all_time_cubic_spline.csv', index=False)

# 刪除所有時間的擬合數據
for time in range(1, 20):
    os.remove(f'time_{time}_cubic_spline.csv')



# 創建一個網格
xi = np.linspace(df['里程'].min(), df['里程'].max(), 1000)
yi = np.linspace(df['時間'].min(), df['時間'].max(), 1000)
xi, yi = np.meshgrid(xi, yi)

# 使用griddata進行插值
zi = griddata((df['里程'], df['時間']), df['31_交通量'], (xi, yi), method='cubic')
zi[zi < 0] = 0  # 將小於0的值設為0

# 繪製3D圖
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xi, yi, zi, cmap='viridis')
ax.set_xlabel('Mileage')
ax.set_ylabel('Time')
ax.set_zlabel('Traffic Volume')

plt.show()











