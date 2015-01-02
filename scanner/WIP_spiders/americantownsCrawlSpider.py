from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#DONE.
#American Towns
#start_url="http://www.americantowns.com/ca/sanjose/search?searchtext=fahrenheit+restaurant&s_business=1&s_places=1&s_news=1&s_events=1"
#state="ca"  ---> two letter state initials
#city="name" --->sanjose

class AmericanTownsCrawlSpider(CrawlSpider):

	name = 'americantownsCrawlSpider'

	def __init__(self, query, state, city, *args, **kwargs):
		self.rules = (Rule(LinkExtractor(allow=('/'+state+'/'+city+'/'+'yp/listing/sp-*')), callback='parse_item',follow = True),)
		super(AmericanTownsCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['www.americantowns.com']
		query = query.replace(' ', '-')
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.americantowns.com/'+state+'/'+city+'/search?searchtext='+query+'&s_business=1&s_places=1&s_news=1&s_events=1']

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="sp_detail"]/div[1]/h1/text()')
		l.add_xpath('address','//*[@id="sp_detail"]/div[3]/div[1]/div/div[1]/text()')
		l.add_xpath('address','//*[@id="sp_detail"]/div[3]/div[1]/div/div[2]/text()')
		l.add_xpath('phone','//*[@id="sp_detail"]/div[3]/div[2]/text()')
		l.add_value('websource', 'americantowns')

		return l.load_item()

		