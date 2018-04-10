# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from shiyanlourepository.Models import engine, Repository
from datetime import datetime


class ShiyanlourepositoryPipeline(object):
    def process_item(self, item, spider):
        item['update_time'] = item['update_time'].replace('T', ' ').replace('Z', '')
        item['update_time'] = datetime.strptime(item['update_time'], "%Y-%m-%d %H:%M:%S")
        item['commits'] = int(item['commits'])
        item['branches'] = int(item['branches'])
        item['releases'] = int(item['releases'])
        self.session.add(Repository(**item))
        return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

