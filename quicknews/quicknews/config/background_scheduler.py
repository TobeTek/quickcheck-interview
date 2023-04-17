import atexit
import logging

from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig()
logger = logging.getLogger(__name__)

SCHEDULER = BackgroundScheduler()
SCHEDULER.start()


import signal

onexit = lambda *args: SCHEDULER.shutdown()

atexit.register(onexit)
signal.signal(signal.SIGINT, onexit)
