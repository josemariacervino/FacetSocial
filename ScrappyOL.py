from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
import os
import json
from os import remove
from scrapy.exceptions import CloseSpider
from multiprocessing.context import Process

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

log_enabled = config['DEBUG']['LOG_ENABLED']


################################
# Func. ScrappyOL: Scrapea la info de la pagina principal de OL
################################
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
            "USER-AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        }
        start_urls = ['https://www.facet.unt.edu.ar/sbe/ofertas-laborales/']

        def parse(self, response):
            sel = Selector(response)
            listaOfertas = sel.xpath(
                "//div[@id='primary']//div[@class='entry-content']//article[contains(@id, 'post-')]")

            for o in listaOfertas:
                item = ItemLoader(Oferta(), o)

                item.add_xpath("id", "@id")
                item.add_xpath("link", ".//h1/a/@href")
                item.add_xpath("titulo", ".//h1/a/text()")
                item.add_xpath("fecha", ".//div[@class='entry-meta']/a/time/text()")

                d = [x.xpath(".//text()").extract() for x in
                     o.xpath(".//div[@class='entry-content']//div[contains(@class,'siteorigin-widget')]")]
                item.add_value("descripcion", d)

                yield item.load_item()

    # CORRIENDO SCRAPY SIN LA TERMINAL

    archivo = "ofertas.json"

    if (os.path.isfile(archivo)):
        remove(archivo)

    def crawl():
        crawler = CrawlerProcess({
            'FEED_FORMAT': 'json',
            'FEED_URI': 'ofertas.json',
            'LOG_ENABLED': log_enabled
        })
        crawler.crawl(FIOfertasLaboralesSpider)
        crawler.start()

    processOL = Process(target=crawl)
    processOL.start()
    processOL.join()


################################
# Func. ScrappyOLInicial: Scrapea solo el titulo de la ultima Oferta Laboral
################################
def ScrappyOLInicial():
    class Oferta(Item):
        id = Field()
        titulo = Field()
        descripcion = Field()

    class FIOfertasLaboralesSpider(Spider):
        name = "OfertasSpider"

        custom_settings = {
            "USER-AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        }
        start_urls = ['https://www.facet.unt.edu.ar/sbe/ofertas-laborales/']

        def parse(self, response):
            sel = Selector(response)
            o = sel.xpath("//div[@id='primary']//div[@class='entry-content']//article[contains(@id, 'post-')][1]")

            item = ItemLoader(Oferta(), o)

            item.add_xpath("id", "@id")
            item.add_xpath("titulo", ".//h1/a/text()")

            d = [x.xpath(".//text()").extract() for x in
                 o.xpath(".//div[@class='entry-content']//div[contains(@class,'siteorigin-widget')]")]
            item.add_value("descripcion", d)

            yield item.load_item()

    # CORRIENDO SCRAPY SIN LA TERMINAL

    archivo = "ofertas.json"

    if (os.path.isfile(archivo)):
        remove(archivo)

    def crawl():
        crawler = CrawlerProcess({
            'FEED_FORMAT': 'json',
            'FEED_URI': 'ofertas.json',
            'LOG_ENABLED': log_enabled
        })
        crawler.crawl(FIOfertasLaboralesSpider)
        crawler.start()

    processOL = Process(target=crawl)
    processOL.start()
    processOL.join()

    #####################
    # Leo y devuelvo el titulo de la ultima pasantia publicada.
    #####################

    ruta = 'ofertas.json'
    with open(ruta) as contenido:

        # oferta = json.load(contenido)
        # o = oferta[0]
        # tituloOL = o["titulo"][0]

        des = ""
        ofertas = json.load(contenido)

        of = ofertas[0]
        idOL = of["id"][0]
        tituloOL = of["titulo"][0]
        descripcion = of["descripcion"][0]

        for d in descripcion:
            if ('\n\u2022' in d):
                des = des + d.strip("\t")
            elif ('\u2022' in d):
                des = des + "\n" + d.strip("\t")
            elif ('\u27a2' in d):
                des = des + "\n" + d.strip("\t")
            elif ('\n' in d):
                # des = des + "\n" + d.strip("\t")
                des = des + d.strip("\t")
            elif (':' in d):
                des = des + d.strip("\t") + "\n"
            else:
                des = des + d.strip("\t")

        return idOL, tituloOL, des