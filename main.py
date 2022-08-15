import json
import time

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from config import cookies, headers

link = 'https://astrahan.vseinstrumenti.ru/instrument/akkumulyatornyj/perforatory/'


def get_data():
    products_list = []
    for pagination in range(1, 11):
        if pagination == 1:
            response = requests.get(link + '#goods', headers=headers, cookies=cookies)
        else:
            response = requests.get(link + f'page{pagination}/#goods', cookies=cookies, headers=headers)

        print(f'Start page : {pagination} ')

        with open('index.html', 'w') as file:
            file.write(response.text)

        with open('index.html', encoding='utf-8') as file:
            page = file.read()

        soup = BeautifulSoup(page, 'lxml')

        products_row = soup.find('div', class_='listing-grid -rows').find_all('div', class_='product-row grid-item')

        for element, product in enumerate(products_row, 1):
            all_products_info = {}

            info_products_left = product.find(class_='left')
            code_items = info_products_left.find(class_='wtis-id').text.split(':')[1].strip()
            link_items = 'https://astrahan.vseinstrumenti.ru' + info_products_left.find(class_='image').find('a').get(
                'href')
            all_products_info['Код инструмента'] = code_items
            all_products_info["Ссылка на инструмент"] = link_items

            info_products_middle = product.find(class_='middle')

            name_and_description_product = info_products_middle.find('a').text.strip()
            all_products_info["Описание и наименование инструмента"] = name_and_description_product

            if info_products_middle.find(class_='advantages'):
                all_products_info['Дополнительные сведения'] = info_products_middle.find(class_='advantages').text

            if info_products_middle.find(class_='rating-wrapper').find('a'):
                amount_reviews = info_products_middle.find(class_='rating-wrapper').find('a').get('title').strip()[0]
                all_products_info['Колличество отзывов'] = amount_reviews

            type_of_acc = info_products_middle.find(class_='features').find('p').find('span').text
            all_products_info['Тип аккумулятора'] = type_of_acc

            info_products_right = product.find(class_='right')

            price = info_products_right.find(class_='price').find('span').text

            all_products_info['Цена'] = price

            if info_products_right.find(class_='promo'):
                price_without_discount = info_products_right.find(class_='old-price').find('span').text
                discount = info_products_right.find(class_='discount').find('span').text

                all_products_info['Цена без скидки'] = price_without_discount
                all_products_info["Скидка"] = discount

            products_list.append(all_products_info)
            print(f'Element number {element} was loading!!!')

        print('#' * 15)
        print(f'Page number {pagination} was loaded!!!')

    with open('product.json', 'w') as file:
        json.dump(products_list, file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == '__main__':
    main()
