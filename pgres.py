import models
import psycopg2

weekdays = {0: 'пн', 1: 'вт', 2: 'ср', 3: 'чт', 4: 'пт', 5: 'сб', 6: 'вс'}


class Database:

    def __init__(self):
        self.connection = psycopg2.connect(
            host="ec2-54-247-71-245.eu-west-1.compute.amazonaws.com",
            database="d8agj8uoqdr5hm",
            user="gufyrauhrcosoq",
            password="ad0480690fea6bde2d6c05cac7e41eb472f596ee3e62c1e9bc61baca9a0bd1f8")
        self.connection.set_session(autocommit=True)
        self.cursor = self.connection.cursor()

    def get_user(self, user_id):
        query = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()

    def get_users(self):
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_available_groups(self):
        query = "SELECT * FROM groups"
        groups = []
        self.cursor.execute(query)
        for group in self.cursor.fetchall():
            groups.append(group[0])
        return groups

    def reg_user(self, user_id, group_id):
        if self.get_user_group(user_id) is None:
            query = "INSERT INTO users VALUES (%s, %s)"
            self.cursor.execute(query, (user_id, group_id))
        else:
            self.update_user_group(user_id, group_id)

    def get_user_group(self, user_id):
        query = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()

    def update_user_group(self, user_id, group_id):
        query = "UPDATE users SET group_id = %s WHERE user_id = %s"
        return self.cursor.execute(query, (group_id, user_id))

    def get_group(self, group_id):
        query = "SELECT * FROM groups WHERE group_id = %s"
        self.cursor.execute(query, (group_id,))
        return self.cursor.fetchone()

    def get_day_schedule(self, user_id, week_day, week_num):
        group = self.get_user_group(user_id)
        weekday = weekdays[week_day]
        query = "SELECT * FROM schedule WHERE day = '%s' AND group_id = %s AND (week is NULL or week = '%s') " \
                "ORDER BY time_begin"
        self.cursor.execute(query, (weekday, group[1], week_num))
        data = self.cursor.fetchall()
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
