import requests
from bs4 import BeautifulSoup
import re
import time
from tqdm import tqdm
import json

domain = 'https://habr.com'
srch = 'ru/hub'
#TODO: вводить/передавать хаб для парсинга
tag = 'kubernetes'
url = f'{domain}/{srch}/{tag}'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
items = {}

#Первый запрос, парсинг первой страницы и записываем в словарь
result = requests.get(url, headers=headers)
soup = BeautifulSoup(result.text, 'html.parser')
item_tags = soup.find_all('a', class_='post__title_link')
for item in item_tags:
    item_link = item.get('href')
    item_title = item.get_text()
    items[item_title] = item_link
#print(items)

#Дальше надо узнать сколько всего страниц и распарсить оставшиеся со 2 по n
#Находим на первой странице блок с ссылкой на последнюю страницу
last_page = soup.find_all('a', title='Последняя страница')
#Получаем часть урл последней страницы
link_last_page = ''
for i in last_page:
    link_last_page = i.get('href')
    #print(link_last_page)

#получаем кол-во страниц
q_pages = re.search(r'\d+', link_last_page)
count_pages = int(q_pages.group(0))
#print(type(count_pages), count_pages)

#В цикле формируем урл каждой страницы, делаем запрос на каждую страницу, парсим вывод, дописываем результат в словарь
#TODO: реализовать парсинг по датам с проверкой уникальности записей
for i in tqdm(range(2, count_pages + 1)):
    currient_page_url = f'{domain}/{srch}/{tag}/page{i}'
    #print(currient_page_url)
    page_result = requests.get(currient_page_url, headers=headers)
    page_soup = BeautifulSoup(page_result.text, 'html.parser')
    item_tags = page_soup.find_all('a', class_='post__title_link')
    for item in item_tags:
        item_link = item.get('href')
        item_title = item.get_text()
        #print(item_title, item_link)
        items[item_title] = item_link
    time.sleep(3)
#print(items)
with open('parse.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False)


