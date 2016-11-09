# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CompanyganjiItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #公司名称
    company_name = Field()
    #公司行业
    company_field = Field()
    #公司规模
    company_size = Field()
    #公司类型
    company_type = Field()
    #公司地址
    company_address = Field()
    #公司联系人
    company_contact = Field()
    #联系人电话
    company_phone = Field()
    #公司经纬度
    company_lnglat = Field()
    #公司招聘职位
    company_jobs_info = Field()
