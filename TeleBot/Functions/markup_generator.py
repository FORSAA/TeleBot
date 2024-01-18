from telebot.util import quick_markup

def markup_generator(page: dict, row_width: int = 2):
    return quick_markup(page['markup_data'], row_width=row_width)
