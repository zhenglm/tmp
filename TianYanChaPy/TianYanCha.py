# -*- coding:utf-8 -*- 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import six.moves.urllib as urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class TianYanCha(object):
	"""docstring for TianYanCha"""
	def __init__(self, sucPath, failedPath):
		super(TianYanCha, self).__init__()
		'''初始化查询结果的存储文件'''
		self.fileSuc = open(sucPath, 'a')
		self.fileFailed = open(failedPath, 'a')
		#self.driver = webdriver.PhantomJS(executable_path = 'C:/Programs/Python/phantomjs-2.1.1-windows/bin/phantomjs.exe')
		self.driver = webdriver.PhantomJS(executable_path = '/usr/local/share/phantomjs-2.1.1-macosx/bin/phantomjs')
		

	def __del__(self):
		print('Get Company Info Success!')
		self.fileSuc.close()
		self.fileFailed.close()
		self.driver.quit()

	def getCompanyByName(self, company):
		url = 'http://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % urllib.parse.quote(company)
		print url
		#self.text.insert('end', '开始查找公司：' + company + ' ' + url + "\r\n")
		self.driver.get(url)
		self.driver.implicitly_wait(1)
		spans = self.driver.find_elements_by_css_selector('span[class=\"c9 ng-binding\"]')
		#print(self.driver.page_source)
		if len(spans) > 0:
			href = self.driver.find_elements_by_css_selector('a[class=\"query_name\"]')
			if len(href) > 0:
				result = company
				url = href[0].get_attribute('href')
				result = result + "\t" + url
				#获取公司名称
				com_name = href[0].find_elements_by_css_selector('span[class=\"ng-binding\"]')
				if len(com_name) > 0:
					result = result + "\t" + com_name[0].text

				#获取公司城市
				com_city = self.driver.find_elements_by_css_selector('div[class=\"search_base col-xs-2 search_repadding2 text-right c3 ng-binding\"]')
				if len(com_city) > 0:
					result = result + "\t" + com_city[0].text

				#获取公司法人
				com_legalPerson = self.driver.find_elements_by_css_selector('span[ng-bind-html=\"node.legalPersonName?node.legalPersonName:\'未公开\' | trustHtml\"]')
				if len(com_legalPerson) > 0:
					result = result + "\t" + com_legalPerson[0].text

				print(url)
				self.driver.get(url)
				self.driver.implicitly_wait(1)
				#print "===================================================================="
				#print(self.driver.page_source)
				#print "===================================================================="

				#获取公司注册资本
				regCapital = self.driver.find_elements_by_css_selector('td[class=\"td-regCapital-value\"]')
				if len(regCapital) > 0:
					result = result + "\t" + regCapital[0].text.replace(' ', '')
				#获取公司注册状态
				regStatus = self.driver.find_elements_by_css_selector('td[class=\"td-regStatus-value\"]')
				if len(regStatus) > 0:
					result = result + "\t" + regStatus[0].text

				#获取公司注册时间
				regTime = self.driver.find_elements_by_css_selector('td[class=\"td-regTime-value\"]')
				if len(regTime) > 0:
					result = result + "\t" + regTime[0].text

				com_base_info_list = self.driver.find_elements_by_xpath('//div[@class=\"row b-c-white company-content\"]/table[2]/tbody/tr/td/div/span')
				if len(com_base_info_list) > 0:
					#获取公司行业
					com_business = com_base_info_list[0].text
					result = result + "\t" + com_business

				#获取公司地址
				com_address = self.driver.find_elements_by_xpath('//div[@class="company_info_text"]/span[@class="ng-binding"][3]')
				if len(com_address) > 0:
					result = result + "\t" + com_address[0].text.replace(' ', '')
				else:
					result = result + "\t" + "\\N"
				#print(com_address[0].text.replace(' ', ''))

				#获取公司简介
				if len(com_base_info_list) > 9:
					com_intro = com_base_info_list[9].text
				else:
					com_intro = "\\N"
				result = result + "\t" + com_intro

				#获取公司评分
				com_grade = self.driver.find_elements_by_xpath('//div[@class="row b-c-white company-content"]/table[1]/tbody/tr/td[@class="td-score"][1]/img')
				if len(com_grade) > 0:
					result = result + "\t" + com_grade[0].get_attribute('ng-alt')
				else:
					result = result + "\t" + "\\N"
				#print(com_grade[0].get_attribute('ng-alt'))

				#获取公司高管
				com_high_staff = self.driver.find_elements_by_xpath('//table[@class="staff-table ng-scope"]/tbody/tr[1]')
				if len(com_high_staff) > 0:
					result = result + "\t" + com_high_staff[0].text.replace(' ', '、')
				else:
					result = result + "\t" + "\\N"

				self.fileSuc.write(result)
				self.fileSuc.write('\r')
				self.fileSuc.flush()
			else:
				print result
		else:
			spans = self.driver.find_elements_by_css_selector('span[class=\"c8\"]')
			if len(spans) > 0:
				self.fileFailed.write(company)
				self.fileFailed.write('\r')
			else:
				spans = self.driver.find_elements_by_css_selector('div[class=\"gt-input\"]')
				if len(spans) > 0:
					print ""
				else:
					self.fileFailed.write('               ' + company)
					self.fileFailed.write('\r')
			self.fileFailed.flush()

def main():
	input_path = "/Users/didi/Desktop/TianYanChaPy"
	output_path = "/Users/didi/Desktop/TianYanChaPy"
	query = TianYanCha(output_path + '/succ.out', output_path + '/fail.out')
	file = open(input_path + '/company.in')
	#query.getCompanyByName('小桔科技')
	for line in file.readlines():
		query.getCompanyByName(line.strip('\n'))

if __name__ == '__main__':
	main()
