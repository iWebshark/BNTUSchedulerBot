from main import db

schedule_cache = {
    'week1': list(),
    'week2': list()
}

users_cache = dict()


def get_day_schedule(week_num, day_num):
    week_schedule = get_week_schedule(week_num)
    return week_schedule[day_num]


def get_week_schedule(week_number):
    week_key = f'week{week_number}'
    if len(schedule_cache.get(week_key)) == 0:
        week_schedule = db.get_week_schedule(week_number)
        schedule_cache[week_key] = week_schedule

    return schedule_cache[week_key]


def update_user_cache(user_id):
    user = db.get_user(user_id)
    users_cache[user.user_id] = user


def get_user(user_id):
    if users_cache.get(user_id) is None:
        update_user_cache(user_id)
    return users_cache.get(user_id)


def reg_user(chat_id, user_id, username):
    db.reg_user(chat_id, user_id, username)
    update_user_cache(user_id)


def update_user(chat_id, user_id, username):
    db.update_user(chat_id, user_id, username)
    update_user_cache(user_id)
