from main import db

schedule_cache = {
    'week1': list(),
    'week2': list()
}


def get_day_schedule(week_num, day_num):
    week_schedule = get_week_schedule(week_num)
    return week_schedule[day_num]


def get_week_schedule(week_number):
    week_key = f'week{week_number}'
    if len(schedule_cache.get(week_key)) == 0:
        week_schedule = db.get_week_schedule(week_number)
        schedule_cache[week_key] = week_schedule

    return schedule_cache[week_key]
