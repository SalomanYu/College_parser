import os
from typing import NamedTuple
import sqlite3
from datetime import date
from selenium.webdriver.chrome.webdriver import WebDriver
import logging 

from dataclasses import dataclass

FOLDER_PAGES_NAME = 'Paginator'
URL = 'https://russia.ucheba.ru/for-abiturients/college'
DOMAIN = "https://russia.ucheba.ru"

DATABASE_NAME = 'UchebaRU'
COLLEGE_TABLE_NAME = 'Colleges'
COURSE_TABLE_NAME = 'Courses'
LOG_FILENAME = 'LOGGING/parser.log'



os.makedirs("LOGGING", exist_ok=True)

log_file = open(LOG_FILENAME, 'w') 
log_file.close()

logging.basicConfig(filename=LOG_FILENAME, encoding='utf-8', level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING) # Без этого urllib3 выводит страшные большие белые сообщения
logging.getLogger('selenium').setLevel(logging.WARNING)


@dataclass
class AutorizeDriver:
    driver: WebDriver


class EGE(NamedTuple):
    subject: str
    point: int

class TrainingOption(NamedTuple):
    name: str # Например: после 11 класса
    form: str # Форма обучения (очная, заочная)
    budgetPlaces: int
    paidPlaces: int
    budgetAveragePassing: float
    startDate: date
    duration_in_month: int


class College(NamedTuple):
    name: str
    description: str
    url: str
    city: str
    logo:str
    advantages: list 
    averagePassing: float
    averagePrice: int
    budgetPlaces: int
    isState: bool
    hasDorm: bool
    hasMilitaryDepart: bool
    programs: int


class Course(NamedTuple):
    college_id: int
    name: str
    description: str
    program_descr: str
    admissionConditions: str # Условия поступления
    # advantages: str
    # training_options: TrainingOption
    budgetAveragePassing: float
    # paidAveragePassing: float
    budgetPlaces: int
    paidPlaces: int
    startDate: date
    duration: int
    educationForm: str
    cost: int
    url: str
    
    # subjects: tuple[EGE]


class KeyIndications(NamedTuple):
    budget_places: int
    average_price: int
    average_passing: float


class Params(NamedTuple):
    hasMilitaryDepart: bool
    hasDorm: bool
    isState: bool
    city: str


class Benefits(NamedTuple):
    title: str
    description: str


class Connection(NamedTuple):
    cursor: sqlite3.Connection
    db: sqlite3.Cursor

