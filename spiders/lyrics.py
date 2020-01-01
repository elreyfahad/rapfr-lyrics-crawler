# -*- coding: utf-8 -*-
import scrapy
import re
import logging
import json
from scrapy.htpp import Request


class LyricsSpider(scrapy.Spider):
    name = 'lyrics'
    custom_settings = {
        
        'LOG_LEVEL': logging.WARNING,
        #'ITEM_PIPELINES': {'rap_fr.pipelines.RapFrPipeline': 1}, # Used for pipeline 1
        'FEED_FORMAT':'csv', # Used for pipeline 2
        'FEED_URI': 'lyrics.csv', # Used for pipeline 2
        'FEED_EXPORT_ENCODING': 'utf-8', #encodage
        'COOKIES_ENABLED ': False, # Disable cookies (enabled by default)
    
        'ROBOTSTXT_OBEY': False ,# Obey robots.txt rules
        #les headers par defauts des requets https
        'DEFAULT_REQUEST_HEADERS' : {'Authorization' :'Bearer jA72FWfI5KDlnqQm3C1Fzbx58ocWHFBM64gXtQGtf-gpTf-xZFAbkS_MtDbLRv_0'} 


    }

    def start_requests(self):

        #url="https://api.genius.com/songs/"

        #lecture du fichier json contenant les artistes scraper dans wikipedia
        with open("idson.json",encoding="utf8") as json_file:
            data = json.load(json_file)
            for p in data:
                song_id=p["song_id"]
                lyrics_links=p["lyrics_link"]
                
                
                
                yield Request(lyrics_links,callback=self.getLyrics,meta={"song_id":song_id,"lyrics_link":lyrics_links})
                
                
                
    
    #fonction qui recuperes les lyrics
    def getLyrics(self,response):
        
        #js=json.loads(response.text)
        
        
        song_id=response.meta.get("song_id")
        lyrics_links=response.meta.get("lyrics_link")

        
        rep=response.xpath("//div[@class='lyrics']/p").getall()
        
        if len(rep)>1:
            lyrics=rep[1]
        else:
            lyrics=rep
        
        
        lyrics=re.sub("<[^>]*>","",lyrics)  #supprime les balise html
        
        lyrics=re.sub("\n"," ",lyrics) #supprime les retours a la ligne
        
        lyrics=re.sub(r"\[[^\]]*\]","",lyrics) #supprime les text entre crochet
        
        
            
        yield {"song_id":song_id,"lyrics_link":lyrics_links,"lyrics":lyrics}


    