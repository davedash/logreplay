import re
import time

import settings


class Log:

    def __init__(self, filename):
        self.filename = filename
        self.start = None

    def etl(self):
        self.file = open(self.filename)
        log_re = re.compile(r'\[(.*) [+|-]\d{4}\] "(GET|POST) ([^"]*) [A-Z]+\/[0-9\.]+"')

        url_accept = None
        if 'URL_ACCEPT' in dir(settings):
            url_accept = re.compile(settings.URL_ACCEPT)

        url_deny = None
        if 'URL_DENY' in dir(settings):
            url_deny = re.compile(settings.URL_DENY)

        for line in self.file:
            try:
                (time_str, method, url) = log_re.search(line).groups()
            except:
                continue

            unixtime = time.mktime(time.strptime(
            time_str, '%d/%b/%Y:%H:%M:%S'))

            if method == 'POST':
                continue

            if url_accept and not url_accept.search(url):
                continue

            if url_deny and url_deny.search(url):
                continue

            if not self.start:
                self.start = int(unixtime)

            yield {'time': int(unixtime), 'url': url}

    def close(self):
        self.file.close()