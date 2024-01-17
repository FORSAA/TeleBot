from telebot import types

def send_error(message: types.Message, reason:str, func_name:str, is_deleting_prev:bool = False):
    user_id = message.chat.id
    local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

    if (is_deleting_prev):
        bot.delete_message(user_id, local_bot_last_message.message_id)

    user_states[user_id]['bot_last_error_message'] = bot.send_message(message.chat.id, f'При обработке возникла ошибка. Причина: {reason}\n\nВы будете возвращены в главное меню, оттуда вы сможете повторить действие.')
    print(f'DEBUG | ERROR | IN {func_name} | REASON: {reason}')
    sleep(2.5)
    bot.delete_message(user_states[user_id]['bot_last_error_message'].chat.id, user_states[user_id]['bot_last_error_message'].message_id)
