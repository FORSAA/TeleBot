
def add_to_states(user_id:int):
    import classes.BotClass
    default_user_states = {
        'auth_state':0,
        'menu_state':'',
        'bot_last_message':None,
        'bot_last_error_message':None,
        'auth_data':{}
    }
    classes.BotClass.user_states[user_id] = 5
    print(classes.BotClass.user_states)

