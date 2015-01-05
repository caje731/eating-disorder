import CGIHTTPServer, BaseHTTPServer
import sys, logging, traceback


class LoggingCGIHTTPRequestHandler(CGIHTTPServer.CGIHTTPRequestHandler):
	def log_request(self, *args):
		logging.info('Client = {0}, Request Version = {1}, Method = {2}, Path = {3}, Headers = {4}'
						.format(self.client_address, self.request_version, self.command, self.path, str(self.headers)))
			
	def log_message(self, format, *args):
		logging.info(format%args)

if __name__ == "__main__":

	serverName		=	'0.0.0.0'
	serverPort		=	9000
	requestHandler 	=	LoggingCGIHTTPRequestHandler
	log_file		=	'CGIServer.log'
	requestHandler.cgi_directories = ["/"]

	logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
						filename=log_file,level=logging.DEBUG)
	logging.info('Starting CGI Server@ '+serverName+':'+str(serverPort))

	try:
		httpd = BaseHTTPServer.HTTPServer((serverName,serverPort),requestHandler)
		httpd.serve_forever()
	except:
		exc_type, exc_value	= sys.exc_info()[:2]
	
		stk_trc_entries = ''.join(traceback.format_list(traceback.extract_tb(sys.exc_info()[2])))
		logging.error('type = '+str(exc_type) + ', value = '+str(exc_value) + ', traceback = '+stk_trc_entries)


