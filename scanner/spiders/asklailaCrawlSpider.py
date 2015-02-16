from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem
from HTMLParser import HTMLParser


#DONE.
#Asklaila
#User Input: location= "Bandra", location1="West" , city="Mumbai" , q = "stomach"
#start_url="http://www.asklaila.com/search/Mumbai/bandra/stomach/?searchNearby=true"
#limit: "http://www.asklaila.com/listing/Mumbai/Bandra+West/Stomach/1dHGIAZT/"

class AsklailaCrawlSpider(CrawlSpider):

	name = 'asklailaCrawlSpider'

	def __init__(self, city, location, query, *args, **kwargs):
		
		query 		= '+'.join( [part.capitalize() for part in query.split()	] ) 
		location 	= '+'.join( [part.capitalize() for part in location.split()	] )
		city 		= city.capitalize()
		
		self.rules = (Rule(	LinkExtractor(	allow=('/listing/'+city.replace('+','\+')+'/'+location.replace('+','\+')+'/'+query.replace('+','\+')),
											deny=('/tel:')),
							callback='parse_item',
							follow = True),
						)
		super(AsklailaCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['www.asklaila.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.asklaila.com/search/'+city+'/'+location+'/'+query+'/?searchNearby=true']

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		#l.add_xpath('name','//*[@id="ldpAdrsDetails"]/div[1]/div[1]/div/h1/span/text()')
		l.add_xpath('name','//span[@itemprop="name"]/h1/text()')
		
		l.add_xpath('address','//span[@class="adr"]')
		l.add_xpath('phone','//span[@itemprop="telephone"]/text()')
		l.add_xpath('cuisine', '//span[@itemprop="servesCuisine"]/text()')
		# I couldn't find any menu images on asklaila
		l.add_value('websource', 'asklaila')
		item = l.load_item()
		
		if 'address' in item:
			htmlparser = CustomHTMLParser()
			htmlparser.feed(''.join(item['address']))
			item['address'] = htmlparser.data
		
		return item



# CustomHTMLParser has been written simply to parse the address
# since the address is a mix of text nodes and nested tags
class CustomHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = ''
		
    # Need to only extract the data so override only that method 
	def handle_data(self, data):
		self.data += data
