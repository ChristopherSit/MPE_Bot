import threading
import discord
from discord.ext import tasks
import time
import queue
import helpers
from structs import Signal, Day
from datetime import datetime, timezone, timedelta

def onStartup(event_queue, client):
    # thread stack
    dailyInterrupt = threading.Event()
    weeklyInterrupt = threading.Event()
    threadStack = [threading.Thread(target=dailyResetWatcher, args=(event_queue, dailyInterrupt,)),
                   threading.Thread(target=weeklyResetWatcher, args=(event_queue, weeklyInterrupt,))]
    
    threadStack[0].start()
    threadStack[1].start()
    print('started threads')
    
def dailyResetWatcher(event_queue, interrupt):
    while(True):
        currentDateTime = datetime.now(timezone.utc)
        timeToReset = timedelta(hours=23-currentDateTime.hour,
                                minutes=59-currentDateTime.minute,
                                seconds=60-currentDateTime.second)
        print('next daily reset is in: ' + str(timeToReset))
        if not interrupt.wait(timeToReset.total_seconds()):
            print('putting daily reset event signal')
            event_queue.put(Signal(event='dailyReset',
                                   payload=timeToReset))
        else:
            break

def weeklyResetWatcher(event_queue, interrupt):
    while(True):
        currentDateTime = datetime.now(timezone.utc)
        timeToReset = timedelta(days=(2-currentDateTime.weekday())%7,
                                hours=23-currentDateTime.hour,
                                minutes=59-currentDateTime.minute,
                                seconds=60-currentDateTime.second)
        print('next weekly reset is in: ' + str(timeToReset))
        if not interrupt.wait(timeToReset.total_seconds()):
            print('putting weekly reset event signal')
            event_queue.put(Signal(event='weeklyReset',
                                   payload=timeToReset))
        else:
            break
