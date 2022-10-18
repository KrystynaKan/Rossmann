import pandas as pd
import requests
import re
from time import sleep
import html
import unicodedata
from bs4 import BeautifulSoup

df_ross = pd.read_csv("full_serum_database.csv")


# ingredients_list = []
# ingredients = ''
# link = df_ross['link'][9]
# http_address = f'https://www.rossmann.pl{link}'
# response = requests.get(http_address)
# content = response.content.decode()
# content = html.unescape(content)
# content = unicodedata.normalize('NFKD', content)
# soup = BeautifulSoup(content, 'html.parser')
# print(link)
# print(soup)
#
# # try:
# #   soup.find('div', {"class":"collapse fade py-2 "}).find('span', {"class":"csC8F6D76"}).get_text()
# # except:
# #   ingredients_list.append('BRAK SKŁADU - BŁĄD')
# # else:
# ingredients = soup.find('div', {"class":"collapse fade py-2"}).find('span', {"class":"csC8F6D76"}).get_text()
# ingredients_list.append(ingredients)
#
#
# print(ingredients_list)



def add_ingredients(df):
    # download list of ingredients from specific serum sites
    ingredients_list = []
    ingredients = ''

    for i in df['link']:
        print(f'Getting ingredients from LINK {i}')
        http_address = f'https://www.rossmann.pl{i}'
        response = requests.get(http_address)
        content = response.content.decode("utf-8")
        content = html.unescape(content)
        content = unicodedata.normalize('NFKD', content)
        soup = BeautifulSoup(content, 'html.parser')
        sleep(1)

        try:
            soup.find('div', {"class": "collapse fade py-2"}).find('span', {"class": "csC8F6D76"}).get_text()
        except:
            ingredients_list.append('BRAK SKŁADU - BŁĄD')
        else:
            ingredients = soup.find('div', {"class": "collapse fade py-2"}).find('span', {"class": "csC8F6D76"}).get_text()
            ingredients_list.append(ingredients)

    df['ingredients'] = pd.Series(ingredients_list)

    return df

df_ross_ing = add_ingredients(df_ross)
df_ross_ing.to_csv('full_serum_with_ing.csv', index=False)
print(df_ross_ing)