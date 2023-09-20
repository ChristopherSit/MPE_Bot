import time
from datetime import datetime, timezone
from structs import Day

def getCurrentDateTime():
    cdt = datetime.now(timezone.utc)
    CurrentDateTime = Day(cdt.year,
                          cdt.month,
                          cdt.day,
                          cdt.hour,
                          cdt.minute,
                          )
    return CurrentDateTime