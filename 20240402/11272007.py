import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send HTTP request
response = requests.get('https://www.cwa.gov.tw/rss/forecast/36_03.xml')

# Parse the webpage content
soup = BeautifulSoup(response.content, 'xml')

# Find the third <description> tag and extract its content
description = soup.find_all('description')[2].text

# Extract the date and text before the first <BR> tag
date_text = description.split('<BR>')[0]

# Create a DataFrame with the extracted date and text
df = pd.DataFrame([date_text], columns=['Date and Text'])

print(df)

# 匯出成 CSV 檔案
df.to_csv('20240402/11272007.csv', index=False)