import pandas as pd
import matplotlib.pyplot as plt

# 讀取csv檔
df = pd.read_csv('資料整理.csv')

# 保留無鉛汽油95和道瓊指數兩欄
df = df[['國際原油', '道瓊指數']]
# 刪除有空值的列
df = df.dropna()

# 繪製散點圖，X軸為台股指數，Y軸為無鉛汽油95
plt.scatter(df['國際原油'], df['道瓊指數'])
plt.xlabel('國際原油', fontsize=24)
plt.ylabel('道瓊指數', fontsize=24)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 設定字體為中文字體

# 以圖上有的點，繪製回歸線
import numpy as np
from sklearn.linear_model import LinearRegression

x = df['國際原油'].values.reshape(-1, 1)
y = df['道瓊指數'].values.reshape(-1, 1)

model = LinearRegression()
model.fit(x, y)
y_pred = model.predict(x)
plt.plot(x, y_pred, color='red')

# 標示回歸線的方程式及R平方值
plt.text(x.min(), y.max(), f'y = {model.coef_[0][0]:.2f}x + {model.intercept_[0]:.2f}\nR^2 = {model.score(x, y):.2f}', color='black')

plt.show()