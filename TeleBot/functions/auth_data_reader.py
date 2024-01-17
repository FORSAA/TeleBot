from functions.test_auth_data_saver import test_auth_data_saver
from telebot import types

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
