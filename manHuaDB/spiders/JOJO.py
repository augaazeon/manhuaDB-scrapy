# -*- coding: utf-8 -*-
from scrapy import Spider,Request
import json
from urllib.parse import urljoin
from manHuaDB.items import DBItem

class JojoSpider(Spider):
    name = 'JOJO'
    allowed_domains = ['manhuadb.com']
    start_urls = ['https://www.manhuadb.com/manhua/128/']

    def parse(self, response):
        # for chapter in response.xpath('//li[@class="sort_div"]/a/@href').extract():
            # chapter_title = chapter.xpath('./@data-sort').extract_first()
            # chapter_url = chapter.xpath('./a/@href').extract_first()
            # yield Request(chapter_url,callback=self.parse_item)

        chapter = response.xpath('// script[ @ type = "application/ld+json"][2]/text()').extract_first()#从<script>提取章节信息和url
        data = json.loads(chapter)
        chapter_item= data["hasPart"][0]["hasPart"]
        for info in chapter_item:
            chapter_title = info["issueNumber"]
            if chapter_title:
                chapter_url = info["url"]
                yield Request(chapter_url,callback=self.parse_item)


    def parse_item(self,response):
        chapter_title = response.xpath('//h2/text()').extract_first()
        for page_info in response.xpath('//option'):
            page_url = page_info.xpath('./@value').extract_first()
            page_num = page_info.xpath('./text()').extract_first()
            yield Request(urljoin('https://www.manhuadb.com',page_url),meta={"chapter_title":chapter_title,"page_num":page_num},callback=self.parse_image)
            # print(chapter_title,page_num,page_url)

    def parse_image(self,response):
        item = DBItem()
        item['name'] = self.name
        item['chapter_title'] = response.meta['chapter_title']
        item['page_num'] = response.meta['page_num']
        item['image_url'] = urljoin('https://www.manhuadb.com',response.xpath('//img[@class="img-fluid"]/@src').extract_first())
        yield item