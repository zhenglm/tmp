#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
from scrapy.spiders import Spider
from scrapy.selector import Selector
from CompanySpider.items import CompanyspiderItem

class CompanySpider(Spider):
    name = "company_info"
    allowed_domains = ["lagou.com"]
    start_urls = []
    
    def start_requests(self):
            url_format = "https://www.lagou.com/gongsi/{0}.html"
            for index in range(10):
                self.start_urls.append(url_format.format(index))

            for url in self.start_urls:
                yield self.make_requests_from_url(url)
            
    def parse(self, response):
        selector = Selector(response)
        item = CompanyspiderItem()
        item['company_field'] = selector.xpath("//div[@class='item_content']/ul/li[1]/span").extract()
        item['company_size'] = selector.xpath("//div[@class='item_content']/ul/li[3]/span").extract()
        item['company_city'] = selector.xpath("//div[@class='item_content']/ul/li[4]/span").extract()
        item['company_stage'] = selector.xpath("//div[@class='item_content']/ul/li[2]/span").extract()
        #company info in json
        company_info = json.loads(selector.xpath("//script[@id='companyInfoData']").extract().body_as_unicode())
        item['company_name'] = company_info['coreInfo']['companyName']
        item['company_lng'] = company_info['coreInfo']['companyName']
        item['company_lat'] = company_info['coreInfo']['companyName']

        return item
