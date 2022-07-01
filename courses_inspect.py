import os
import re
import requests
from bs4 import BeautifulSoup

from config import COURSE_TABLE_NAME, DATABASE_NAME, DOMAIN, Course, TrainingOption
import database

def parse_programs(url: str, college_id: int) -> None:
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')

    all_programs = soup.find_all('section', class_='search-results-info-item')
    for program in all_programs:
        program_url = DOMAIN + program.a['href']
        about_program_soup = BeautifulSoup(requests.get(program_url).text, 'lxml')

        title = program.h3.text.strip()
        # budgetPlaces = _getBudgetPlaces(program)
        # budgetAveragePassing = _get_budgetAveragePassing(program)
        cost = _getCost(program)
        descr = _getDescription(about_program_soup)
        admissionConditions = _getAdmissionConditions(about_program_soup)
        program_descr = _getProgramDescr(about_program_soup)
        # Вариант обучения после 11 класса или после 9 класса
        # try:
        training_option = _getTrainingOptions(about_program_soup)
        database.add_course(db_name=DATABASE_NAME, table_name=COURSE_TABLE_NAME, data=Course(college_id,title, descr, program_descr, admissionConditions, training_option.budgetAveragePassing, training_option.budgetPlaces, training_option.paidPlaces, training_option.startDate, training_option.duration_in_month, training_option.name, cost, program_url))


def _getCost(program: BeautifulSoup) -> int:
    try:
        cost = program.find('section', class_='search-results-options-item sro-price_interval col-sm-5 col-xs-4').find('div', class_='big-number-h2 price-year').text.strip()
        #  Регулярка вытаскивает цифры из "от 62 000 р./год"  шаблонов
        return int(''.join(re.findall('\d+', cost))) 
    except:
        return 0


def _getDescription(about_program: BeautifulSoup) -> str:
    descr = ''
    sections = about_program.find_all('section', class_='mb-section-large')
    for section in sections:
        if "О программе" in section.text:
            descr = section.p.text.strip()
    return descr


def _getAdmissionConditions(about_program: BeautifulSoup) -> str:
    admission = ''
    sections = about_program.find_all('section', class_='mb-section-large')
    for section in sections:
        if "Условия поступления" in section.text:
            try:
                admission = (item.text for item in section.ul.find_all('li'))
            except AttributeError:
                # return about_program.h1.text.strip()
                admission = (item.text for item in section.find_all('h4'))
    return '|'.join(admission)


def _getProgramDescr(about_program: BeautifulSoup) -> str:
    program = ''
    sections = about_program.find_all('section', class_='mb-section-large')
    for section in sections:
        if "Особенности программы" in section.text:
            program = section.p.text.strip()
    return program


def _getTrainingOptions(about_program: BeautifulSoup) -> TrainingOption:
    try:
        name = about_program.find('ul', class_='nav nav-tabs nav-tabs-underline mb-25').find('li', class_='active').text.strip()
    except:
        name = 'Очная'
    sections = about_program.find_all('section', class_='mb-section-large')
    for section in sections:
        if "Варианты обучения" in section.text:
            result_row = section.find_all('div', class_='program-table__row')[-1]
            form = result_row.find('div', class_='program-table__title').text.strip()
            try:
                budgetAveragePassing = float(re.findall('\d.+', result_row.find_all('div', class_='program-table__col')[1].text.strip())[0])
            except:
                budgetAveragePassing = 0
            try:
                budgetPlaces = int(result_row.find_all('div', class_='program-table__col')[3].text.strip().split('\n')[-1].strip().replace('/ ', ''))
            except ValueError:
                budgetPlaces = 0
            try:
                paidPlaces = result_row.find_all('div', class_='program-table__col')[3].find('span', class_='text-gray').text.strip()
            except AttributeError:
                paidPlaces = 0
            try:
                startDate = result_row.find_all('div', class_='program-table__col')[-2].text.strip().split('\n')[-1]
            except:
                startDate = '1 сен.'
            try:
                duration_in_months = int(re.findall('\d+', result_row.find_all('div', class_='program-table__col')[-1].text.strip())[0])
            except:
                duration_in_months = 12 * 4
            return(TrainingOption(name, form, budgetPlaces, paidPlaces,  budgetAveragePassing, startDate, duration_in_months)) 


if __name__ == "__main__":
    database.create_table_for_course(db_name=DATABASE_NAME, table_name=COURSE_TABLE_NAME)
    # print(parse_programs('https://russia.ucheba.ru/uz/17842/programs'))