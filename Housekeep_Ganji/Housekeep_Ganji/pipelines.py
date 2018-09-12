# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymysql

class HousekeepGanjiPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()
    def process_item(self, item, spider):
        if item['phone'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['phone'])  ##这里换成你自己的item["#"]
            return item


class MysqlPipeline():
    def __init__(self,host,database,user,password,port,crawl_type,crawl_type_clean):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.crawl_type = crawl_type
        self.crawl_type_clean = crawl_type_clean

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST'),
            database =  crawler.settings.get('MYSQL_DATABASE'),
            user = crawler.settings.get('MYSQL_USER'),
            password = crawler.settings.get('MYSQL_PASSWORD'),
            port = crawler.settings.get('MYSQL_PORT'),
            crawl_type = crawler.settings.get('CRAWL_TYPE'),
            crawl_type_clean = crawler.settings.get('CRAWL_TYPE_CLEAN')
        )

    def open_spider(self,spider):
        self.db = pymysql.connect(host=self.host,user=self.user,passwd=self.password,db=self.database,charset='utf8')
        self.cursor = self.db.cursor()

    def close_spider(self,spider):
        self.db.close()

    def process_item(self,item,spider):
            insert_sql = 'insert into spider_housekeep(s_address,type,title,label,service,address,phone,image) values (%s,%s,%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(insert_sql,(item['s_address'],self.crawl_type_clean,item['title'],item['label'],item['service'],item['address'],item['phone'],item['image']))
            self.db.commit()
            return item
