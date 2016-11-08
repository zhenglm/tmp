#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from CompanyGanji.items import CompanyganjiItem

class company_ganji(Spider):
    name = "company_ganji"
    allowed_domains = ["ganji.com"]
    start_urls = []
    
    def start_requests(self):
            url_format = "http://www.ganji.com/gongsi/{0}/"
            for index in range(44000000):
                self.start_urls.append(url_format.format(index))

            for url in self.start_urls:
                yield self.make_requests_from_url(url)
            
    def parse(self, response):
        hxSelector = HtmlXPathSelector(response)
        item = CompanyganjiItem()

        item['company_name'] = hxSelector.select("//div[@class=\"c-introduce\"]/ul/li[1]/text()").extract_first().strip()
        item['company_field'] = hxSelector.select("//div[@class=\"c-introduce\"]/ul/li[3]/a/text()").extract_first().strip()
        item['company_size'] = hxSelector.select("//div[@class=\"c-introduce\"]/ul/li[2]/text()").extract_first().strip()
        item['company_type'] = hxSelector.select("//div[@class=\"c-introduce\"]/ul/li[4]/a/text()").extract_first().strip()
        item['company_address'] = hxSelector.select("//div[@class=\"c-introduce\"]/ul/li[7]/text()").extract_first().strip()
        item['company_contact'] = hxSelector.select("//div[@class=\"c-introduce\"]/ul/li[5]/text()").extract_first().strip()
        item['company_phone'] = "img"
        #company info in json
        #company_info = json.loads(hxSelector.select("//script[@id='companyInfoData']").extract().body_as_unicode())
        #item['company_name'] = company_info['coreInfo']['companyName']
        #item['company_lng'] = company_info['coreInfo']['companyName']
        #item['company_lat'] = company_info['coreInfo']['companyName']

        return item
