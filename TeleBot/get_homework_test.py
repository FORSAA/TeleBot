import _io
from typing import BinaryIO

import selenium.types
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep

from datetime import timedelta, datetime
import os
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU')

def get_date(offset: int) -> str:
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
              "декабря"]
    today: datetime = datetime.today()+timedelta(days=offset)

    day_num: str = today.strftime("%d")
    month: str = months[int(today.strftime("%m"))-1]
    weekday: str = today.strftime("%A")
    weekday: str = weekday[0].upper()+weekday[1:]
    year: str = today.strftime("%Y")

    return f'{weekday}, {day_num} {month} {year} г.'

def return_data_handler(return_data: str | BinaryIO) -> str | BinaryIO:
    if (type(return_data) is str):

        if (return_data not in ['screenshot_error', 'login_error']):
            return return_data
        elif (return_data == 'screenshot_error'):
            return 'Ошибка при создании фото. Повторите попытку.'
        elif (return_data == 'login_error'):
            return 'Ошибка при входе в аккаунт. Проверьте ваш логин/пароль и повторите попытку.'

    else:
        return return_data

def login_to_account(login: str, password: str, browser: webdriver.Chrome):

    browser.get("https://e-school.obr.lenreg.ru/authorize/login")
    browser.implicitly_wait(20)

    school_name_selection = browser.find_element(By.CLASS_NAME, "select2__button")
    login_box = browser.find_element(By.NAME, "loginname")
    password_box = browser.find_element(By.NAME, "password")
    login_button = browser.find_element(By.CLASS_NAME, "primary-button")

    school_name_selection.click()
    school_name_input = browser.find_element(By.CLASS_NAME, "select2-search__field")
    school_name_input.send_keys('МОБУ "СОШ "ЦО "Кудрово"')
    browser.find_elements(By.CLASS_NAME, "org-name-data")[1].click()

    login_box.send_keys(login)
    password_box.send_keys(password)

    login_button.click()

def do_after_login_process(browser: webdriver.Chrome):
    continue_button = browser.find_element(By.XPATH, "//button[@title='Продолжить']")
    continue_button.click()
    if (not browser.current_url.endswith('/studentdiary/')):
        browser.get('https://e-school.obr.lenreg.ru/angular/school/studentdiary/')
    sleep(3)

def log_out(browser: webdriver.Chrome):
    out_button = browser.find_element(By.XPATH, "//a[@href='JavaScript:Logout(true);']")
    out_button.click()
    sleep(0.1)
    out_button = browser.find_element(By.XPATH, "//button[@class='btn btn-primary']")
    out_button.click()

def get_exercises(browser: webdriver.Chrome, is_photo:bool, date_offset:int) -> BinaryIO | str:
    date_with_offset = get_date(date_offset)

    exercises_table = browser.find_element(By.XPATH, f"//span[contains(., '{date_with_offset}')]").find_element(By.XPATH,'..').find_element(By.XPATH,'..').find_element(By.XPATH,'..')
    exercises_rows = exercises_table.find_elements(By.XPATH, ".//tr[@class='ng-scope']")

    if (not is_photo):
        formatted_strings = []
        print(f'DEBUG | INFO | GETTING ROWS AND FORMATTING STRINGS.')
        for row in exercises_rows:
            exercise_num = row.find_elements(By.XPATH, ".//td[@class='num_subject ng-binding']")[0].text

            exercise_name_and_time = row.find_elements(By.XPATH,".//td")[1]
            exercise_name = exercise_name_and_time.find_element(By.XPATH, ".//a[@class='subject ng-binding ng-scope']").text
            exercise_time = exercise_name_and_time.find_element(By.XPATH, ".//div[@class='time ng-binding ng-scope']").text

            exercise_task = row.find_element(By.XPATH, ".//td[@class='hidden-mobile wrapper_three_dots']").text

            formatted_strings.append(f'Урок №{exercise_num} | {exercise_name.center(35)} | {exercise_time.center(29)} | {exercise_task}\n')
        return_string = ''.join(formatted_strings)
        return return_string
    else:
        if (exercises_table.screenshot(r'\screenshots\Homework_Screenshot.png')):
            print(f'DEBUG | INFO | RETURNING SCREENSHOT.')
            return 'screenshot'
        else:
            print(f'DEBUG | INFO | SCREENSHOT ERROR. RETURNING.')
            return 'screenshot_error'


def get_homework(auth_data: dict, is_photo: bool, date_offset:int) -> str:
    login, password = auth_data.values()

    browser_options = Options()

    # browser_options.add_argument("--headless=new")
    browser_options.add_argument("--window-size=1000,750")

    browser = webdriver.Chrome(options=browser_options)

    print(f'DEBUG | INFO | OPENING BROWSER. . .')

    browser.implicitly_wait(5)

    try:
        print(f'DEBUG | INFO | LOGGINING. . .')
        login_to_account(login, password, browser)

    except NoSuchElementException:
        print(f'DEBUG | ERROR | LOGIN ERROR. GETTING BACK.')
        return 'login_error'


    sleep(1.2)
    if (browser.current_url.endswith('SecurityWarning.asp')):
        do_after_login_process(browser)

    return_data:str | _io.BufferedReader = get_exercises(browser, is_photo, date_offset)

    log_out(browser)

    browser.close()

    return return_data


if __name__=='__main__':
    exercise_num = "1"
    exercise_name = "Math"
    exercise_time = "10:00, Room 101"
    exercise_task = "Do exercises 1-5"

    # Заголовки
    headers = ["№", "Название", "Время", "Задание"]

    # Форматирование данных
    formatted_data = [
        [exercise_num, exercise_name, exercise_time, exercise_task]
    ]

    # Вывод заголовков
    header_row = [header.center(15) for header in headers]
    header_line = "+"+"+".join(["-"*15]*len(headers))+"+"

    # Вывод данных
    data_rows = []
    for row in formatted_data:
        formatted_row = "|".join([str(item).center(15) for item in row])
        data_rows.append(formatted_row)

    # Вывод таблицы
    table = f"{header_line}\n|{'|'.join(header_row)}|\n{header_line}\n"
    table += "\n".join([f"|{data_row}|" for data_row in data_rows])
    table += f"\n{header_line}"

    print(table)
