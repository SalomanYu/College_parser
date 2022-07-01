import os
import codecs
import requests
from bs4 import BeautifulSoup

import config
from config import College, KeyIndications, Benefits, Params

from courses_inspect import parse_programs
from database import create_table_for_college, add_college, create_table_for_course


def read_html(filename: str) -> BeautifulSoup:
    html = codecs.open(filename, 'r')
    soup = BeautifulSoup(html.read(), 'lxml')
    return soup


def collect_page(soup: BeautifulSoup) -> None:
    colleges = soup.find_all('div', class_='search-results-row row')
    for item in colleges:
        url = config.DOMAIN + item.find('h2', class_='search-results-title').a['href']
        college = parse_college(url)
        add_college(db_name=config.DATABASE_NAME, table_name=config.COLLEGE_TABLE_NAME, data=college)
        parse_programs(url + '/programs', college_id=college.programs)


def parse_college(college_url: str) -> College:
    print(college_url)
    req = requests.get(college_url)
    soup = BeautifulSoup(req.text, 'lxml')

    name = soup.find('h1', class_='head-announce__title').text.strip()
    logo = soup.find('img', class_='head-announce__img logo-uz')['src']    
    descr = _get_description(soup)
    programs = int(college_url.split('/')[-1])
    benefits = _get_adverages(college_url)
    military, dorm, state, city = _get_params(soup) 
    budget_places, average_price, average_passing = _get_key_indications(soup)

    return College(name, descr, college_url, city, logo, benefits, average_passing, average_price, budget_places, state, dorm, military, programs)


def _get_key_indications(soup: BeautifulSoup) -> KeyIndications:
    budget_places = 0
    average_price = 0.0
    average_passing = 0.0

    key_indications = soup.find_all('dl', class_='col-xs-12 col-md-4 key-indicators__item')
    for indication in key_indications:
        key_descr = indication.find('div', class_='key-indicators__desc').text.strip()
        key_val = indication.find('dd', class_='key-indicators__val').text.strip()

        if "Бюджетныеместа" in key_descr:
            budget_places = int(key_val.replace("&nbsp", ""))
        elif "Средний проходнойбалл" in key_descr:
            average_passing = float(key_val)
        elif "Сред. стоимостьза год, тыс. руб." in key_descr:
            average_price = int(key_val) * 1000

    return KeyIndications(budget_places, average_price, average_passing)


def _get_description(soup: BeautifulSoup) -> str:
    descr = ''
    sections = soup.find_all('section', class_='mb-section-large')
    for section in sections:
        if "Об учебном заведении" in section.text:
            descr = section.p.text
    return descr


def _get_programs(soup: BeautifulSoup) -> set[str]:
    programs = [config.DOMAIN + link.a['href'] for link in soup.find_all('li', class_='program-list__row')]
    if programs:
        return ' | '.join(programs)
    programs = (config.DOMAIN + link['href'] for link in soup.find_all('a', class_='program-card__heading-link'))
    return ' | '.join(programs)


def _get_params(soup: BeautifulSoup) -> Params:
    params = soup.find('ul', class_='params-list').find_all('li')
    city = params[0].text.strip()
    isState = False
    hasDorm = False
    hasMilitaryDepart = False

    for item in params:
        if 'Государственный' in item.text:
            isState = True
        elif 'общежитие' in item.text:
            hasDorm = True
        elif 'кафедра' in item.text:
            hasMilitaryDepart = True
    return Params(hasMilitaryDepart, hasDorm, isState, city)


def _get_adverages(url: str) -> list[Benefits]:
    adver_url = url + '/about#benefits'
    req = requests.get(adver_url)
    soup = BeautifulSoup(req.text, 'lxml')
    titles = [title.text.strip() for title in soup.find_all('div', class_='grid-heading')]
    descrs = [descr.p.text.strip().replace(u'\xa0', u'') for descr in soup.find_all('div', class_='grid__item grid__item_lg-4 grid__item_sm-6')]
    if descrs:
        if descrs[0] == '':
            descrs = [descr.find_all('div')[-1].text.strip() for descr in soup.find_all('div', class_='grid__item grid__item_lg-4 grid__item_sm-6')]

    result = []
    for item in range(len(titles)):
        data = ';'.join(Benefits(title=titles[item], description=descrs[item]))
        result.append(data)
    return ' | '.join(result)


if __name__ == "__main__":
    create_table_for_college(db_name=config.DATABASE_NAME, table_name=config.COLLEGE_TABLE_NAME)
    create_table_for_course(db_name=config.DATABASE_NAME, table_name=config.COURSE_TABLE_NAME)
    
    for file in os.listdir(config.FOLDER_PAGES_NAME):
        soup = read_html(filename=os.path.join(config.FOLDER_PAGES_NAME, file))
        collect_page(soup)
