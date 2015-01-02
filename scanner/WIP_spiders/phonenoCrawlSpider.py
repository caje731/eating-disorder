from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#DONE.
#PhonenNmber
#start_url:
# http://www.phonenumber.com/business?key=peanuts+deluxe+cafe&where=San+Jose%2C+CA


class PhoneNumberCrawlSpider(CrawlSpider):

	name = 'phonenumberCrawlSpider'

	def __init__(self, query, location, state, *args, **kwargs):
		location	= location.replace(' ','-')
		query 		= query.replace(' ','-')
		self.rules 	= (Rule(LinkExtractor(allow=('/business/'+query+'-'+location+'-'+state)), 
							callback='parse_item',
							follow = True),)
		super(PhoneNumberCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['www.phonenumber.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]		
		else:
			self.start_urls = ['http://www.phonenumber.com/business?key='+query+'&where='+location+'%2C+'+state]		

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="business_name"]/text()')
		l.add_xpath('address','//*[@id="left"]/div[1]/div[2]/div[3]/div[1]/div[1]/div/text()')
		l.add_xpath('address','//*[@id="left"]/div[1]/div[2]/div[3]/div[1]/div[1]/span[1]/text()')
		l.add_xpath('address','//*[@id="left"]/div[1]/div[2]/div[3]/div[1]/div[1]/abbr/text()')
		l.add_xpath('address','//*[@id="left"]/div[1]/div[2]/div[3]/div[1]/div[1]/span[2]/text()')
		l.add_xpath('timings','//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]/p[2]/text()')
		l.add_xpath('phone','//*[@id="phones_list"]/span/span/text()')
		l.add_value('websource', 'phonenumber')
		return l.load_item()
