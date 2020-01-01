# -*- coding: utf-8 -*-
import scrapy


class ApiSpider(scrapy.Spider):
    name = 'api'
    #allowed_domains = ['api.genius.com']
    start_urls = ['http://api.genius.com']

    def parse(self, response):
        pass
