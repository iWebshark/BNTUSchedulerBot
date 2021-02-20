import datetime


class User:

    def __init__(self) -> None:
        self.__username = None
        self.__user_id = None
        self.__chat_id = None

    @property
    def username(self):
        return self.username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def user_id(self):
        return self.user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def chat_id(self):
        return self.chat_id

    @chat_id.setter
    def chat_id(self, chat_id):
        self.__chat_id = chat_id


class BNTUDaySchedule:

    def __init__(self) -> None:
        self.__day_schedule: list = list()

    @property
    def day_schedule(self):
        return self.__day_schedule

    @day_schedule.setter
    def day_schedule(self, day_schedule: list):
        self.__day_schedule = day_schedule

    def __str__(self) -> str:
        text = ''
        for cl in self.day_schedule:
            text += f"{cl}\n\n"
        return text


class BNTUClass:
    class_types = {'практ': 'Практика', 'лек': 'Лекция', None: None}
    class_type = {'Практика': '🟠', 'Лекция': '🟢', None: '🔵'}

    def __init__(self):
        self.name = None
        self.__type = None
        self.teachers = None
        self.place = None
        self.week = None
        self.__day = None
        self.__time = None
        self.addition = None

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, typecl):
        self.__type = self.class_types[typecl]

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        self.__day = str(day).capitalize()

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        t_begin = time[0].split(":")
        t_end = time[1].split(":")
        begin = datetime.time(int(t_begin[0]), int(t_begin[1]))
        end = datetime.time(int(t_end[0]), int(t_end[1]))
        self.__time = f"{begin.strftime('%-H:%M')}-{end.strftime('%-H:%M')}"

    def __str__(self) -> str:
        text = f"{self.class_type[self.type]}<b>{self.time}</b> | {self.name} | <b>{self.place}</b>\n" \
               f"{self.teachers}"
        if self.addition is not None:
            text += f" ({self.addition})"
        if self.week is not None:
            text += f" <i>{self.week} неделя</i>"
        return text
