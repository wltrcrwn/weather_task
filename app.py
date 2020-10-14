from csv import DictReader
from itertools import groupby
from statistics import mean
from datetime import timedelta, datetime


def group_by_week(el):
    time = datetime.strptime(el['date'], '%d.%m.%Y %H:%M')
    while datetime.weekday(time) != 0:
        time += timedelta(days=1)
    new_date = time + timedelta(days=7)
    return f'{time.day}/{time.month}/{time.year} - {new_date.day}/{new_date.month}/{new_date.year}'


def group_by_month(el):
    time = datetime.strptime(el['date'], '%d.%m.%Y %H:%M')
    return f"{time.month}-{time.year}"


def group_by_day(el):
    time = datetime.strptime(el['date'], '%d.%m.%Y %H:%M')
    return f"{time.day}-{time.month}-{time.year}"


def calc(data, func, index):
    temp = {x: mean(float(j[index]) for j in y) for x, y in data.items()}
    return {x: y.__round__(2) for x, y in filter(lambda x: temp[x[0]] == func(temp.values()), temp.items())}


if __name__ == '__main__':
    reader = DictReader(open('data.csv', encoding='utf-8'), delimiter=';')
    DATA = [dict(r) for r in reader]
    DATA = sorted(DATA, key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y %H:%M'))
    months = {x: list(y) for x, y in groupby(DATA, key=group_by_month)}
    days = {x: list(y) for x, y in groupby(DATA, key=group_by_day)}
    weeks = {x: list(y) for x, y in groupby(DATA, key=group_by_week)}

    print('Самая ветреный месяц', calc(weeks, min, 'Ff'))
    print('Самый холодный месяц', calc(months, min, 'T'))
    print('Самый холодный день', calc(days, min, 'T'))
    print('Самый теплый месяц', calc(months, max, 'T'))
    print('Самый теплый день', calc(days, max, 'T'))
    print('Самая теплая неделя', calc(weeks, max, 'T'))
