# -*- coding: utf-8 -*-

import scrapy

class BusinessInfoItem(scrapy.Item):
	name 		= 	scrapy.Field()
	address 	= 	scrapy.Field()
	phone		= 	scrapy.Field()
	timings		=	scrapy.Field()
	websource 	=	scrapy.Field()	
	cuisine		=	scrapy.Field()
	cost		= 	scrapy.Field()
	menus		=	scrapy.Field()
	websourcelink=  scrapy.Field()
    
