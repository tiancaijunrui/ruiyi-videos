import hashlib
import json
import random
import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
}


def get_news():
    url = "https://www.gamersky.com/news/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    news_list = []
    for i, news in enumerate(soup.find(class_="contentpaging").find_all(class_="tit", limit=5)):  # 按需调整选择器和限制
        for link in news.find_all('a'):
            href = link['href']
            news_list.append(href)

    return news_list


def get_news_detail(url):
    print("start ", url)
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find(class_="Mid2L_tit").find("h1").text
    articleArr = [child for child in soup.find(class_="Mid2L_con").find_all("p") if
                  child.__class__ != "GsImageLabel" and child.text != ""][:-2]
    article = "\n".join([str(i.text) for i in articleArr])
    date = soup.find(class_="Mid2L_tit").find(class_="detail").text
    match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', date)
    if match:
        date = match.group()
    print("title ", title, "article ", article, ",date ", date)
    return {"title": title, "article": article, "date": date}


def is_new(date_string):
    date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    delta = now - date
    return delta <= timedelta(minutes=10)


def translate_baidu(content, from_lang, to_lang, appid, secret_key):
    base_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    salt = random.randint(32768, 65536)
    sign = appid + content + str(salt) + secret_key
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = base_url + "?appid=" + appid + "&q=" + content + "&from=" + from_lang + "&to=" + to_lang + "&salt=" + str(
        salt) + "&sign=" + sign

    try:
        response = requests.get(url, headers=headers)
        result_all = response.json()
        result = result_all['trans_result'][0]['dst']
        return result
    except Exception as e:
        print(e)


def post_news_to_nodebb(api_url, api_key, detail):
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }

    data = {
        'cid': 8,
        'title': detail.get("title"),
        'content': detail.get("article"),
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Failed to post news: {detail.get('title')}")


appid = '20201209000643067'
secret_key = 'nLLqUsa_N2vbOOMoLV7l'
api_url = "https://www.ruiyi77.com/api/v3/topics"
api_key = "587f44bb-80a7-45ac-afc9-5702dc7e018f"

news_list = get_news()
for news in news_list:
    try:
        detail = get_news_detail(news)
        if is_new(detail.get("date")):
            post_news_to_nodebb(api_url, api_key, detail)
    except Exception as e:
        print(e)
