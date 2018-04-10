# -*- coding: utf-8 -*-
import scrapy
from shiyanlourepository.items import ShiyanlourepositoryItem


class RunSpider(scrapy.Spider):
    name = 'run'
    # allowed_domains = ['github.com']
    start_urls = ['http://github.com/']

    @property
    def start_urls(self):
        url_template = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return [url_template.format(i) for i in range(1, 5)]

    def parse(self, response):
        for r in response.css('li[itemtype="http://schema.org/Code"]'):
            item = ShiyanlourepositoryItem()
            item['name'] = r.css('a[itemprop="name codeRepository"]::text').re_first('\S+')
            item['update_time'] = r.css('relative-time::attr("datetime")').extract_first()
            uri = r.css('a[itemprop="name codeRepository"]::attr("href")').extract_first()
            request = scrapy.Request(url=response.urljoin(uri), callback=self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        item['commits'] = response.xpath('//svg[@class="octicon octicon-history"]/following-sibling::*[1]/text()').re_first('\S+').replace(',', '')
        item['branches'] = response.xpath('//svg[@class="octicon octicon-git-branch"]/following-sibling::*[1]/text()').re_first('\S+').replace(',', '')
        item['releases'] = response.xpath('//svg[@class="octicon octicon-tag"]/following-sibling::*[1]/text()').re_first('\S+').replace(',', '')
        yield item