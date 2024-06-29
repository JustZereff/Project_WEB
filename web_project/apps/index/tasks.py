import requests
from bs4 import BeautifulSoup
import json
import os
import time

API_KEY = '5a34eaa59405a1885754cbe1ad6e61ce'

def parse_and_save_news():
    script_dir = os.path.dirname(__file__)
    logs_dir = os.path.join(script_dir, 'logs')
    json_path = os.path.join(logs_dir, 'news_data.json')

    if os.path.exists(json_path):
        last_modified = os.path.getmtime(json_path)
        current_time = time.time()
        if current_time - last_modified < 4 * 3600:
            return  # Если файл изменялся менее 4 часов назад, не выполняем скрапинг

    payload = {
        'api_key': API_KEY,
        'url': 'https://bank.gov.ua/ua/news/all?perPage=25&page=1',
        'render': 'true',
        'follow_redirect': 'false'
    }
    response = requests.get('https://api.scraperapi.com/', params=payload)

    soup = BeautifulSoup(response.content, 'html.parser')
    news_items = soup.find_all('div', class_='collection-item post-inline post-with-image new')
    news_list = []

    for item in news_items:
        title_tag = item.find('a')
        title = title_tag.text.strip() if title_tag else 'Без заголовка'
        url = title_tag['href'] if title_tag else '#'
        timestamp_tag = item.find('time')
        timestamp = timestamp_tag.text.strip() if timestamp_tag else 'Без даты'
        tags_div = item.find('div', class_='tags')
        tags = [tag.text.strip() for tag in tags_div.find_all('a')] if tags_div else []

        news_list.append({
            'title': title,
            'url': url,
            'timestamp': timestamp,
            'tags': tags
        })

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(news_list, json_file, ensure_ascii=False, indent=4)

    # Сохраняем текущее время как дату последнего изменения файла
    os.utime(json_path, times=(current_time, current_time))

if __name__ == "__main__":
    parse_and_save_news()