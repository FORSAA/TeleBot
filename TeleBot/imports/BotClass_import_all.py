import telebot
from telebot.types import CallbackQuery
from telebot.util import quick_markup
from telebot import types
from time import sleep
from functions.days_until_next_weekday import days_until_next_weekday
from functions.get_date import get_date
from functions.days_until_next_weekday import days_until_next_weekday
from functions.test_auth_data_saver import test_auth_data_saver
from functions.auth_data_reader import auth_data_reader
from functions.add_to_states import add_to_states
from functions.markup_generator import markup_generator
from functions.send_error import send_error
from functions.send_succsesfully import send_succsesfully
from functions.render_page import render_page
