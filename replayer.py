import os
import threading
from time import time, sleep

import settings

from log_etl import Log
from visitor import Visitor

start = time()
log = Log(os.path.join(os.path.dirname(__file__),'data/data.txt'))

v = Visitor(settings.TARGET_HOST)

for data in log.etl():
    elapsed = time()-start
    if ((data['time']-log.start) > (elapsed * settings.SPEED)):
        sleep((data['time']-log.start)-(elapsed * settings.SPEED))

    while (threading.activeCount() > settings.THREAD_LIMIT):
        print "Threading limit reached.  Sleeping..."
        sleep(settings.THREAD_LIMIT_SLEEP)

    v.visit(data['url'])

v.close()
log.close()
