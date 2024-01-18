from datetime import datetime

def days_until_next_weekday(target_weekday: int) -> int:
    weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

    current_day_index = datetime.now().weekday()

    difference = target_weekday-current_day_index

    return difference


if __name__=='__main__':
    print(days_until_next_weekday(0))  # 0 - Monday, 1 - Tuesday,...
