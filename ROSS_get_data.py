import pandas as pd
import requests
import re
from time import sleep
import html
import unicodedata
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def get_data(number_of_pages):
    all_data = []
    all_prices = []

    for page_number in range(1, number_of_pages + 1):
        print(f'Getting data from page number {page_number}')

        http_address = f'https://www.rossmann.pl/kategoria/twarz/pielegnacja-twarzy/serum,9225?CategoryId=9225&Page={page_number}&PageSize=96'
        response = requests.get(http_address)
        content = response.content.decode("utf-8")
        content = html.unescape(content)
        content = unicodedata.normalize('NFKD', content)
        soup = BeautifulSoup(content, 'html.parser')

        data = soup.find_all('a', {'class': 'tile-product__name'})
        price = soup.find_all('div', {'class': 'tile-product__price'})
        print(data, type(data))
        print(price, type(price))

        all_data.extend(data)
        all_prices.extend(price)

        sleep(5)

    print(len(all_data))
    print(len(all_prices))

    a = all_prices[0]
    all_prices = [i for i in all_prices if (i != a)]
    print(len(all_data))
    print(len(all_prices))

    df = pd.DataFrame([all_data, all_prices]).T

    return df


def split_data(all_data):
    # split data to columns
    links = []
    companies = []
    descriptions = []
    prices = []
    sizes = []
    i = 0

    # split data using regex
    for cream in all_data[0]:
        link = re.findall(r'href="(.*?)"><', str(cream), re.DOTALL)
        company = re.findall(r'<strong>(.*?)</strong>', str(cream), re.DOTALL)
        description = re.findall(r'<span>(.*?)<span', str(cream), re.DOTALL)
        size = re.findall(r'class="text-nowrap">(\d.*?)</span>', str(cream), re.DOTALL)
        if not size:
            size = 'EMPTY'
        # print(i, size)
        i += 1

        links.extend(link)
        companies.extend(company)
        descriptions.extend(description)
        sizes.extend(size)

    for money in all_data[1]:
        if money:
            price = money.get_text()
            price = (re.findall(r'.*?zł', str(price), re.DOTALL))[0]
            # print(price)
            prices.append(str(price))

    # split company to brand and series
    print(len(links))
    print(len(companies))
    print(len(descriptions))
    print(len(prices))
    print(len(sizes))

    brand = []
    series = []
    a = []
    for i in range(len(companies)):
        a = companies[i].split('<!-- --> <!-- -->')

        # check which brands do not have series
        if len(a) < 2:
            brand.append(a[0].replace('<!-- --> ', ''))
            series.append('@NO_NAME@')
        else:
            # print(a, a[0], a[1])
            brand.append(a[0])
            series.append(a[1])

    # create df
    df_all_data = pd.DataFrame({'link': links,
                                'brand': brand,
                                'series': series,
                                'size': sizes,
                                'price': prices,
                                'info': descriptions})

    return df_all_data



