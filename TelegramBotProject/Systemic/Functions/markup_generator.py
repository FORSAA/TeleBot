from telebot.util import quick_markup

from Systemic.Classes.Page import Page

def markup_generator(page: Page, row_width: int = 2):
    return quick_markup(page.markup_data, row_width=row_width)
