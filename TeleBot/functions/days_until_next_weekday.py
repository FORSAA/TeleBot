from datetime import timedelta, datetime

def days_until_next_weekday(target_weekday):
    weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

    current_day_index = datetime.now().weekday()

    difference = target_weekday - current_day_index

    # if difference < 0:
    #     difference += 7

    return difference

if __name__ == '__main__':
    print(days_until_next_weekday(0))