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

def ScrappyOL():
  
  class Oferta(Item):
    id = Field()
    link = Field()
    titulo = Field()
    fecha = Field()
    descripcion = Field()

  class FIOfertasLaboralesSpider(Spider):
    name = "OfertasSpider"

    custom_settings = {
        "USER-AGENT":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    start_urls = ['https://www.facet.unt.edu.ar/sbe/ofertas-laborales/']

    def parse(self, response):
        sel = Selector(response)
        oferta = sel.xpath("//div[@id='primary']//div[@class='entry-content']//article[contains(@id, 'post-')][1]")
        i = 0

        o = oferta
        item = ItemLoader(Oferta(), o)

        item.add_value("id", i)
        item.add_xpath("link",".//h1/a/@href")
        item.add_xpath("titulo", ".//h1/a/text()")
        item.add_xpath("fecha", ".//div[@class='entry-meta']/a/time/text()")

        x = o.xpath(".//div[@class='entry-content']//div[contains(@class,'siteorigin-widget')]/p/span/text()")

        if x == []:
            item.add_xpath("descripcion", ".//div[@class='entry-content']//div[contains(@class,'siteorigin-widget')]/p/text()")
        else:
            item.add_xpath("descripcion", ".//div[@class='entry-content']//div[contains(@class,'siteorigin-widget')]/p/span/text()")

        i += 1

        yield item.load_item()


#CORRIENDO SCRAPY SIN LA TERMINAL

  archivo = "ofertas.json"

  if (os.path.isfile(archivo)):
    remove(archivo)

  def crawl():
    crawler = CrawlerProcess({
      'FEED_FORMAT': 'json',
      'FEED_URI': 'ofertas.json'
    })
    crawler.crawl(FIOfertasLaboralesSpider)
    crawler.start()
  
  process = Process(target=crawl)
  process.start()
  process.join()