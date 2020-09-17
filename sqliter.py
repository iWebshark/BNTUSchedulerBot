import sqlite3
import config
import models

weekdays = {0: 'пн', 1: 'вт', 2: 'ср', 3: 'чт', 4: 'пт', 5: 'сб', 6: 'вс'}


class SQLiter:

    def __init__(self):
        self.connection = sqlite3.connect(config.SQL_DB_PATH, isolation_level=None, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_user(self, user_id):
        query = "SELECT * FROM `users` WHERE `user_id` = ?"
        return self.cursor.execute(query, (user_id,)).fetchone()

    def get_users(self):
        query = "SELECT * FROM `users`"
        return self.cursor.execute(query).fetchall()

    def get_available_groups(self):
        query = "SELECT * FROM `groups`"
        groups = []
        for group in self.cursor.execute(query).fetchall():
            groups.append(group[0])
        return groups

    def reg_user(self, user_id, group_id):
        if self.get_user_group(user_id) is None:
            query = "INSERT INTO `users` VALUES (?, ?)"
            return self.cursor.execute(query, (user_id, group_id))
        else:
            self.update_user_group(user_id, group_id)

    def get_user_group(self, user_id):
        query = "SELECT * FROM `users` WHERE `user_id` = ?"
        return self.cursor.execute(query, (user_id,)).fetchone()

    def update_user_group(self, user_id, group_id):
        query = "UPDATE `users` SET `group_id` = ? WHERE `user_id` = ?"
        return self.cursor.execute(query, (group_id, user_id))

    def get_group(self, group_id):
        query = "SELECT * FROM `groups` WHERE `group_id` = ?"
        return self.cursor.execute(query, (group_id,)).fetchone()

    def get_day_schedule(self, user_id, week_day, week_num):
        group = self.get_user_group(user_id)
        weekday = weekdays[week_day]
        query = "SELECT * FROM `schedule` WHERE `day`= ? AND `group_id` = ? AND (week is NULL or week = ?) " \
                "ORDER BY time(`time_begin`)"
        data = self.cursor.execute(query, (weekday, group[1], week_num)).fetchall()
        classes = []
        for row in data:
            bntu_class = models.BNTUClass()
            bntu_class.name = row[2]
            bntu_class.type = row[3]
            bntu_class.teachers = row[4]
            bntu_class.place = row[5]
            bntu_class.week = row[6]
            bntu_class.day = row[7]
            bntu_class.time = (row[8], row[9])
            bntu_class.addition = row[10]

            classes.append(bntu_class)
        return classes
