# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import requests
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
import time
import base64
import sys


class HousekeepGanjiSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HousekeepGanjiDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent


# class ProxyMiddleware(object):
#     def __init__(self,proxy_url):
#         self.logger = logging.getLogger(__name__)
#         self.proxy_url = proxy_url
#
#     def get_random_proxy(self):
#         try:
#             response  = requests.get(self.proxy_url)
#             if response.status_code == 200:
#                 proxy = response.text
#                 return proxy
#         except Exception as e:
#             self.logger.warning("Error Occurred", e.args)
#             return False
#
#     # def process_request(self,request,spider):
#     #     if request.meta.get('retry_times'):
#     #         proxy = self.get_random_proxy()
#     #         if proxy:
#     #             uri = 'http://{proxy}'.format(proxy=proxy)
#     #             self.logger.debug('使用代理' + proxy)
#     #             request.meta['proxy'] = uri
#
#     #独享代理  ---一次仅有一个
#     # def process_request(self,request,spider):
#     #     uri = 'http://{proxy}'.format(proxy=self.proxy_url)
#     #     self.logger.debug('使用代理' + self.proxy_url)
#     #     request.meta['proxy'] = uri
#
#     def process_request(self, request, spider):
#         proxy = self.get_random_proxy()
#         if proxy:
#             uri = 'http://{proxy}'.format(proxy=proxy)
#             self.logger.debug('使用代理' + proxy)
#             request.meta['proxy'] = uri
#     #
#     # def process_response(self, request, response, spider):
#     #     if response.status >= 300:
#     #         proxy = self.get_random_proxy()
#     #         if proxy:
#     #             uri = 'http://{proxy}'.format(proxy=proxy)
#     #             self.logger.debug('使用代理' + proxy)
#     #             request.meta['proxy'] = uri
#     #             time.sleep(1.5)
#     #             return request
#     #     return response
#
#
#     @classmethod
#     def from_crawler(cls,crawler):
#         settings = crawler.settings
#         return cls(proxy_url=settings.get('PROXY_URL'))


####亿牛云
PY3 = sys.version_info[0] >= 3

def base64ify(bytes_or_str):
    if PY3 and isinstance(bytes_or_str, str):
        input_bytes = bytes_or_str.encode('utf8')
    else:
        input_bytes = bytes_or_str

    output_bytes = base64.urlsafe_b64encode(input_bytes)
    if PY3:
        return output_bytes.decode('ascii')
    else:
        return output_bytes

class ProxyMiddleware(object):
    def process_request(self, request, spider):
            # 代理服务器
        proxyHost = "p5.t.16yun.cn"
        proxyPort = "6445"

            # 代理隧道验证信息
        proxyUser = "16SMRAJZ"
        proxyPass = "288252"

        request.meta['proxy'] = "http://{0}:{1}".format(proxyHost,proxyPort)

            # 添加验证头
        encoded_user_pass = base64ify(proxyUser + ":" + proxyPass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

            # 设置IP切换头(根据需求)  一般用于要用cookies登陆以后完成相关操作
        # tunnel = random.randint(1,10000)
        # request.headers['Proxy-Tunnel'] = str(tunnel)