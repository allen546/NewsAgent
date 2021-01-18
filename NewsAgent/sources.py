from nntplib import NNTP, decode_header
from urllib.request import urlopen
import textwrap
try:
    from .newsitems import *
except:
    from newsitems import *
    
KNOWN_NNTP_SERVERS = ["secure.news.easynews.com", "freenews.netfront.net", "news.easynews.com"]

class SourceBase:
    def get_items(self):
        pass

class NNTPSource(SourceBase):
    """
    A news source that retrieves news items from an NNTP group.
    """
    def __init__(self, group, howmany):
        self.group = group
        self.howmany = howmany

    def get_items(self):
        for servername in KNOWN_NNTP_SERVERS:
            try:
                server = NNTP(servername)
                resp, count, first, last, name = server.group(self.group)
                start = last - self.howmany + 1
                resp, overviews = server.over((start, last))
                for id, over in overviews:
                    title = decode_header(over['subject'])
                    resp, info = server.body(id)
                    body = '\n'.join(line.decode('latin1')
                                     for line in info.lines) + '\n\n'
                    yield NewsItem(title, body, "NNTP NewsGroup "+self.group)
                server.quit()
                break
            except: continue
        return []

class SimpleWebSource(SourceBase):
    """
    A news source that extracts news items from a web page using regular
    expressions.
    """
    def __init__(self, url, title_pattern, body_pattern, encoding='utf8'):
        self.url = url
        self.title_pattern = re.compile(title_pattern)
        self.body_pattern = re.compile(body_pattern)
        self.encoding = encoding

    def get_items(self):
        try:
            text = urlopen(self.url).read().decode(self.encoding)
            titles = self.title_pattern.findall(text)
            bodies = self.body_pattern.findall(text)
            for title, body in zip(titles, bodies):
                yield NewsItem(title, textwrap.fill(body) + '\n', "WebPage "+self.url)
        except:
            return []
