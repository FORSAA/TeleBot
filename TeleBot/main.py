#  IMPORTS
from datetime import timedelta, datetime

from typing import BinaryIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import telebot
from telebot.types import CallbackQuery
from telebot.util import quick_markup
from telebot import types

from time import sleep

import random
import pyodbc
import os
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU')

# FAST TO USE CODE
"""

local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

"""

#  GLOBALS

bot: telebot.TeleBot = telebot.TeleBot('6070580163:AAFKRJt7nnNWL__vunKkFVz1r1IZ6xDJgXI')

user_states = {}
separator = ':'

pages = {
    'start':{'message_text':'Добро пожаловать в главное меню телеграмм бота! Используйте кнопки ниже для навигации.',
             'markup_data':{
                 'Смена Логина/Пароля':{'callback_data':'auth_data_edit'},
                 'Как пользоваться?':{'callback_data':'help'},
                 'Получить Д/З':{'callback_data':'get_homework'},
             }
             },
    'auth_data_edit':{'message_text':f'Тут вы можете поменять ваш логин и пароль для автоматической работы бота.\n\nЧтобы сменить ваш пароль, напишите его в следующем виде без пробелов: "Логин{separator}Пароль"\n\nP.S: Отправляя свои данные авторизации вы делаете это добровольно и соглашаетесь с их обработкой."',
                      'markup_data':{
                            '« Вернуться в главное меню':{'callback_data':'menu'},
                      }
                      },
    'help_page':{'message_text':'Как пользоваться ботом? Очень легко!\n\nДля начала использования бота достаточно ввести логин и пароль от сайта ГИССОЛО на странице "Смена логина/пароля". (Кнопка "Смена Логина/Пароля"). \n \n После выполнения этого шага вы можете перейти по пути "Получить Д/З->Текст" и выбрать дату. Ваш запрос будет обработан.',
                 'markup_data':{
                        '« Вернуться в главное меню':{'callback_data':'menu'}
                 }
                 },
    'get_homework':{'message_text':'Выберите в каком формате бот должен прислать вам домашнее задание.',
                    'markup_data':{
                        'Текст':{'callback_data':'homework_wish_text'},
                        'Фотография':{'callback_data':'homework_wish_photo'}
                    }

    },

    'debug_page':{'message_text':str(),
                  'markup_data':{
                      '« Вернуться в главное меню':{'callback_data':'menu'}
                  }
                  }

}

#  ======FUNCTIONS======

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

# ====GETTING HOMEWORK FUNCTIONS========

def return_data_handler(return_data: str|BinaryIO) -> str|BinaryIO:
    if (type(return_data) is str):

        if (return_data not in ['screenshot_error', 'login_error']):
            return return_data
        elif (return_data=='screenshot_error'):
            return 'Ошибка при создании фото. Повторите попытку.'
        elif (return_data=='login_error'):
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


