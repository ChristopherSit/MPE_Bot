class Signal:
    def __init__(self, event='default', payload='none'):
        self.event = event
        self.payload = payload

    def __str__(self):
        return f'{self.event},{self.payload}'
    
class Day:
    def __init__(self, year=0, month=0, day=0, hour=0, minute=0, second=0, timezone=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.timezone = timezone

    def __str__(self):
        return f'{self.year},{self.month},{self.day},{self.hour},{self.minute},{self.second},{self.timezone}'