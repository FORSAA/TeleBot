import types

from Systemic.Imports.TelegramBot_Import_all import *

states: dict[int, User] = {}
# states[user_id] = {'auth_state':int, 'menu_state':str, 'bot_last_message':telebot.types.Message, 'auth_data':{'login':str, 'password':str}}
separator = ':'

#  PAGES
StartPage = Page(
    name='start',
    message_text='Добро пожаловать в главное меню телеграмм бота!\n\n Используйте кнопки ниже для навигации.',
    markup_data={
        'Смена Логина/Пароля':{'callback_data':'auth_data_edit'},
        'Как пользоваться?':{'callback_data':'help'},
        'Получить Д/З':{'callback_data':'get_homework'},
    }
)

AuthDataEditPage = Page(
    name='auth_data_edit',
    message_text=f'Тут вы можете поменять ваш логин и пароль для автоматической работы бота.\n\nЧтобы сменить ваш пароль, напишите его в следующем виде без пробелов: "Логин{separator}Пароль"\n\nP.S: <i>Отправляя свои данные авторизации вы делаете это добровольно и соглашаетесь с их обработкой.</i>"',
    markup_data={
        '« Вернуться в главное меню':{'callback_data':'menu'},
    }
)

HelpPage = Page(
    name='help_page',
    message_text='Как пользоваться ботом? Очень легко!\n\nДля начала использования бота достаточно ввести логин и пароль от сайта ГИССОЛО на странице "Смена логина/пароля". (Кнопка "Смена Логина/Пароля"). \n \n После выполнения этого шага вы можете перейти по пути "Получить Д/З->Текст" и выбрать дату. Ваш запрос будет обработан.',
    markup_data={
        '« Вернуться в главное меню':{'callback_data':'menu'}
    }
)

GetHomeworkPage = Page(
    name='get_homework',
    message_text='Выберите в каком формате бот должен прислать вам домашнее задание.',
    markup_data={
        'Текст':{'callback_data':'homework_wish_text'},
        'Фотография':{'callback_data':'homework_wish_photo'},
        '« Вернуться в главное меню':{'callback_data':'menu'}
    }
)

DaySelectPage = Page(
    name='day_select_page',
    message_text='Выберите день недели домашнее задание для которого вас интересует',
    markup_data={
        'Понедельник':{'callback_data':'0_day'},
        'Вторник':{'callback_data':'1_day'},
        'Среда':{'callback_data':'2_day'},
        'Четверг':{'callback_data':'3_day'},
        'Пятница':{'callback_data':'4_day'},
        'Суббота':{'callback_data':'5_day'},
        '« Вернуться в главное меню':{'callback_data':'menu'}
    }
)

BlankPage = Page(
    name='blank_page',
    message_text=f'',
    markup_data={
        '« Вернуться в главное меню':{'callback_data':'menu'}
    }
)


