import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta


def get_news():
    url = "https://sports.sina.com.cn/global/index.shtml"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    news_list = []
    for i, news in enumerate(soup.find(class_="ul-type1").find_all('a', limit=5)):  # 按需调整选择器和限制
        link = news['href']
        news_list.append((link))

    return news_list


def get_news_detail(url):
    print("start ", url)
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find(class_="main-title").text
    article = soup.find(id="artibody").find_all('p').__getitem__(1).text
    date = soup.find(class_="date").text
    # datetime.strptime(date, "%y年%m月%d日 %H:%M")
    print("title ", title, "article ", article, ",date ", date)
    return {"title": title, "article": article, "date": date}


def post_news_to_nodebb(api_url, api_key, detail):
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }

    data = {
        'cid': 7,
        'title': detail.get("title"),
        'content': detail.get("article"),
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Failed to post news: {detail.get('title')}")


def is_new(date_string):
    date = datetime.strptime(date_string, "%Y年%m月%d日 %H:%M")
    now = datetime.now()
    delta = now - date
    return delta <= timedelta(minutes=10)


news_list = get_news()
api_url = "https://www.ruiyi77.com/api/v3/topics"
api_key = "587f44bb-80a7-45ac-afc9-5702dc7e018f"  # 按需调整

for news in news_list:
    detail = get_news_detail(news)
    if is_new(detail.get("date")):
        post_news_to_nodebb(api_url, api_key, detail)
