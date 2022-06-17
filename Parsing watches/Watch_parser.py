# Parser для сбора полной информации из всех карточек товара по категории "часы" с последующим выводом в csv-файл с сайта http://parsinger.ru/html/index1_page_1.html
import csv
import requests
from bs4 import BeautifulSoup

# создаём заголовки
with open('res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        'Наименование', 'Артикул', 'Бренд', 'Модель', 'Тип', 'Технология экрана',
        'Материал корпуса', 'Материал браслета', 'Размер', 'Сайт производителя',
        'Наличие', 'Цена', 'Старая цена', 'Ссылка на карточку с товаром'])

# создаём список ссылок на 4 страницы с часами
url = 'http://parsinger.ru/html/index1_page_1.html'
response = requests.get(url=url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')
pages = ['http://parsinger.ru/html/' + x['href'] for x in soup.find('div', class_='pagen').find_all('a')]

# итерируемся по страницам с часами и создаем список ссылок на 8 товаров на текущей странице
for x in pages:
    response = requests.get(url=x)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    links = ['http://parsinger.ru/html/' + x['href'] for x in soup.find_all('a', class_='name_item')]

    # итерируемся по ссылкам на модели часов и работаем с каждой карточкой товара отдельно
    for i in links:
        url = i
        response = requests.get(url=i)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        # создаём списки данных под колонки
        name = [x.text.strip() for x in soup.find('p', id='p_header')]
        article = [x.text.split(':')[1] for x in soup.find('p', class_="article")]
        brand_site = [x.text.split('\n') for x in soup.find_all('ul', id='description')]
        in_stock = [x.text.split(':')[1] for x in soup.find('span', id='in_stock')]
        price = [x.text.split(' ')[0] for x in soup.find_all('span', id='price')]
        old_price = [x.text.split(' ')[0] for x in soup.find('span', id='old_price')]
        link = [i]

        # разбиваем данные в подходящий формат
        for name, article, brand_site, in_stock, price, old_price, link in zip(name, article, brand_site, in_stock, price, old_price, link):
            result = []
            flatten = name, article, [x.split(':')[1].strip() for x in brand_site if x], in_stock, price, old_price, link
            for x in flatten:
                if isinstance(x, list):
                    result.extend(x)
                else:
                    result.append(x)

            # записываем данные в csv-файл
            with open('res.csv', 'a', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(result)