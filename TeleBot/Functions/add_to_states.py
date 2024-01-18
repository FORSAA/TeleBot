def add_to_states(user_id: int, states: dict):
    default_user_states = {
        user_id:{
            'auth_state':0,
            'menu_state':'',
            'bot_last_message':None,
            'bot_last_error_message':None,
            'auth_data':{}
        }
    }
    states.update(default_user_states)
