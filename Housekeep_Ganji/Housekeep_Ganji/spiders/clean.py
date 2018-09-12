# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import requests
import re

from scrapy.contrib.linkextractors import LinkExtractor
from ..items import  HousekeepGanjiItem

from scrapy.exceptions import CloseSpider
# from scrapy.linkextractors import LinkExtractor

class CleanSpider(scrapy.Spider):
    name = 'clean'
    allowed_domains = ['ganji.com']
    all_city = [
        "chaoyang",
        "kaifeng",
        "nanyang",
        "zz",
        "puer",
        "km",
        "honghe",
        "wenshan",
        "sy",
        "cs",
        "changde",
        "huaihua",
        "hengyang",
        "xuancheng",
        "bozhou",
        "huangshan",
        "luan",
        "hf",
        "fuyang",
        "wuhu",
        "linyi",
        "heze",
        "yantai",
        "yancheng",
        "su",
        "nj",
        "jinhua",
        "nb",
        "wenzhou",
        "jiaxing",
        "hz",
        "huzhou",
        "yuxi",
        "xiangtan",
        "foshan",
        "gz",
        "cq",
        "nn",
        "sh",
        "xiangyang",
        "tangshan",
        "anyang",
        "xinxiang",
        "chengde",
        "baoshan",
        "cc",
        "dandong",
        "yingkou",
        "hrb",
        "yueyang",
        "yongzhou",
        "weifang",
        "dongying",
        "suqian",
        "changzhou",
        "jian",
        "jxyichun",
        "zhangzhou",
        "dg",
        "wx",
        "shangrao",
        "jingzhou",
        "wh",
        "nc",
        "ganzhou",
        "sz",
        "jiujiang",
        "tj",
        "handan",
        "hengshui",
        "baoding",
        "qinhuangdao",
        "xinyang",
        "qujing",
        "dali",
        "anshan",
        "fz",
        "dl",
        "shanwei",
        "sjz",
        "cangzhou",
        "zhuzhou",
        "jingmen",
        "binzhou",
        "nanping",
        "xm",
        "yichang",
        "bj",
        "zhaotong",
        "loudi",
        "quanzhou",
        "shaoyang",
    ]
    start_urls = [
        'http://{city}.ganji.com/baojie/'.format(city=city) for city in all_city
    ]

    def __init__(self):
        self.img_list = []
        self.current_num = 0
        self.max_num = 6

    def parse(self, response):
        link = LinkExtractor(allow='/baojie/.*',
                             restrict_xpaths='//dl[@class="selitem selitem-area clearfix"]/dd[@class="posrelative w-area"]/a')
        links = link.extract_links(response)
        for i in links:
            self.city_name = re.split('\/', i.url)[-2]
            yield Request(i.url, callback=self.get_index, meta={'city_name': self.city_name, 'dont_redirect': True},dont_filter=True)

            ###获取各个地区的url下的详情页

    def get_index(self, response):
        city_name = response.meta['city_name']
        link = LinkExtractor(
            restrict_xpaths='//div[@class="leftBox"]//div[@class="list"]/ul/li[@class="list-img"]/div[@class="pic"]/a')
        links = link.extract_links(response)

        for i in links:
            yield Request(i.url, callback=self.get_message,
                          meta={'city_name': city_name, 'dont_redirect': True},dont_filter=True)

            ###解析详情页

    def get_message(self, response):
        item = HousekeepGanjiItem()
        item['s_address'] = response.meta['city_name']
        item['title'] = response.xpath('//div[@class="d-top-area"]//h1[@class="p1"]/text()').extract_first().strip()
        lable = response.xpath(
            '//div[@class="d-top-info"]/ul//span[contains(text(),"服务特色")]/following-sibling::div//text()').extract_first()
        if lable:
            item['label'] = lable
        else:
            item['label'] = ''
        service = response.xpath(
            '//div[@class="d-top-info"]/ul//span[contains(text(),"提供服务")]/following-sibling::div/a/text()').extract()
        if service:
            item["service"] = "".join(service)
        else:
            item['service'] = ''
        item['address'] = "".join(response.css('.d-top-info > ul > li:nth-last-child(2) > div > p ::text').extract())
        s_phone = response.xpath(
            '//div[@class="d-top-info"]//li[@class="tel-num clearfix"]/div[@class="tcon pos-r"]/a/@gjalog').extract_first().strip()
        item['phone'] = re.findall('.*?phone=(.*?)@.*?', s_phone)[0]
        item['image'] = response.xpath('//div[@class="d-top-area"]//div[@class="pic"]/img/@src').extract_first().strip()
        yield item
