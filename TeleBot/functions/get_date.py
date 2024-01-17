import locale
from datetime import timedelta, datetime

locale.setlocale(locale.LC_TIME, 'ru_RU')

def get_date(offset: int = 0) -> str:
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
              "декабря"]
    today: datetime = datetime.today()+timedelta(days=offset)

    day_num: str = today.strftime("%d")
    month: str = months[int(today.strftime("%m"))-1]
    weekday: str = today.strftime("%A")
    weekday: str = weekday[0].upper()+weekday[1:]
    year: str = today.strftime("%Y")

    return f'{weekday}, {day_num} {month} {year} г.'

if __name__ == '__main__':
    print(get_date(0))