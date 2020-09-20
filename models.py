import datetime


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
