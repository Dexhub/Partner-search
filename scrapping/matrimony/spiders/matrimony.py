# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest

class LinkedinSpider(CrawlSpider):
    name = 'dev_matrimony'
    #allowed_domains = ['www.linkedin.com/in/']
    start_urls = 'http://devanshmatrimony.com/advance_result_new.php'
    #login_url = 'https://www.linkedin.com/uas/login'

    def start_requests(self):
        yield Request(
                url=self.login_url,
                callback=self.parse_items,
                dont_filter=True
        )

    def parse_items(self, response):
        self.log('We got data!')
        yield {
                'name': response.css("span.full-name::text").extract_first(),
                'title': response.css("div.headline-container::text").extract_first()
            }
        next_links = response.css("ol.discovery-results a::attr(href)").extract()
        if next_links:
            for url in next_links:
                yield scrapy.Request(url, callback=self.parse_items_1)

    def parse_items_1(self, response):
        yield {
                'name': response.css("span.full-name::text").extract_first(),
                'title': response.css("div.headline-container::text").extract_first()
            }
