from math import floor

from kivy.clock import Clock
from refs import Refs

MONTHS = ['Vadrinerth', 'Xazoclite', 'Signion', 'Chaphapus', 'Poanus', 'Nioliv', 'Dukurus', 'Llamalara', 'Ladus', 'Chiea', 'Chalosie', 'Aitune', 'Vochatis', 'Simarilia', 'Strolla', 'Vyria']
NUMBER_ENDINGS = ['st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th',
                  'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th',
                  'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th',
                  'st', 'nd', 'rd', 'th', 'th', 'th']

MINUTES_IN_HOUR = 60
HOURS_IN_DAY = 25
DAYS_IN_MONTH = 36
MONTHS_IN_YEAR = 16
MINUTES_IN_DAY = MINUTES_IN_HOUR * HOURS_IN_DAY
MINUTES_IN_MONTH = MINUTES_IN_DAY * DAYS_IN_MONTH
MINUTES_IN_YEAR = MINUTES_IN_MONTH * MONTHS_IN_YEAR


class Calendar:
    def __init__(self, time):
        self._time = time
        self._callback = None
        self._events = {}
        Clock.schedule_interval(self._increase_time, 5)

    @staticmethod
    def _get_time_parts(time):
        year = floor(time / MINUTES_IN_YEAR)
        time %= MINUTES_IN_YEAR
        month = floor(time / MINUTES_IN_MONTH)
        time %= MINUTES_IN_MONTH
        day = floor(time / MINUTES_IN_DAY)
        time %= MINUTES_IN_DAY
        hour = floor(time / MINUTES_IN_HOUR)
        time %= MINUTES_IN_HOUR
        return year, month, day, hour, time

    def _increase_time(self, dt):
        self._time += 1
        if self._callback is not None:
            self._callback()
        if Refs.gc.get_floor_data() is not None:
            floor_data = Refs.gc.get_floor_data()
            if floor_data.get_node_time() == 0:
                floor_data.set_node_time(self._time)
            elif self._time - floor_data.get_node_time() > 20:
                floor_data.generate_time_encounter(self._time)
        if self._time - Refs.gc.get_last_save_time() > 180:
            Refs.gc.save_game(None)
            Refs.app.log('Auto Save Game')
        self.check_events()

    def fast_forward(self, dt):
        self._time += dt
        self.check_events()
        if self._callback is not None:
            self._callback()

    def set_callback(self, callback):
        self._callback = callback

    def check_events(self):
        for key in sorted(list(self._events.keys())):
            if key > self._time:
                self._events.pop(key)()

    def schedule_event(self, int_time, callback):
        self._events[int_time] = callback

    def get_int_time(self):
        return self._time

    def get_int_date(self):
        return self._time

    def get_date(self):
        year, month, day, hour, minute = self._get_time_parts(self._time)
        return f'{MONTHS[month]} {day + 1}{NUMBER_ENDINGS[day]}, {year}'

    def get_time(self):
        year, month, day, hour, minute = self._get_time_parts(self._time)
        return f'{hour:02}:{minute:02} {MONTHS[month]} {day + 1}{NUMBER_ENDINGS[day]}, {year}'

    def get_days_until(self, int_time):
        time_until = int_time - self._time
        months = floor(time_until / (36 * 25 * 60))
        days = floor((time_until % (36 * 25 * 60)) / (25 * 60))
        return months * DAYS_IN_MONTH + days

    @staticmethod
    def int_time_to_date(int_time):
        year, month, day, hour, minute = Calendar._get_time_parts(int_time)
        return f'{MONTHS[month]} {day + 1}{NUMBER_ENDINGS[day]}, {year}'
