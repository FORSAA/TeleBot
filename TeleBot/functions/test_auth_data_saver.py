from telebot import types

def test_auth_data_saver(message:types.Message, to_save_auth_data:list) -> None:
    user_id = message.chat.id

    auth_data = {}
    login, password = to_save_auth_data
    auth_data['login'] = login
    auth_data['password'] = password
    user_states[user_id]['auth_data'] = auth_data
    user_states[user_id]['auth_state'] = 1
    print(f'DEBUG | INFO | {user_id} GOT AUTH.')
