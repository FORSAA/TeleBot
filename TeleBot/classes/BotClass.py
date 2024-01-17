from imports.BotClass_import_all import *

user_states = {}
separator = ':'

pages = {
    'start':{'message_text':'Добро пожаловать в главное меню телеграмм бота!\n\n Используйте кнопки ниже для навигации.',
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
    'day_select_page':{'message_text':'Выберите день недели домашнее задание для которого вас интересует',
                       'markup_data':{
                           'Понедельник':{'callback_data':'0_day'},
                           'Вторник':{'callback_data':'1_day'},
                           'Среда':{'callback_data':'2_day'},
                           'Четверг':{'callback_data':'3_day'},
                           'Пятница':{'callback_data':'4_day'},
                           'Суббота':{'callback_data':'5_day'}
                       }
                       },
    'debug_page':{'message_text':str(),
                  'markup_data':{
                      '« Вернуться в главное меню':{'callback_data':'menu'}
                  }
                  },

}

class TelegramBot():
    def __init__(self, token):
        self.token = token
        self.bot = telebot.TeleBot(self.token)

        @self.bot.message_handler(commands=['start'])
        def start(message: types.Message, by_another_func: bool = False) -> None:
            user_id = message.chat.id

            self.bot.clear_step_handler_by_chat_id(user_id)

            if (user_id not in user_states):
                add_to_states(user_id)
                print(f'DEBUG | INFO | ADDED TO STATES | CHAT_ID: {message.chat.id} | NEW STATES = {user_states}')

            user_states[user_id]['menu_state'] = 'start'
            print(f'DEBUG | INFO | START_MENU | CHAT_ID: {message.chat.id}')

            if (not by_another_func):
                self.bot.delete_message(user_id, message.message_id)

            user_states[user_id]['menu_state'] = 'start'

            render_page(pages['start'], message, not by_another_func)

        @self.bot.message_handler(commands=['debug'])
        def debug(message: types.Message) -> None:
            user_id = message.chat.id

            if (user_id not in user_states):
                add_to_states(user_id)
                print(f'DEBUG | INFO | ADDED TO STATES | CHAT_ID: {message.chat.id} | NEW STATES = {user_states}')

            user_states[user_id]['menu_state'] = 'debug'
            print(f'DEBUG | INFO | DEBUG_MENU | CHAT_ID: {message.chat.id}')

            self.bot.delete_message(message.chat.id, message.message_id)

            if (user_id not in user_states):
                add_to_states(user_id)

            for k, v in user_states.items():
                print(f'{k} = {v}')

            pages['debug_page']['message_text'] = f'{user_states}'

            render_page(pages['debug_page'], message, True)

        @self.bot.callback_query_handler(func=lambda call:call.data=='menu')
        def menu_callback_handler(call: types.CallbackQuery) -> None:
            user_id = call.from_user.id
            local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

            self.bot.delete_message(local_bot_last_message.chat.id, local_bot_last_message.message_id)
            start(call.message, True)

        @self.bot.callback_query_handler(func=lambda call:call.data=='auth_data_edit')
        def auth_data_edit_query_handler(call: types.CallbackQuery) -> None:
            user_id = call.from_user.id

            if (user_id not in user_states):
                add_to_states(user_id)
                print(f'DEBUG | INFO | ADDED TO STATES | CHAT_ID: {user_id} | NEW STATES = {user_states}')

            local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

            user_states[user_id]['menu_state'] = 'auth_data_edit'
            print(f'DEBUG | INFO | AUTH_DATA_EDIT | CHAT_ID: {call.message.chat.id}')

            user_states[user_id]['menu_state'] = 'auth_edit'
            render_page(pages['auth_data_edit'], call.message)
            bot.register_next_step_handler(call.message, auth_data_reader)

        @self.bot.callback_query_handler(func=lambda call:call.data=='help')
        def help_callback_handler(call: types.CallbackQuery):
            user_id = call.from_user.id

            if (user_id not in user_states):
                add_to_states(user_id)
                print(f'DEBUG | INFO | ADDED TO STATES | CHAT_ID: {user_id} | NEW STATES = {user_states}')

            local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

            print(f'DEBUG | INFO | HELP_MENU | CHAT_ID: {call.message.chat.id}')

            user_states[user_id]['menu_state'] = 'help'
            render_page(pages['help_page'], call.message)

        @self.bot.callback_query_handler(func=lambda call:call.data=='get_homework')
        def get_homework_callback_handler(call: types.CallbackQuery):
            user_id = call.from_user.id

            if (user_id not in user_states):
                add_to_states(user_id)
                print(f'DEBUG | INFO | ADDED TO STATES | CHAT_ID: {user_id} | NEW STATES = {user_states}')

            local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

            render_page(pages['get_homework'], call.message)

        @self.bot.callback_query_handler(func=lambda call:call.data in ['homework_wish_photo', 'homework_wish_text'])
        def homework_wish_type_callback_handler(call: types.CallbackQuery):
            user_id = call.from_user.id
            local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

            if (user_states[user_id]['auth_state']==1):
                if (call.data=='homework_wish_photo'):
                    user_states[user_id]['photo_mode'] = True
                else:
                    user_states[user_id]['photo_mode'] = False
            else:
                send_error(call.message, 'Не введен пароль для авторизации и получения домашнего задания/расписания.',
                           'homework_wish_type_callback_hadler', True)
                start(call.message, True)
                return

            render_page(pages['day_select_page'], call.message, markup_row_width=3)

        @self.bot.callback_query_handler(func=lambda call:call.data in ['0_day', '1_day', '2_day', '3_day', '4_day', '5_day'])
        def change_day_callback_handler(call: types.CallbackQuery):
            user_id = call.from_user.id
            local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

            day_wish = int(call.data[0])

            offset: int = days_until_next_weekday(day_wish)

            self.bot.delete_message(user_id, local_bot_last_message.message_id)
            user_states[user_id]['bot_last_message'] = bot.send_message(user_id,
                                                                        f'Получение домашнего задания на {get_date(offset)}..')
            local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

            auth_data = user_states[user_id]['auth_data']
            is_photo = user_states[user_id]['photo_mode']

            returned_data = get_homework(auth_data, is_photo, offset)

            self.bot.delete_message(user_id, local_bot_last_message.message_id)

            if (returned_data=='screenshot'):
                with open(os.getcwd()+r'\screenshots\Homework_Screenshot.png', 'rb') as screenshot:
                    user_states[user_id]['bot_last_message'] = self.bot.send_photo(user_id, screenshot,
                                                                              f'Домашнее задание на {get_date(offset)}')
                path = os.getcwd()+r'\screenshots\Homework_Screenshot.png'
                os.remove(path)
            elif (type(returned_data) is str and 'error' not in returned_data):
                user_states[user_id]['bot_last_message'] = self.bot.send_message(user_id,
                                                                            f'Домашнее задание на {get_date(offset)}\n{returned_data}\n')  # , reply_markup=quick_markup({'Вернуться в меню':{'callback_data':'menu'}})
            else:
                send_error(call.message, returned_data, 'homework_wish_type_callback_hadler')

            start(call.message, True)

    def run(self):
        self.bot.polling(none_stop=True)

if __name__=='__main__':
    Bot = TelegramBot('6070580163:AAFKRJt7nnNWL__vunKkFVz1r1IZ6xDJgXI')

    Bot.run()