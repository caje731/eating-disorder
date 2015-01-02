from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#Done. Check json file generated. If the file is non empty, there exist company/companies with the searched name..
#ec21
#start_url:
# http://supplier.ec21.com/tamo_technology_co_ltd.html

class EC21CrawlSpider(CrawlSpider):

	name = 'ec21CrawlSpider'

	def __init__(self, query, *args, **kwargs):
		
		self.rules = (Rule(LinkExtractor('en.ec21.com'), callback='parse_item',follow = True),)
		super(EC21CrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['ec21.com']
		
		query = query.replace(' ', '_')
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://supplier.ec21.com/'+query+'.html']

	def parse_item(self,response):
		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','/html/body/center/table[2]/text()')
		l.add_value('websource', 'ec21')
		return l.load_item()
