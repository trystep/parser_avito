import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


# Получаем количество страниц пагинации
def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('div', class_='pagination-pages clearfix').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def write_csv(data):
    with open('avito.csv', 'a', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'], data['price'], data['metro'], data['url']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find('div', class_='snippet-list js-catalog_serp').find_all('div', 'item__line')
    for ad in ads:

        name = ad.find('a', class_='snippet-link').text.lower()

        if 'htc' in name:

            try:
                title = ad.find('a', class_='snippet-link').text
            except:
                title = ''
            try:
                price = ad.find('div', class_="snippet-price-row").text.strip()
            except:
                price = ''
            try:
                metro = ad.find('span', class_='item-address-georeferences-item__content').text.strip()
            except:
                metro = ''
            try:
                url = 'https://www.avito.ru' + ad.find('a', class_='snippet-link').get('href')
            except:
                url = ''
            data = {'title': title,
                    'price': price,
                    'metro': metro,
                    'url': url}
            write_csv(data)


def main():
    url = 'https://www.avito.ru/moskva/telefony?q=htc&p=100'
    base_url = 'https://www.avito.ru/moskva/telefony?'
    page_part = 'p='
    query_part = 'q=htc&p'
    total_pages = get_total_pages(get_html(url))
    # for i in range(total_pages):
    for i in range(2):
        url_gen = base_url + query_part + page_part + str(i)
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()
