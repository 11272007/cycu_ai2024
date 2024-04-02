# crawler from rss of central weather agency

import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import os

import feedparser

# url = https://www.cwa.gov.tw/rss/forecast/36_01.xml
# 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, to 22

for num in range(1, 23):
    #string format with prefix 0 if num < 10
    url = 'https://www.cwa.gov.tw/rss/forecast/36_' + str(num).zfill(2) + '.xml'
    
    # get xml from url
    response = requests.get(url)
    # parse rss feed
    feed = feedparser.parse(response.content)
    # extract the first title
    title = feed.entries[0].title
    # extract the first three characters
    first_three_chars = title[:3]
    # extract the text between "溫度: " and "降雨機率"
    temperature = title.split("溫度: ")[1].split("降雨機率")[0]
    # print the modified title
    print(first_three_chars + temperature)
    print("=======================================")



#尋找台灣的區界地圖 shape file/ geojson file
#https://data.gov.tw/dataset/7441

#read 20240402/tract_20140313.json as geopanas
import geopandas as gpd
import pandas as pd

#read shape file
taiwan=gpd.read_file('20240402/county/county_moi_1090820.shp')
import os
# print cwd
print(taiwan.shape)

# create a new column in the taiwan dataframe to store the temperature values
taiwan['Temperature'] = ''

# iterate through the feed entries
for num in range(1, 23):
    url = 'https://www.cwa.gov.tw/rss/forecast/36_' + str(num).zfill(2) + '.xml'
    response = requests.get(url)
    feed = feedparser.parse(response.content)
    title = feed.entries[0].title
    first_three_chars = title[:3]
    temperature = title.split("溫度: ")[1].split("降雨機率")[0]
    
    # find the corresponding county in the taiwan dataframe and update the temperature value
    taiwan.loc[taiwan['COUNTYNAME'] == first_three_chars, 'Temperature'] = temperature

# plot taiwan using matplotlib
fig, ax = plt.subplots(figsize=(10, 10))
taiwan.plot(ax=ax, color='lightgray', edgecolor='black')

# plot the temperature values at the center of each county
for idx, row in taiwan.iterrows():
    centroid = row['geometry'].centroid
    temperature = row['Temperature']
    ax.text(centroid.x, centroid.y, temperature, ha='center', va='center')

# 將數字保留在圖範圍內
ax.set_xlim(117.7, 122.5)
ax.set_ylim(21.7, 26.5)

# 將溫度範圍轉換為平均溫度
def convert_temperature_range_to_average(temp_range):
    temps = temp_range.split('~')
    if len(temps) == 2:
        return (float(temps[0]) + float(temps[1])) / 2
    else:
        return pd.to_numeric(temp_range, errors='coerce')

taiwan['Temperature'] = taiwan['Temperature'].apply(convert_temperature_range_to_average)

# 以溫度由高到低，從紅到藍
taiwan.plot(column='Temperature', cmap='coolwarm', ax=ax)

plt.title('台灣 04/02 今晚明晨溫度預報', fontproperties='Arial Unicode MS')
plt.show()