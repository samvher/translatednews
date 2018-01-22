import feedparser as fp
from googletrans import Translator
from bs4 import BeautifulSoup
from urllib.parse import quote

trans = Translator()

class RegionInfo:
  def __init__(self, hl, ned, gl, lang):
    self.hl   = hl
    self.ned  = ned
    self.gl   = gl
    self.lang = lang

regions = {
  "The Netherlands": RegionInfo("nl",    "nl_nl", "NL", "nl"),
  "Indonesia":       RegionInfo("id",    "id_id", "ID", "id"),
  "Austria":         RegionInfo("de_at", "de_at", "AT", "de"),
  "Russia":          RegionInfo("ru",    "ru_ru", "RU", "ru")
  }

class NewsItem:
  def __init__(self, title, url_trans, url_orig, img):
    self.title     = title
    self.url_trans = url_trans
    self.url_orig  = url_orig
    self.img       = img

  def __str__(self):
    return "<a href=\"%s\">%s</a> <a href=\"%s\">(orig)</a>" \
           % (self.url_trans, self.title, self.url_orig)

def gtrans_url(source_lang, target_lang, url):
  template = "https://translate.google.com/translate?sl=%s&tl=%s&js=y&" + \
             "ie=UTF-8&u=%s&act=url"
  return template % (source_lang, target_lang, quote(url, safe=''))

def entry_img(feed_entry):
  try:
    summ = BeautifulSoup(e['summary'], 'html.parser')
    img  = summ.img['src']
  except:
    img  = None
  return img

def get_news(region_name, language):
  reg_info = regions[region_name]
  feed     = fp.parse("https://news.google.com/news/rss/?hl=%s&ned=%s&gl=%s"
                      % (reg_info.hl, reg_info.ned, reg_info.gl))

  news = []
  for e in feed['entries']:
    title     = trans.translate(e['title'], src=reg_info.hl, dest=language).text
    url_trans = gtrans_url(reg_info.lang, language, e['link'])
    url_orig  = e['link']
    img       = entry_img(e)
    news     += [NewsItem(title, url_trans, url_orig, img)]
  return news
