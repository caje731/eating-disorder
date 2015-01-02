from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#DONE.
#JustDial US
#start_url="http://us.justdial.com/CA/San_Jose/fahrenheit_restaurant/Downtown_San_Jose"
#state="CA" ---> two letter initials
#city="San_Jose"   ---> name
#query="Fahrenheit_Restaurant_And_Lounge"  ---> business_name --> Initials Capital. MUST.

#Landing url: http://us.justdial.com/CA/San_Jose/Peanuts_Deluxe_Cafe/near_7th_St,san_Fernando_St/BBL0076697-U2FuIEpvc2UsQ0EgcGVhbnV0cyBkZWx1eGUgY2FmZSBTQU4gSk9TRSBBVkU=


class JustDialUSCrawlSpider(CrawlSpider):

	name = 'justdialUSCrawlSpider'

	def __init__(self,state,city, query, location, *args, **kwargs):
		
		city = city.replace(' ','_')
		query = query.replace(' ','_')
		location = query.replace(' ','_')
		self.rules = (Rule(	LinkExtractor(allow=(r'/'+state+'/'+city+'/'+query+'/*')),
							callback='parse_item',
							follow = True),)
		super(JustDialUSCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['us.justdial.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://us.justdial.com/'+state+'/'+city+'/'+query+'/'+location]
		

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="compdetails"]/section[1]/div/h1/span[1]/span/text()')
		l.add_xpath('address','/html/body/section[1]/section[3]/section[2]/section[2]/section[1]/section[1]/section[1]/dl[1]/dt[2]/text()')
		l.add_xpath('phone','//*[@id="compdetails"]/section[2]/span[2]/text()')
		l.add_value('websource', 'justdialus')
		return l.load_item()