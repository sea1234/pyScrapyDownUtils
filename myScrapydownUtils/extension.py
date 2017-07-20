# -*- coding: utf-8 -*-
__author__ = 'cht'


from scrapy import signals
from scrapy.exceptions import NotConfigured

import downuitls


class SpiderOpenCloseLogging(object):

    def __init__(self, item_count):
        self.item_count = item_count
        # self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        # get the number of items from settings
        # item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)
        # my_name=cls.__name__
        # instantiate the extension object 实例化扩展对象
        ext = cls(cls.__name__)
        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        # return the extension object
        return ext

    def spider_opened(self, spider):
        spider.log("opened spider %s" % spider.name)

    def spider_closed(self, spider):
        spider.log("closed spider %s" % spider.name)

        print u'spider已关闭正在准备开始下载'
        Redis = downuitls.dowork(spider.name)
        print u'下载完成正在准备删除redis数据'
        ##  删除数据库
        Redis.delete(spider.name)

    def item_scraped(self, item, spider):
        # self.items_scraped += 1
        # if self.items_scraped % self.item_count == 0:
        #     spider.log("scraped %d items" % self.items_scraped)
        pass

