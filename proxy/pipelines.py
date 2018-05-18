# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class ProxyPipeline(object):
    update_count = 0

    def __init__(self, mongo_db):
        # self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        print('################')
        print('本次更新%d条数据' % self.update_count)
        print('################')
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        if not self.db[collection_name].update_one({'ip':dict(item)['ip']}, {'$set':dict(item)}, upsert=True).matched_count:
            self.update_count += 1
        return item
