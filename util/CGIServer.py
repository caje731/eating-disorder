#!/usr/bin/env python

import CGIHTTPServer, BaseHTTPServer
import sys, traceback
import fileLogger


class LoggingCGIHTTPRequestHandler(CGIHTTPServer.CGIHTTPRequestHandler):

	logger = fileLogger.get_file_logger()

	def log_request(self, *args):
		content_length = self.headers.getheader('content-length')
		if content_length is None:
			content_length = 0
		else:
			content_length = int(content_length)
		content	= self.rfile.read(content_length)
		self.logger.debug('Client = {0}, Request Version = {1}, Method = {2}, Path = {3}, Headers = {4}Data: {5}'
						.format(self.client_address, self.request_version, self.command, self.path, str(self.headers), content))
		
	def log_message(self, format, *args):
		self.logger.info(format%args)

	def log_error(self, format, *args):
		self.logger.error(format%args)

if __name__ == "__main__":

	serverName		=	'0.0.0.0'
	serverPort		=	9000
	requestHandler 		=	LoggingCGIHTTPRequestHandler
	requestHandler.cgi_directories = ["/"]

	logger = fileLogger.get_file_logger()

	logger.info('Starting CGI Server... '+serverName+':'+str(serverPort))

	try:
		httpd = BaseHTTPServer.HTTPServer((serverName,serverPort),requestHandler)
		httpd.serve_forever()
	except:
		exc_type, exc_value	= sys.exc_info()[:2]
	
		stk_trc_entries = ''.join(traceback.format_list(traceback.extract_tb(sys.exc_info()[2])))
		logger.error('type = '+str(exc_type) + ', value = '+str(exc_value) + ', traceback = '+stk_trc_entries)
		logger.critical('CGI Server is down !')


