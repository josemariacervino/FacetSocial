from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
import os
from os import remove
from scrapy.exceptions import CloseSpider
from multiprocessing.context import Process

def ScrappyPPS():
  
  class Pasantia(Item):
    id = Field()
    link = Field()
    titulo = Field()
    fecha = Field()
    descripcion = Field()

  class FIPasantiasSpider(Spider):
    name = "PasantiasSpider"

    custom_settings = {
        "USER-AGENT":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
    }
    start_urls = ['https://www.facet.unt.edu.ar/sbe/pasantias-y-pps/']

    def parse(self, response):
        sel = Selector(response)
        listaPasantia = sel.xpath("//div[@id='panel-194-0-0-0']//article[contains(@id, 'post-')]")

        i = 0
        
        for p in listaPasantia:
          item = ItemLoader(Pasantia(), p)
  
          item.add_value("id", i)
          item.add_xpath("link", ".//h1/a/@href")
          item.add_xpath("titulo", ".//h1/a/text()")
          item.add_xpath("fecha", ".//div[@class='entry-meta']/a/time/text()")
  
          x = p.xpath(".//div[@class='entry-content']//div[contains(@class,'siteorigin-widget')]/p/span/text()")
  
          if x == []:
              item.add_xpath("descripcion", ".//div[@class='entry-content']//div[contains(@class,'siteorigin-widget')]/p/text()")
          else:
              item.add_xpath("descripcion", ".//div[@class='entry-content']//div[contains(@class,'siteorigin-widget')]/p/span/text()")
  
          i += 1
  
          yield item.load_item()


#CORRIENDO SCRAPY SIN LA TERMINAL

  archivo = "pasantias.json"

  if (os.path.isfile(archivo)):
    remove(archivo)

  def crawl():
    crawler = CrawlerProcess({
      'FEED_FORMAT': 'json',
      'FEED_URI': 'pasantias.json'
    })
    crawler.crawl(FIPasantiasSpider)
    crawler.start()
  
  processPPS = Process(target=crawl)
  processPPS.start()
  processPPS.join()