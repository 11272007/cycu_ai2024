import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, griddata

# 讀取 CSV 文件並轉換為 DataFrame
df = pd.read_csv('C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\20240514\\20240429.csv')

for time in range(1, 289):
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

# 合併所有時間的擬合數據，第一欄是檔名中的時間，第二欄是里程，第三欄是31_交通量
df_all = pd.DataFrame(columns=['時間', '里程', '31_交通量'])
for time in range(1, 289):
    df_new = pd.read_csv(f'time_{time}_cubic_spline.csv')
    df_new['時間'] = time
    df_all = pd.concat([df_all, df_new], axis=0)

df_all.to_csv('all_cubic_spline.csv', index=False)

# 刪除所有時間的擬合數據
for time in range(1, 289):
    os.remove(f'time_{time}_cubic_spline.csv')

# 讀取合併後的擬合數據
df_all = pd.read_csv('all_cubic_spline.csv')

# X軸為里程，Y軸為時間，Z軸為31_交通量，建立網格
x = df_all['里程'].values
y = df_all['時間'].values
z = df_all['31_交通量'].values
xi = np.linspace(x.min(), x.max(), 1000)
yi = np.linspace(y.min(), y.max(), 1000)
zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')

# 繪製3D圖
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(xi, yi)
ax.plot_surface(X, Y, zi, cmap='viridis')
ax.set_xlabel('里程')
ax.set_ylabel('時間')
ax.set_zlabel('小客車交通量')
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 設置字體為中文字體

# 將繪製的3D圖以Z軸分別旋轉45度、135度、225度、315度，並保存為圖片
ax.view_init(elev=20, azim=45)
plt.savefig('11272007_45度.png')
ax.view_init(elev=20, azim=135)
plt.savefig('11272007_135度.png')
ax.view_init(elev=20, azim=225)
plt.savefig('11272007_225度.png')
ax.view_init(elev=20, azim=315)
plt.savefig('11272007_315度.png')

from PIL import Image

# 讀取四張圖片
images = [Image.open(f) for f in ['11272007_45度.png', '11272007_135度.png', '11272007_225度.png', '11272007_315度.png']]

# 獲取每張圖片的寬度和高度
widths, heights = zip(*(i.size for i in images))

# 計算合併後的圖片的寬度和高度
total_width = max(widths) * 2
total_height = max(heights) * 2

# 創建一個新的空白圖片，大小為合併後的大小
new_im = Image.new('RGB', (total_width, total_height))

# 將每張圖片貼到新的圖片上
new_im.paste(images[0], (0,0)) # 左上
new_im.paste(images[1], (max(widths),0)) # 右上
new_im.paste(images[2], (0,max(heights))) # 左下
new_im.paste(images[3], (max(widths),max(heights))) # 右下

# 在新的圖片上中間上方添加標題
from PIL import ImageDraw, ImageFont

draw = ImageDraw.Draw(new_im)
font = ImageFont.truetype('arial.ttf', 50)
draw.text((max(widths) // 1.25, 0), '11272007', font=font, fill='black')

# 保存合併後的圖片
new_im.save('combined.png')

# 刪除四張圖片
for f in ['11272007_45度.png', '11272007_135度.png', '11272007_225度.png', '11272007_315度.png']:
    os.remove(f)