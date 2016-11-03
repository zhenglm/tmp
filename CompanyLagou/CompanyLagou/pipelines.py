# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CompanylagouPipeline(object):
    def process_item(self, item, spider):
        def __init__(self):
        self.file = codecs.open('/home/zhengliming/company_spider/crawler//result.dat', mode='wb',encoding='utf-8')

    def process_item(self, item, spider):
		if item['company_city']:
        	line = json.dumps(dict(item)) + '\n'
        	self.file.write(line.decode("unicode_escape"))

        return item
