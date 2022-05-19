import csv
import requests
from bs4 import BeautifulSoup

with open('../../Парсинг/HDD-descr_to_csv/res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        'Наименование', 'Бренд', 'Форм-фактор', 'Ёмкость', 'Объём буф. памяти', 'Цена'])

url = 'http://parsinger.ru/html/index4_page_1.html'
response = requests.get(url=url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')
pagen = ['http://parsinger.ru/html/' + x['href'] for x in soup.find('div', class_='pagen').find_all('a')]

for i in pagen:
    url = i
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    name = [x.text.strip() for x in soup.find_all('a', class_='name_item')]
    description = [x.text.split('\n') for x in soup.find_all('div', class_='description')]
    price = [x.text for x in soup.find_all('p', class_='price')]

    for item, descr, price in zip(name, description, price):
        result = []
        flatten = item, [x.split(':')[1].strip() for x in descr if x], price

        for x in flatten:
            if isinstance(x, list):
                result.extend(x)
            else:
                result.append(x)
        print(result)

        with open('../../Парсинг/HDD-descr_to_csv/res.csv', 'a', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(result)
print('Файл res.csv создан')