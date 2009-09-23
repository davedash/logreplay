SPEED = 1 # we will play the log @ 1x production traffic
THREAD_LIMIT = 2000 # os will run out of resources
THREAD_LIMIT_SLEEP = 2 # this is catchup time
try:
    from local_settings import *
except ImportError:
    pass