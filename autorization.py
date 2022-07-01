from time import sleep
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from config import FOLDER_PAGES_NAME, URL

from config import AutorizeDriver


def autorize() -> AutorizeDriver:
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get('https://russia.ucheba.ru/auth/password?redirect=%2F')
    driver.implicitly_wait(10)

    input_log, input_pass = driver.find_elements(By.XPATH, "//input[@class='TextFieldstyles__Input-sc-tfn43g-1 jREPon']")
    input_log.send_keys('rosya-8@yandex.ru')
    input_pass.send_keys('helloworld')
    input_pass.send_keys(Keys.ENTER)
    driver.implicitly_wait(10)
    return driver


def save_html(filename: str, content: str) -> None:
    with open(filename, 'w') as file:
        file.write(content)


def save_all_pages(last_page_num_in_url: int, driver: AutorizeDriver) -> None:
    PAGE_COUNT = 0    
    os.makedirs(FOLDER_PAGES_NAME, exist_ok=True)
    # Сохраняем первую страницу отдельно, потому что 
    # у нее нет приставки с номером страницы в конце, в отличие от других страниц
    sleep(1)
    driver.get(URL)
    save_html(f'{FOLDER_PAGES_NAME}/page_{str(PAGE_COUNT/10)}.html', content=driver.page_source) 

    while PAGE_COUNT < last_page_num_in_url:
        PAGE_COUNT += 10
        driver.get(URL + f"?s={str(PAGE_COUNT)}") # Подключаемся к новой странице
        driver.implicitly_wait(5) # Ждём пока подгрузится контент
        print(driver.current_url)
        filename = f'{FOLDER_PAGES_NAME}/page_{str(PAGE_COUNT//10)}.html'
        save_html(filename, content=driver.page_source) #  Сохраняем в отдельный файлик


if __name__ == "__main__":
    save_all_pages(last_page_num_in_url=2520, driver=autorize())
