# -*- coding: utf-8 -*-
import scrapy
from proxy.items import ProxyItem


class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn']
    for i in range(2,21):
        start_urls.append('http://www.xicidaili.com/nn/%d/' % i)

    def parse(self, response):
        crawl_items = response.xpath('//tr[@class]')
        # print(items)
        item = ProxyItem()
        for crawl_item in crawl_items:
            item['ip'] = crawl_item.xpath('./td[2]/text()').extract()
            item['port'] = crawl_item.xpath('./td[3]/text()').extract()
            item['area'] = crawl_item.xpath('./td[4]/a/text()').extract()
            item['ip_type'] = crawl_item.xpath('./td[6]/text()').extract()
            yield item

        # print(item)