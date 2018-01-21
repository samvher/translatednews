import feedparser as fp
from googletrans import Translator
from bs4 import BeautifulSoup

trans = Translator()

class RegionInfo:
  def __init__(self, hl, ned, gl):
    self.hl = hl
    self.ned = ned
    self.gl = gl

regions = {
  "nl": RegionInfo("nl", "nl_nl", "NL"),
  "id": RegionInfo("id", "id_id", "ID"),
  "at": RegionInfo("de_at", "de_at", "AT"),
  "ru": RegionInfo("ru", "ru_ru", "RU")
  }

class NewsItem:
  def __init__(self, title, url, img):
    self.title = title
    self.url = url
    self.img = img

  def __str__(self):
    return "<a href=\"%s\">%s</a>" % (self.url, self.title)

def get_news(region_name, language):
  reg_info = regions[region_name]
  feed = fp.parse("https://news.google.com/news/rss/?hl=%s&ned=%s&gl=%s"
                  % (reg_info.hl, reg_info.ned, reg_info.gl))

  news = []
  for e in feed['entries']:
    title = trans.translate(e['title'], src=reg_info.hl, dest=language).text
    url = e['link']
    try:
      summ = BeautifulSoup(e['summary'], 'html.parser')
      img = summ.img['src']
    except:
      img = None
    news += [NewsItem(title, url, img)]

  return news
