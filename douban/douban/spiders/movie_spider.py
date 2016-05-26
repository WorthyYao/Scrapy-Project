# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from douban.items import DoubanmoiveItem
import logging

class MoiveSpider(CrawlSpider):
    name="doubanmoive"
    allowed_domains=["movie.douban.com"]
    start_urls=["https://movie.douban.com/top250"]
    # for i in range(0,250,25):
    #     start_urls.append("https://movie.douban.com/top250?start=%d&filter=" %i)
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.*'))),
        Rule(SgmlLinkExtractor(allow=(r'https://movie.douban.com/subject/\d+')),callback="parse_item"),
    ]

    def parse_item(self,response):
        logging.info('parsed ' + str(response))
        sel=Selector(response)
        item=DoubanmoiveItem()
        item['name']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()

        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score']=sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        item['director']=sel.xpath('//*[@id="info"]/span[1]/a/text()').extract()
        item['classification']= sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor']= sel.xpath('//*[@id="info"]/span[3]/a[1]/text()').extract()
        return item
