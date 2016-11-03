# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanylagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #公司名称
    company_name = Field()
    #公司领域
    company_field = Field()
    #公司规模
    company_size = Field()
    #公司所在城市
    company_city = Field()
    #公司阶段
    finance_stage = Field()
    #公司经度
    company_lng = Field()
    #公司纬度
    company_lat = Field()
