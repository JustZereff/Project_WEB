from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time
import os

def parse_and_save_news():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get('https://bank.gov.ua/ua/news/all?perPage=25&page=1')
        time.sleep(5)  # Подождём, чтобы страница полностью загрузилась

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

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

        # Определение пути для сохранения JSON файла
        script_dir = os.path.dirname(__file__)
        logs_dir = os.path.join(script_dir, 'logs')
        json_path = os.path.join(logs_dir, 'news_data.json')

        # Создание директории, если она не существует
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Сохранение данных в JSON файл
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(news_list, json_file, ensure_ascii=False, indent=4)

    finally:
        driver.quit()

