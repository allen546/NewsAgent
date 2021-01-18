from nntplib import NNTP, decode_header
from urllib.request import urlopen
from urllib.parse import urljoin
import textwrap, bs4
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

class FoxNewsSource(SourceBase):
    def __init__(self, n=10):
        self.n=n
    def get_items(self):
        r = urlopen("https://www.foxnews.com/")
        resp = r.read()
        b = bs4.BeautifulSoup(markup=resp, features="html.parser")
        matches = b.select("h2[class='title'] > a[href]")[:self.n]
        h = {}
        for match in matches:
            h[match.text]=match.get("href")
        for match in h:
            yield NewsItem(match, "Link: {}".format("https:"+h[match]), "Fox News")
