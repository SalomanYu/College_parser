import sqlite3
import os

from config import Connection, College, Course, logging 


def connect_to_db(name) -> Connection:
    os.makedirs(name='SQL', exist_ok=True)
    db = sqlite3.connect(f'SQL/{name}.db')
    cursor = db.cursor()
    return cursor, db


# connect_to_db('hello')
def create_table_for_college(db_name: str, table_name: str) -> None:
    cursor, db = connect_to_db(db_name)

    pattern = f"""
        CREATE TABLE IF NOT EXISTS {table_name}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            название_колледжа VARCHAR(255),
            описание TEXT,
            ссылка VARCHAR(255),
            город VARCHAR(100),
            логотип VARCHAR(255),
            преимущества TEXT,
            проходной_балл_бюджет REAL,
            средняя_стоимость_в_год INTEGER,
            бюджетные_места INTEGER,
            государственный BOOLEAN,
            есть_общежитие BOOLEAN,
            есть_военная_кафедра BOOLEAN,
            course_id INTEGER
        )
    """
    cursor.execute(pattern)
    db.commit()
    db.close()


def add_college(db_name: str, table_name: str, data: College) -> None:
    cursor, db = connect_to_db(db_name)
    pattern = f"""
        INSERT INTO {table_name}(
            название_колледжа,
            описание,
            ссылка,
            город,
            логотип,
            преимущества,
            проходной_балл_бюджет ,
            средняя_стоимость_в_год,
            бюджетные_места,
            государственный ,
            есть_общежитие,
            есть_военная_кафедра,
            course_id
        ) VALUES({','.join('?' for i in range(len(data)))})
    """
    cursor.execute(pattern, data)
    db.commit()
    db.close()
    # print(f'Добавлен колледж - {data.name}')
    logging.info("Added college - %s", data.name)


def create_table_for_course(db_name: str, table_name: str) -> None:
    cursor, db = connect_to_db(db_name)

    pattern = f"""
        CREATE TABLE IF NOT EXISTS {table_name}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            college_id INTEGER,
            название_курса VARCHAR(255),
            описание TEXT,
            программа_курса TEXT,
            условия_для_поступления VARCHAR(255),
            проходной_балл_бюджет REAL,
            бюджетные_места INTEGER,
            платные_места INTEGER,
            дата_начала VARCHAR(20),
            продолжительность_в_месяцах INTEGER,
            форма_обучения VARCHAR(30),
            стоимость_в_год INTEGER,
            ссылка VARCHAR(255)
        )
    """
    cursor.execute(pattern)
    db.commit()
    db.close()


def add_course(db_name: str, table_name: str, data: Course) -> None:
    cursor, db = connect_to_db(db_name)
    pattern = f"""
        INSERT INTO {table_name}(
            college_id,
            название_курса,
            описание,
            программа_курса,
            условия_для_поступления,
            проходной_балл_бюджет,
            бюджетные_места,
            платные_места,
            дата_начала,
            продолжительность_в_месяцах ,
            форма_обучения,
            стоимость_в_год,
            ссылка
        ) VALUES({','.join('?' for i in range(len(data)))})
    """
    cursor.execute(pattern, data)
    db.commit()
    db.close()
    # print(f'Добавлен курс - {data.name}')
    logging.info("Added course - %s", data.name)

