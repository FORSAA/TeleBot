from telebot import types

def send_succsesfully(message:types.Message, reason:str, func_name:str):
    user_id = message.chat.id
    local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

    user_states[user_id]['bot_last_error_message'] = bot.send_message(message.chat.id, f'{reason}!\n\nВы будете возвращены в главное меню.')
    print(f'DEBUG | SUCCESSFULLY | IN {func_name} | REASON: {reason}')
    sleep(2.5)
    bot.delete_message(user_states[user_id]['bot_last_error_message'].chat.id, user_states[user_id]['bot_last_error_message'].message_id)

