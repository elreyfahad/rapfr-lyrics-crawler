# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
import logging
from rapfr.items import RapFrItem

class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    ##allowed_domains = ['https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Rappeur_fran%C3%A7ais']
    start_urls = ['http://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Rappeur_fran%C3%A7ais']

    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        #'ITEM_PIPELINES': {'rap_fr.pipelines.RapFrPipeline': 1}, # Used for pipeline 1
        'FEED_FORMAT':'json', # Used for pipeline 2
        'FEED_URI': 'file.json', # Used for pipeline 2
        'FEED_EXPORT_ENCODING': 'utf-8' #encodage


    }

    

    def parse(self, response):

        il=ItemLoader(item=RapFrItem(),response=response)
            #author=quote.css("span small.author::text").get()
             
        il.add_css("artist","div.mw-category-group ul li a::text")
        #il.add_css("author","div.quote span small.author")
        
        #yield {
            #"artist": response.css("div.mw-category-group ul li a::text").extract()
            #}


        #suivie des liens
        path=response.xpath("//div[@id='mw-pages']/a/@href").get() #recupere le liens du page suivant
        text=response.xpath("//div[@id='mw-pages']/a/text()").get() #recupere le text du balise "a" de ce lien
        

        if path is not None and text=="page suivante" :

            next_page="https://fr.wikipedia.org"+path
                
            yield response.follow(next_page,callback=self.parse)

        
        

            
        #return il.load_item()
