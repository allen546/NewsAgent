from nntplib import NNTP, NNTP_SSL, decode_header
from urllib.request import urlopen
from urllib.parse import urljoin
import textwrap, bs4, abc
try:
    from .newsitems import *
except:
    from newsitems import *
    
KNOWN_NNTP_SERVERS = ["secure.news.easynews.com", "freenews.netfront.net", "news.easynews.com"]

class SourceBase(abc.ABC):
    @abc.abstractmethod
    def get_items(self):
        pass

class WebSourceBase(SourceBase):
    def __init__(self, n=5):
        self.n = n

class NNTPSource(SourceBase):
    class NewsGroupDoesNotExist(Exception):
        pass
    """
    A news source that retrieves news items from an NNTP group.
    """
    def __init__(self, group, howmany):
        self.group = group
        self.howmany = howmany

    def get_items(self):
        for servername in KNOWN_NNTP_SERVERS:
            try:
                try:
                    server = NNTP_SSL(servername)
                except:
                    server = NNTP(servername)
                resp, count, first, last, name = server.group(self.group)
                start = last - self.howmany + 1
                resp, overviews = server.over((start, last))
                for id, over in overviews:
                    title = decode_header(over['subject'])
                    resp, info = server.body(id)
                    body = '\n'.join(line.decode('utf-8')
                                     for line in info.lines) + '\n\n'
                    yield NewsItem(title, body, "NNTP NewsGroup "+self.group)
                server.quit()
                break
            except: continue
        else:
            raise self.NewsGroupDoesNotExist(f"Newsgroup {self.group} Does not exist")
        return []

class FoxNewsSource(WebSourceBase):
    def get_items(self):
        r = urlopen("https://www.foxnews.com/")
        resp = r.read()
        b = bs4.BeautifulSoup(markup=resp, features="html.parser")
        matches = b.select("h2[class='title'] > a[href]")[:self.n]
        h = {}
        for match in matches:
            h[match.text]=match.get("href")
            if not h[match.text].startswith("https://"):
                h[match.text] = "https:"+match.get("href")
            yield NewsItem(match.text, "Link: {}".format(h[match.text]), "Fox News")
class SinaNewsSource(WebSourceBase):
    def get_items(self):
        r = urlopen("https://news.sina.com.cn/")
        resp = r.read()
        b = bs4.BeautifulSoup(markup=resp, features="html.parser")
        matches = b.select("a[class='linkNewsTopBold']")[:self.n]
        h = {}
        for match in matches:
            h[match.text]=match.get("href")
            if not h[match.text].startswith("https://"):
                h[match.text] = "https:"+match.get("href")

            rb = urlopen(h[match.text]).read()
            bs = bs4.BeautifulSoup(markup=rb, features="html.parser")
            matches2 = bs.select("div[class='article']")[0]
            text = "\n".join(m.text for m in matches2.select("p"))
            n = 0
            temp= ""
            for i in text:
                n += 1
                temp += i
                if n == 75:
                    n = 0
                    temp += "\n"
            yield NewsItem(match.text, temp+"\nLink: {}".format(h[match.text]), "Sina News")