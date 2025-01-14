import models
import psycopg2
import utils

schedule_cache = dict()


class Database:

    def __init__(self):
        self.connection = psycopg2.connect(
            host="",
            database="",
            user="",
            password="")
        self.connection.set_session(autocommit=True)
        self.cursor = self.connection.cursor()

    def get_all_users(self):
        query = ""
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        users = dict()
        for row in data:
            user = models.User()
            user.user_id = row[0]
            user.chat_id = row[1]
            user.username = row[2]

            users[user.user_id] = user
        return users

    def get_user(self, user_id):
        query = ""
        self.cursor.execute(query, (user_id,))
        data = self.cursor.fetchone()
        user = models.User()
        user.user_id = data[0]
        user.chat_id = data[1]
        user.username = data[2]
        return user

    def reg_user(self, chat_id, user_id, username):
        query = ""
        self.cursor.execute(query, (chat_id, user_id, username))

    def update_user(self, chat_id, user_id, username):
        query = ""
        self.cursor.execute(query, (chat_id, username, user_id))

    def get_week_schedule(self, week_num) -> list:
        week_schedule = list()
        for day_num, day_name in utils.weekdays.items():
            day_schedule = self.get_day_schedule(day_name.lower(), week_num)
            week_schedule.append(day_schedule)
        return week_schedule

    def get_day_schedule(self, weekday, week_num) -> models.BNTUDaySchedule:
        query = " "
        self.cursor.execute(query, (weekday, week_num))
        data = self.cursor.fetchall()
        classes = []
        for row in data:
            bntu_class = models.BNTUClass()
            bntu_class.name = row[1]
            bntu_class.type = row[2]
            bntu_class.teachers = row[3]
            bntu_class.place = row[4]
            bntu_class.week = row[5]
            bntu_class.day = row[6]
            bntu_class.time = (row[7], row[8])
            bntu_class.addition = row[9]

            classes.append(bntu_class)
        schedule = models.BNTUDaySchedule()
        schedule.day_schedule = classes
        return schedule
