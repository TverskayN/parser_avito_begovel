import requests
from bs4 import BeautifulSoup
import csv


# План:
# 1. Выясняем количество страниц
# 2. Формируем список урлов на страницы выдачи
# 3. Собираем данные

def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find("div", class_="pagination-pages").find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split("&")[0]
    return int(total_pages)

def write_csv(data):
    with open('avito_begovel.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['title'],
                          data['price'],
                          data['metro'],
                          data['url']) )



def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='js-catalog_serp').find_all('div', class_='item__line')

    for ad in ads:
        # title, price, metro, url
        name = ad.find('div', class_='description').find('h3').text.strip().lower()
        if 'беговел' in name:
            try:
                title = ad.find('div', class_='description').find('h3').text.strip()
            except:
                title = ''

            try:
                url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
            except:
                url = ''

            try:
                price = ad.find('span', class_='snippet-price').text.strip()
            except:
                price = ''

            try:
                metro = ad.find('span', class_='item-address-georeferences-item__content').text.strip()
            except:
                metro = ''

            data = {'title': title,
                    'price': price,
                    'metro': metro,
                    'url': url}
            write_csv(data)
        else:
            continue


def main():
    url = 'https://www.avito.ru/ekaterinburg/tovary_dlya_detey_i_igrushki/kupit-velosipedy_i_samokaty-ASgBAgICAUT~AaCGAQ?q=%D0%B1%D0%B5%D0%B3%D0%BE%D0%B2%D0%B5%D0%BB&p=5'
    base_url = 'https://www.avito.ru/ekaterinburg/tovary_dlya_detey_i_igrushki/kupit-velosipedy_i_samokaty-ASgBAgICAUT~AaCGAQ?'
    page_part = '&p='
    query_part = 'q=%D0%B1%D0%B5%D0%B3%D0%BE%D0%B2%D0%B5%D0%BB'
    total_pages = get_total_pages(get_html(url))
    for i in range(1, total_pages + 1):
        url_gen = base_url + query_part + page_part + str(i)
        html = get_html(url_gen)
        get_page_data(html)


# if __main__ == "__main__":
main()
