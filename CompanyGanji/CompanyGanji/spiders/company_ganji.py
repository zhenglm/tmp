#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import json
from scrapy.spiders import Spider
from scrapy.selector import Selector
from CompanyGanji.items import CompanyganjiItem
from scrapy.http import Request

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
            
    def parse_lnglat(self, response):
        item = response.meta['item']
        #print response.body
        zbSelector = Selector(text=response.body)
        #print response.body
        #company lnglat in json
        company_info_list = zbSelector.xpath("//div[@id='baidu-map']/@data-ref").extract_first()
        if company_info_list:
            company_info = json.loads(company_info_list)
        if company_info != None and 'lnglat' in company_info:
            item['company_lnglat'] = company_info['lnglat']
        else:
            item['company_lnglat'] = None

        return item 

    def parse(self, response):
        hxSelector = Selector(text=response.body)
        #print "###################"
        #print(response.body)

        item = CompanyganjiItem()

        c_name = hxSelector.xpath("//div[@class=\"c-introduce\"]/ul/li[1]/text()").extract_first()
        if c_name != None:
            item['company_name'] = c_name.strip()
        else:
            item['company_name'] = None
        item['company_field'] = hxSelector.xpath("//div[@class=\"c-introduce\"]/ul/li[3]/a/text()").extract_first()
        item['company_size'] = hxSelector.xpath("//div[@class=\"c-introduce\"]/ul/li[2]/text()").extract_first()
        item['company_type'] = hxSelector.xpath("//div[@class=\"c-introduce\"]/ul/li[4]/a/text()").extract_first()
        item['company_address'] = hxSelector.xpath("//div[@class=\"c-introduce\"]/ul/li[7]/text()").extract_first()
        item['company_contact'] = hxSelector.xpath("//div[@class=\"c-introduce\"]/ul/li[5]/text()").extract_first()
        item['company_phone'] = "img"

        jobs_info_dict_list = []
        jobs_list = hxSelector.xpath("//div[@class=\"common-list-tab mt-5\"]/table/tbody/tr")
        if len(jobs_list) > 1:
            for index in range(2, len(jobs_list)+1):
                jobs_info_dict = {}
                str_xpath = "//div[@class=\"common-list-tab mt-5\"]/table/tbody/tr[{0}]"
                str_res_xpath = str_xpath.format(index)
                jobs_info_dict['job_name'] = hxSelector.xpath(str_res_xpath + "/td[1]/a/text()").extract_first()
                jobs_info_dict['job_salary'] = hxSelector.xpath(str_res_xpath + "/td[2]/text()").extract_first()
                jobs_info_dict['job_edu'] = hxSelector.xpath(str_res_xpath + "/td[3]/text()").extract_first()
                jobs_info_dict_list.append(jobs_info_dict)

            item['company_jobs_info'] = jobs_info_dict_list
        else:
            item['company_jobs_info'] = None


        company_jobs = hxSelector.xpath("//a[@post-type][1]/@href").extract_first()
        #print company_jobs
        if company_jobs != None:
            if company_jobs.startswith('h'):
                yield Request(company_jobs, meta={'item':item}, callback=self.parse_lnglat)
            else:
                yield Request("http://www.ganji.com" + company_jobs, meta={'item':item}, callback=self.parse_lnglat)
        else:
            item['company_lnglat'] = None
            yield item
