import CGIHTTPServer, BaseHTTPServer
import sys, logging, traceback

serverName		=	'0.0.0.0'
serverPort		=	9000
requestHandler 		=	CGIHTTPServer.CGIHTTPRequestHandler
log_file		=	'CGIServer.log'
requestHandler.cgi_directories = ["/"]

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename=log_file,level=logging.DEBUG)
logging.info('Starting CGI Server@ '+serverName+':'+str(serverPort))

try:
	httpd = BaseHTTPServer.HTTPServer((serverName,serverPort),requestHandler)
	httpd.serve_forever()
except:
	exc_type, exc_value	= sys.exc_info()[:2]

	stk_trc_entries = ''.join(traceback.format_list(traceback.extract_tb(sys.exc_info()[2])))
	logging.error('type = '+str(exc_type) + ', value = '+str(exc_value) + ', traceback = '+stk_trc_entries)

