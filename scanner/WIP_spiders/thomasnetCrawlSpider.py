from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#Thomasnet.com
#start_url:
# `


class ThomasNetCrawlSpider(CrawlSpider):

	name = 'thomasnetCrawlSpider'

	def __init__(self,*args, **kwargs):
		
		self.rules = (Rule(	LinkExtractor(allow=(r'/profile/*')),
							callback='parse_item',
							follow = True),)
		super(ThomasNetCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['thomasnet.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['']
		

	def parse_item(self,response):
		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('company','//*[@id="profilehead"]/tbody/tr[1]/td/h1/a/text()')
		l.add_xpath('phone','//*[@id="phones-30121314"]/strong[1]]/text()')
		#l.add_xpath('company_profile','//*[@id="coprobody"]/b/text()/br[1]/text()')
		#l.add_xpath('fax','//*[@id="phones-30121314"]/text()')
		l.add_value('websource', 'thomasnet')
		return l.load_item()