class TelegramBot():
    def __init__(self, token: str):
        self.token:str = token
        self.bot:telebot.TeleBot = telebot.TeleBot(self.token)

        #   ===============HANDLERS===============

        @self.bot.message_handler(commands=['start'])
        def start_handler(message: Message):
            user_id = message.chat.id
            if (user_id in states):
                main_menu(message)
            else:
                setup(message)


        def main_menu(message: Message) -> None:
            user_id = message.chat.id

            self.bot.delete_message(user_id, message.message_id)
            self.bot.clear_step_handler_by_chat_id(message.chat.id)

            self.render_page(message, StartPage)


        def setup(message: Message) -> None:
            user_id = message.chat.id

            self.add_to_states(user_id)
            self.bot.delete_message(user_id, message.message_id)
            self.render_page(message, StartPage, False)


        @self.bot.message_handler(func=lambda message: message)
        def non_defined_commands_cleaning(message: Message):
            self.bot.delete_message(message.chat.id, message.message_id)


        @self.bot.callback_query_handler(func=lambda call: call.data=='auth_data_edit')
        def auth_data_edit_handler(call: CallbackQuery):
            user_id = call.from_user.id

            self.render_page(call.message, AuthDataEditPage, True)

            self.bot.register_next_step_handler_by_chat_id(call.message.chat.id, auth_data_reader)


        def auth_data_reader(message: Message) -> None:
            response:str = message.text
            user_id = message.chat.id
            auth_data:dict[str, str] = {}

            if (separator in response):

                response = response.replace(' ', '')
                temp_list = response.split(separator)
                if (len(temp_list)>1 and '' not in temp_list):
                    auth_data['login'], auth_data['password'] = temp_list
                    states[user_id].auth_data = auth_data
                    states[user_id].auth_state = 1
                    self.edit_message_for_time(states[user_id].bot_last_message, 'Пароль успешно изменен!\n\nВы будете возвращены в меню.')
                    self.render_page(message, StartPage)
                else:
                    self.edit_message_for_time(states[user_id].bot_last_message, f'Недостаточно данных! Введите данные по формату еще раз, убедитесь что введенные данные корректны.\n\nP.s: Формат - <b>Логин{separator}Пароль.</b>')
                    self.bot.register_next_step_handler_by_chat_id(user_id, auth_data_reader)

            elif (response.startswith('/')):
                self.render_page(message, StartPage)
                return

            else:
                self.edit_message_for_time(states[user_id].bot_last_message, f'Переданные данные не соответствуют формату!\n\nРазделите логин и пароль с помощью символа " {separator} " без лишних пробелов.')
                self.bot.register_next_step_handler_by_chat_id(user_id, auth_data_reader)

            self.bot.delete_message(user_id, message.message_id)

            return None


        @self.bot.callback_query_handler(func=lambda call: call.data=='get_homework')
        def get_homework_handler(call: CallbackQuery):
            user_id = call.from_user.id
            if (states[user_id].auth_state == 1):
                self.render_page(call.message, GetHomeworkPage)
            else:
                BlankPage.message_text = 'Ошибка! Для начала вы должны авторизоваться.\n\nЧтобы сделать это перейдите в "Смена Логина/Пароля"'
                self.render_page(call.message, BlankPage)


        @self.bot.callback_query_handler(func=lambda call: call.data in ['homework_wish_text', 'homework_wish_photo'])
        def wish_type_handler(call: CallbackQuery):
            user_id = call.from_user.id

            states[user_id].wish_type = call.data

            self.render_page(call.message, DaySelectPage)


        @self.bot.callback_query_handler(func=lambda call:call.data in ['0_day', '1_day', '2_day', '3_day', '4_day', '5_day'])
        def day_select_handler(call: CallbackQuery):
            user_id = call.from_user.id

            wish_day:int = int(call.data[0])

            states[user_id].wish_day = wish_day

        def send_homework_response(message):
            pass
            # TODO: Homework handler / Homework Formatter / Homework Getter

        @self.bot.callback_query_handler(func=lambda call: call.data=='menu')
        def menu_handler(call: CallbackQuery):
            self.render_page(call.message, StartPage)


        @self.bot.callback_query_handler(func=lambda call: call.data=='help')
        def help_handler(call: CallbackQuery):
            self. render_page(call.message, HelpPage)

        #  ==============HANDLERS END==============

    def render_page(self, message: Message, page: Page, del_prev: bool = True) -> None:
        user_id = message.chat.id

        local_bot_last_message: Message = states[user_id].bot_last_message

        self.bot.clear_step_handler_by_chat_id(user_id)

        if (del_prev and local_bot_last_message is not None):
            try:
                self.bot.delete_message(user_id, local_bot_last_message.message_id)
            except telebot.apihelper.ApiException:
                pass

        states[user_id].bot_last_message = self.bot.send_message(user_id, page.message_text, reply_markup=markup_generator(page), parse_mode='HTML')


    def edit_message_to_page(self, message:Message, edit_to: Page) -> str:
        user_id = message.chat.id

        current_message_text = message.text

        self.bot.edit_message_text(edit_to.message_text, user_id, message.message_id, reply_markup=markup_generator(edit_to), parse_mode='HTML')

        return current_message_text


    def edit_message_for_time(self, message: Message, text:str) -> None:
        user_id = message.chat.id

        BlankPage.message_text = text

        reply_markup_from_message = message.reply_markup

        temp_str = self.edit_message_to_page(message, BlankPage)
        sleep(3)

        self.bot.edit_message_text(temp_str, user_id, message.message_id, reply_markup=reply_markup_from_message, parse_mode='HTML')


    @staticmethod
    def add_to_states(user_id: int) -> bool:
        defaults = {
            'auth_state':0,
            'menu_state':'start',
            'bot_last_message':None,
            'auth_data':None,
            'wish_type':None,
            'wish_day':None,
        }
        states[user_id] = User(defaults)
        if (user_id in states):
            return True
        else:
            return False


    def run(self):
        self.bot.polling(none_stop=True)

if __name__=='__main__':
    Bot = TelegramBot('6070580163:AAFKRJt7nnNWL__vunKkFVz1r1IZ6xDJgXI')

    Bot.run()

