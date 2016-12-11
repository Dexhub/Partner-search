import scrapy


class QuotesSpider(scrapy.Spider):
    name = "frisky"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
            next_link = response.css('li.next a::attr(href)').extract_first()
        if next_link is not None:
                next_link = response.urljoin(next_link)
                yield scrapy.Request(next_link, callback=self.parse)