def get_exercises(browser: webdriver.Chrome, is_photo: bool, date_offset: int) -> BinaryIO|str:
    date_with_offset = get_date(date_offset)

    exercises_table = browser.find_element(By.XPATH, f"//span[contains(., '{date_with_offset}')]").find_element(
        By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
    exercises_rows = exercises_table.find_elements(By.XPATH, ".//tr[@class='ng-scope']")

    if (not is_photo):
        formatted_strings = []
        print(f'DEBUG | INFO | GETTING ROWS AND FORMATTING STRINGS.')
        for row in exercises_rows:
            exercise_num = row.find_elements(By.XPATH, ".//td[@class='num_subject ng-binding']")[0].text

            exercise_name_and_time = row.find_elements(By.XPATH, ".//td")[1]
            exercise_name = exercise_name_and_time.find_element(By.XPATH,
                                                                ".//a[@class='subject ng-binding ng-scope']").text
            exercise_time = exercise_name_and_time.find_element(By.XPATH,
                                                                ".//div[@class='time ng-binding ng-scope']").text

            exercise_task = row.find_element(By.XPATH, ".//td[@class='hidden-mobile wrapper_three_dots']").text

            formatted_strings.append(
                f'Урок №{exercise_num} | {exercise_name.center(35)} | {exercise_time.center(29)} | {exercise_task}\n')
        return_string = ''.join(formatted_strings)
        return return_string
    else:
        if (exercises_table.screenshot(os.getcwd()+r'\screenshots\Homework_Screenshot.png')):
            with open(os.getcwd()+r'\screenshots\Homework_Screenshot.png', 'rb') as screenshot:
                print(f'DEBUG | INFO | OPENING AND RETURNING SCREENSHOT FILE.')
                return screenshot
        else:
            print(f'DEBUG | INFO | SCREENSHOT ERROR. RETURNING.')
            return 'screenshot_error'


def get_homework(auth_data: dict, is_photo: bool, date_offset: int) -> str:
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

    return_data: str|BinaryIO = get_exercises(browser, is_photo, date_offset)

    log_out(browser)

    browser.close()

    return return_data

# =====ANOTHER FUNCTIONS======
def test_auth_data_saver(message:types.Message, to_save_auth_data:list) -> None:
    user_id = message.chat.id

    auth_data = {}
    login, password = to_save_auth_data
    auth_data['login'] = login
    auth_data['password'] = password
    user_states[user_id]['auth_data'] = auth_data
    user_states[user_id]['auth_state'] = 1
    print(f'DEBUG | INFO | {user_id} GOT AUTH.')


def add_to_states(user_id:int):
    default_user_states = {
        'auth_state':0,
        'menu_state':'',
        'bot_last_message':None,
        'bot_last_error_message':None,
        'auth_data':{}
    }
    user_states[user_id] = default_user_states


def markup_generator(page: dict, row_width: int = 2):
    return quick_markup(page['markup_data'], row_width=row_width)


def auth_data_reader(message: types.Message):
    user_id = message.chat.id
    local_bot_last_message:types.Message = user_states[user_id]['bot_last_message']
    local_bot_last_error_message: types.Message = user_states[user_id]['bot_last_error_message']

    print(f'DEBUG | INFO | AUTH_DATA_EDIT REQUEST BY {user_id}')

    bot.delete_message(user_id, message.message_id)
    bot.delete_message(user_id, local_bot_last_message.message_id)

    if (separator not in message.text):
        send_error(message, f'Не обнаружен знак-делитель.(" {separator} ")', 'auth_data_reader')
    else:
        auth_data = message.text.split(separator)
        if (' ' in auth_data):
            send_error(message, f'Обнаружен лишний пробел.(" {separator} ")', 'auth_data_reader')
        else:
            test_auth_data_saver(message, auth_data)
            #  TODO: Auth_data saver function
            send_succsesfully(message, 'Пароль успешно изменен', 'auth_data_reader')
    start(message, True)
    return


def send_error(message: types.Message, reason:str, func_name:str):
    user_id = message.chat.id
    local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

    user_states[user_id]['bot_last_error_message'] = bot.send_message(message.chat.id, f'При обработке возникла ошибка. Причина: {reason}\n\nВы будете возвращены в главное меню, оттуда вы сможете повторить действие.')
    print(f'DEBUG | ERROR | IN {func_name} | REASON: {reason}')
    sleep(4)
    bot.delete_message(user_states[user_id]['bot_last_error_message'].chat.id, user_states[user_id]['bot_last_error_message'].message_id)


def send_succsesfully(message:types.Message, reason:str, func_name:str):
    user_id = message.chat.id
    local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

    user_states[user_id]['bot_last_error_message'] = bot.send_message(message.chat.id, f'{reason}!\n\nВы будете возвращены в главное меню.')
    print(f'DEBUG | SUCCESSFULLY | IN {func_name} | REASON: {reason}')
    sleep(4)
    bot.delete_message(user_states[user_id]['bot_last_error_message'].chat.id, user_states[user_id]['bot_last_error_message'].message_id)


def render_page(page: pages, message: types.Message, del_prev_bot_message: bool = True, markup_row_width: int = 2) -> None:
    user_id = message.chat.id
    local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

    if del_prev_bot_message and (local_bot_last_message is not None):
        bot.delete_message(local_bot_last_message.chat.id, local_bot_last_message.message_id)

    new_bot_last_message = bot.send_message(message.chat.id, page['message_text'], reply_markup=markup_generator(page))
    user_states[user_id]['bot_last_message'] = new_bot_last_message

    print(f'DEBUG | INFO | RENDERING PAGE "{pages}" | USER_ID = {user_id} | BOT_LAST_MESSAGE_ID = {new_bot_last_message.message_id}')


#  ========MAIN========

@bot.message_handler(commands=['start'])
def start(message: types.Message, by_another_func:bool = False) -> None:
    user_id = message.chat.id

    bot.clear_step_handler_by_chat_id(user_id)

    if (user_id not in user_states):
        add_to_states(user_id)
        print(f'DEBUG | INFO | ADDED TO STATES | CHAT_ID: {message.chat.id} | NEW STATES = {user_states}')

    user_states[user_id]['menu_state'] = 'start'
    print(f'DEBUG | INFO | START_MENU | CHAT_ID: {message.chat.id}')

    if (not by_another_func):
        bot.delete_message(user_id, message.message_id)

    user_states[user_id]['menu_state'] = 'start'

    render_page(pages['start'], message, not by_another_func)


@bot.message_handler(commands=['debug'])
def debug(message: types.Message) -> None:
    user_id = message.chat.id

    user_states[user_id]['menu_state'] = 'debug'
    print(f'DEBUG | INFO | DEBUG_MENU | CHAT_ID: {message.chat.id}')

    bot.delete_message(message.chat.id, message.message_id)

    if (user_id not in user_states):
        add_to_states(user_id)

    for k, v in user_states.items():
        print(f'{k} = {v}')

    pages['debug_page']['message_text'] = f'{user_states}'

    render_page(pages['debug_page'], message, True)


@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def menu_callback_handler(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

    bot.delete_message(local_bot_last_message.chat.id, local_bot_last_message.message_id)
    start(call.message, True)


@bot.callback_query_handler(func=lambda call: call.data == 'auth_data_edit')
def auth_data_edit_query_handler(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

    user_states[user_id]['menu_state'] = 'start'
    print(f'DEBUG | INFO | AUTH_DATA_EDIT | CHAT_ID: {call.message.chat.id}')

    user_states[user_id]['menu_state'] = 'auth_edit'
    render_page(pages['auth_data_edit'], call.message)
    bot.register_next_step_handler(call.message, auth_data_reader)


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def help_callback_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

    print(f'DEBUG | INFO | HELP_MENU | CHAT_ID: {call.message.chat.id}')

    user_states[user_id]['menu_state'] = 'help'
    render_page(pages['help_page'], call.message)

@bot.callback_query_handler(func=lambda call: call.data=='get_homework')
def get_homework_callback_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

    render_page(pages['get_homework'], call.message)

@bot.callback_query_handler(func=lambda call: call.data=='homework_wish_photo' or call.data=='homework_wish_text')
def homework_wish_type_callback_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

    if (user_states[user_id]['auth_state']==1):
        if (call.data=='homework_wish_photo'):
                user_states[user_id]['bot_last_message'] = bot.send_photo(call.message.chat.id, return_data_handler(get_homework(user_states[user_id]['auth_data'], True, 0)))

bot.polling()
