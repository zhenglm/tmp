#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
from scrapy.spiders import Spider
from scrapy.selector import Selector
from CompanyLagou.items import CompanylagouItem

class company_lagou(Spider):
    name = "company_lagou"
    allowed_domains = ["lagou.com"]
    start_urls = []
    
    def start_requests(self):
            url_format = "https://www.lagou.com/gongsi/{0}.html"

            for index in range(70000):
                self.start_urls.append(url_format.format(index))

            for url in self.start_urls:
                yield self.make_requests_from_url(url)

            
    def parse(self, response):
        selector = Selector(text=response.body)
        item = CompanylagouItem()
        item['company_field'] = selector.xpath("//div[@class='item_content']/ul/li[1]/span/text()").extract_first()
        item['company_size'] = selector.xpath("//div[@class='item_content']/ul/li[3]/span/text()").extract_first()
        item['company_city'] = selector.xpath("//div[@class='item_content']/ul/li[4]/span/text()").extract_first()
        item['finance_stage'] = selector.xpath("//div[@class='item_content']/ul/li[2]/span/text()").extract_first()
        #company info in json
	company_info_list = selector.xpath("//script[@id='companyInfoData']/text()").extract()
        #print company_info_list
	
	if company_info_list:
		company_info = json.loads(company_info_list[0])
		item['company_name'] = company_info['coreInfo']['companyName']
		item['company_lng'] = company_info['addressList'][0]['lng']
		item['company_lat'] = company_info['addressList'][0]['lat']
	return item
