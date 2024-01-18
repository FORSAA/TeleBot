from telebot import types
from Classes.BotClass import pages

def render_page(page: pages, message: types.Message, del_prev_bot_message: bool = True, markup_row_width: int = 2) -> None:
    user_id = message.chat.id
    local_bot_last_message: types.Message = user_states[user_id]['bot_last_message']

    if del_prev_bot_message and (local_bot_last_message is not None):
        bot.delete_message(local_bot_last_message.chat.id, local_bot_last_message.message_id)

    new_bot_last_message = bot.send_message(message.chat.id, page['message_text'], reply_markup=markup_generator(page, markup_row_width))
    user_states[user_id]['bot_last_message'] = new_bot_last_message

    print(f'DEBUG | INFO | RENDERING PAGE "{page}" | USER_ID = {user_id} | BOT_LAST_MESSAGE_ID = {new_bot_last_message.message_id}')
