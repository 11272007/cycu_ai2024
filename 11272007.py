import feedparser

# RSS Feed URL
url = "https://news.pts.org.tw/xml/newsfeed.xml"

# 解析 RSS Feed
feed = feedparser.parse(url)

#提取 Feed 內容
for entry in feed.entries:
    print(entry.title)
    #印出 summary
    print(entry.summary)

    # 印出區隔線
    print("="*50)

    # 將含有 以色列 的標題印出 並轉成CSV格式
    if "屏東" in entry.title:
        print(f"{entry.title},{entry.link}")
        print("="*50)
        # 檔案位置在 C:\Users\jimmy\OneDrive\桌面\cycu_ai2024\11272007.csv
        with open("C:\\Users\\jimmy\\OneDrive\\桌面\\cycu_ai2024\\11272007.csv", "a", encoding="utf-8") as f:
            f.write(f"{entry.title},{entry.link}\n")

    