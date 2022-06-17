from bs4 import BeautifulSoup
import requests
import csv

url_list = list()
rows = list()

header = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Тип',
          'Технология экрана', 'Материал корпуса', 'Материал браслета',
          'Размер', 'Сайт производителя', 'Наличие', 'Цена',
          'Старая цена', 'Ссылка на карточку с товаром']
rows.append(header)

for i in range(1, 5):
    url = f'http://parsinger.ru/html/index1_page_{i}.html'
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    url_list.extend([link['href'] for link in soup.find_all('a', class_="name_item")])
print(url_list)
for url in url_list:
    element_url = 'http://parsinger.ru/html/' + url
    response = requests.get(url=element_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    rows.append([soup.find('p', id='p_header').text,
                 soup.find('p', class_='article').text.split(': ')[1],
                 soup.find('li', id='brand').text.split(': ')[1],
                 soup.find('li', id='model').text.split(': ')[1],
                 soup.find('li', id='type').text.split(': ')[1],
                 soup.find('li', id='display').text.split(': ')[1],
                 soup.find('li', id='material_frame').text.split(': ')[1],
                 soup.find('li', id='material_bracer').text.split(': ')[1],
                 soup.find('li', id='size').text.split(': ')[1],
                 soup.find('li', id='site').text.split(': ')[1],
                 soup.find('span', id='in_stock').text.split(': ')[1],
                 soup.find('span', id='price').text,
                 soup.find('span', id='old_price').text,
                 element_url, ])
print(rows)
with open('watch_all.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')

    # Запись сразу всего файла, в result содержится список строк, которые также представлены списком элементов
    writer.writerows(rows)

print('Файл watch_all.csv создан')