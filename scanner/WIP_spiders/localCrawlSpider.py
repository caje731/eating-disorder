from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem


#input examples:-
#location="san jose ca"
#query="fahrenheit restaurant and lounge"
#start_url="http://www.local.com/business/results/location/query/"
#start_urls = ['http://www.local.com/business/results/?keyword='+query+'&location=San%20Jose%2C%20CA']

class LocalCrawlSpider(CrawlSpider):
	name = 'localCrawlSpider'
	allowed_domains = ['www.local.com']
	
	def __init__(self, city, query, state, *args, **kwargs):
		query 	= query.replace(' ','-')
		city 	= city.replace(' ','-')
		
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls	= [	'http://www.local.com/business/results/?keyword='+query+'&location='+city+'%2C'+state]
		
		self.rules = (Rule(LinkExtractor(allow=(r'/business/details/'+city+'-'+state+'/'+query+'*')),callback='parse_item',follow=True),)
		super(LocalCrawlSpider, self).__init__(*args, **kwargs)
		
	def parse_item(self,response):
		l = ItemLoader(item = BusinessInfoItem(),response = response)

		l.add_xpath('name','//*[@id="biz-vcard"]/div[2]/h1/span/text()')
		l.add_xpath('phone','//*[@id="biz-vcard"]/div[5]/div[2]/address/p/strong/text()')
		l.add_xpath('address','//*[@id="biz-vcard"]/div[5]/div[2]/address/p/span[2]/text()')
		l.add_xpath('address','//*[@id="biz-vcard"]/div[5]/div[2]/address/p/span[3]/text()')
		l.add_xpath('address','//*[@id="biz-vcard"]/div[5]/div[2]/address/p/span[4]/text()')
		l.add_value('websource', 'local')
		return  l.load_item()
	  
