from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#DONE. Perfectly.
#YellowPages
#start_url:
# http://www.yellowpages.com/san-jose-ca/peanuts-deluxe-cafe?g=san%20jose%2C%20ca&q=%20peanuts%20deluxe%20cafe


class YellowPagesCrawlSpider(CrawlSpider):

	name = 'yellowpagesCrawlSpider'

	def __init__(self, query, city, location, state, *args, **kwargs):
		location 	= location.replace(' ','-')
		query 		= query.replace(' ','-')
		self.rules 	= (Rule(	LinkExtractor(allow=('/'+location+'-'+ state + '/mip/'+query+'*')),
								callback='parse_item',
								follow= True),)
		super(YellowPagesCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['www.yellowpages.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.yellowpages.com/'+city+'-'+state+'/'+query+'?g='+city+'%2C%20'+state+'&q='+query]
		

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="main-content"]/div[1]/div[1]/h1/text()')
		l.add_xpath('address','//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]/p[1]/text()')
		l.add_xpath('address','//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]/p[2]/text()')
		l.add_xpath('phone','//*[@id="main-content"]/div[1]/div[1]/div/section[2]/div[1]/p[3]/text()')
		l.add_value('websource', 'yellowpages')
		return l.load_item()