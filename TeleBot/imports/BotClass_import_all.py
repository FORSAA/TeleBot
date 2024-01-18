import telebot
from telebot.types import CallbackQuery
from telebot.util import quick_markup
from telebot import types
from time import sleep
from Functions.days_until_next_weekday import days_until_next_weekday
from Functions.get_date import get_date
from Functions.days_until_next_weekday import days_until_next_weekday
from Functions.test_auth_data_saver import test_auth_data_saver
from Functions.auth_data_reader import auth_data_reader
from Functions.add_to_states import add_to_states
from Functions.markup_generator import markup_generator
from Functions.send_error import send_error
from Functions.send_succsesfully import send_succsesfully
from Functions.render_page import render_page
