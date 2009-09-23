import threading

from time import time
from urllib2 import urlopen, URLError, HTTPError

import settings


class Worker(threading.Thread):
    def __init__(self, url, visitor):
        self.url = url
        self.visitor = visitor
        threading.Thread.__init__(self)

    def run(self):
        # open url
        start = time()
        content = None
        code = 0

        try:
            f = urlopen(self.url)
            content = f.read()
            code = f.code
            
        except HTTPError, e:
            code = e.code
            try:
                content = e.read()
            except Exception, e2:
                content = e2.message

        except URLError, e:
            code = -1
            content = e.reason.message
        
        except Exception, e:
            code = -2
            content = e.message
            
        elapsed = time()-start
        self.visitor.write_log(self.url, code, elapsed, content)



class Visitor:
    codes = {}
    queries = 0

    def __init__(self, host):
        self.host    = host
        self.start   = time()
        self.log     = open('logs/status.%d'%int(self.start), 'w')
        self.bad_log = open('logs/bad.%d'%int(self.start), 'w')

    def visit(self,url):
        Worker(self.host + url, self).start()
        self.queries += 1

    def write_log(self, url, code, elapsed, content=None):

        if code in self.codes:
            self.codes[code].append(url)
        else:
            self.codes[code] = [url]

        line = "%s,%d,%fs\n" % (url, code, elapsed)
        self.log.write(line)

        if code != 200:
            self.bad_log.write("%s,%s\n" % (code, url))

            if content:
                self.bad_log.write(content)

            self.bad_log.write("\n"+('='*78)+"\n")

    def close(self):
        self.elapsed = time() - self.start
        self.log.close()
        self.bad_log.close()
        qps = "%f QPS" % (self.queries/self.elapsed)
        print qps
        self.log.write(qps + "\n")
