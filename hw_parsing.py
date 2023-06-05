import json
import requests
from fake_headers import Headers
import bs4
import re
from time import sleep
import time
from pprint import pprint

start = time.time()
hh_dict = {}

for i in range(8): # количество страниц с вакансиями по 20 штук(обойдем все страницы)
    headers = Headers(browser='firefox', os='win')
    headers_data = headers.generate()
    main_page_html = requests.get(
        f'https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=python+django+flask&excluded_text=&area=2&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page={i}',
        headers=headers_data).text
    main_page_soup = bs4.BeautifulSoup(main_page_html, 'lxml')
    # pattern = r'(Москва)|(Санкт\-Петербург)+?'  # регуляркой

    div_article_list_tag = main_page_soup.find('div', class_='HH-MainContent HH-Supernova-MainContent')
    article_tags = div_article_list_tag.find_all(class_='vacancy-serp-item-body')
    for article_tag in article_tags:

        h3_tag = article_tag.find('h3')
        title = h3_tag.text

        a_tag = h3_tag.find('a')

        link = a_tag['href']

        salary_tag = article_tag.find('span', class_="bloko-header-section-3")

        company_tag = article_tag.find('div', class_='vacancy-serp-item-company')
        a_company_tag = company_tag.find('a')
        company_name = a_company_tag.text
        location_tag = company_tag.find('div')
        # city = re.search(pattern, location_tag.text)[0] # Если регуляркой
        city = \
            location_tag.find(class_="bloko-text", attrs={'data-qa': "vacancy-serp__vacancy-address"}).text.split(',')[
                0]
        try:
            hh_dict.update(
                {title: [{'Ссылка': link, 'Зарплата': salary_tag.text, 'Компания': company_name, 'Город': city}]})
        except AttributeError:
            hh_dict.update(
                {title: [{'Ссылка': link, 'Зарплата': 'Не указана', 'Компания': company_name, 'Город': city}]})

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(hh_dict, file, ensure_ascii=False, indent=3)


