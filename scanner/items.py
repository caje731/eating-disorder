# -*- coding: utf-8 -*-

import scrapy

class BusinessInfoItem(scrapy.Item):
	name 		= 	scrapy.Field()
	address 	= 	scrapy.Field()
	phone		= 	scrapy.Field()
	timings		=	scrapy.Field()
	websource 	=	scrapy.Field()	
	
    
