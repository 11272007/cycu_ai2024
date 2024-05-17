import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# 讀取 CSV 文件並轉換為 DataFrame
df = pd.read_csv('C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\20240514\\20240429.csv')

# 留下時間、里程、31_交通量、31_車速列
df = df[['時間', '里程', '31_交通量', '31_車速']]

# 設定里程為X軸，時間為Y軸，31_交通量為Z軸
x = df['里程'].values
y = df['時間'].values
z = df['31_交通量'].values

# 創建一個規則的網格
xi = np.linspace(x.min(), x.max(), 100)
yi = np.linspace(y.min(), y.max(), 100)
xi, yi = np.meshgrid(xi, yi)

# 使用 griddata 進行插值
zi = griddata((x, y), z, (xi, yi), method='cubic')

# 繪製3D圖
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xi, yi, zi, cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()




