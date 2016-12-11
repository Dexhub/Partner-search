# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest

class LinkedinSpider(CrawlSpider):
    name = 'linkedin'
    #allowed_domains = ['www.linkedin.com/in/']
    start_urls = 'https://www.linkedin.com/in/himanshu1410/'
    login_url = 'https://www.linkedin.com/uas/login'

    def start_requests(self):
        yield Request(
                url=self.login_url,
                callback=self.after_login,
                dont_filter=True
        )

    def after_login(self, response):
        # check login succeed before going on
        return FormRequest.from_response(
                response,
                formdata={'session_key': 'coverme7879@gmail.com', 'session_password': 'coverme12345'},
                callback=self.check_login_response)

    def check_login_response(self, response):
        if 'Sign Out' in response.body:
            self.log('Hi, this is an item page!')
            yield Request(
                url=self.start_urls,
                callback=self.parse_items,
                dont_filter=True
            )
            return
        else:
            self.log('Failed')

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
