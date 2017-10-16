# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

# 使用redis去重
# from scrapy.dupefiters import RFPDupeFilter

from DuZhe.items import DuzheItem


class DuzheSpider(RedisCrawlSpider):
    name = 'duzhe'
    redis_key = "DuzheSpider:start_urls"
    #allowed_domains = ['www.52duzhe.com']

    rules = (
        Rule(LinkExtractor(allow=r'\d+_\d+/index.html'), callback='parse_item', follow=False),
    )

    def __init__(self, *args, **kwargs):
        super(DuzheSpider, self).__init__(*args, **kwargs)
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))

    def parse_item(self, response):
        items = []
        essayList = response.xpath('//table[@class="booklist"]//tr[not(@class="category")]')
        for essay in essayList:
            item = DuzheItem()

            try:
                item['title'] = essay.xpath('./td[@class="title"]/a/text()').extract()[0]
            except:
                continue
            try:
                item['author'] = essay.xpath('./td[@class="author"]/@title').extract()[0]
            except:
                item['author'] = "None"
            item['source'] = essay.xpath('./td[@class="source"]/@title').extract()[0]
            item['topic'] = essay.xpath('./preceding-sibling::tr[@class="category"]/td/text()').extract()[-1]
            item['journal'] = essay.xpath('//h1/text()').extract()[0][:-2]

            contentLink = essay.xpath('./td[@class="title"]/a/@href').extract()[0]
            responseUrl = re.sub('index.html', contentLink, response.url)
            item['link'] = responseUrl

            items.append(item)

        for item in items:
            yield scrapy.Request(url=item['link'], meta={'meta_1': item}, callback=self.parse_Content)

    def parse_Content(self, response):

        item = response.meta['meta_1']
        contentList = response.xpath('//div[@class="blkContainerSblkCon"]/p/text()').extract()
        content = ""
        for contentOne in contentList:
            content += contentOne
        item['Content'] = content
        yield item


