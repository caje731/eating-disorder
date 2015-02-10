from flask import Flask, request
import fileLogger 		# custom logging (I'm not relying on Flask's in-app logger)
import scanOps			# all endpoint-related operations are in this module
import sys, traceback	# exception handling

# Configuration values
SERVER = '0.0.0.0' 	# publicly available server
PORT   = 9000		# This port has been opened from within our AWS instance

app = Flask(__name__)				# The scanner application
app.config.from_object(__name__)	# Read configuration values from uppercase variables in this file
# app.config.from_envvar('SCANNER_SETTINGS', silent=True)	# Read configuration values from an environment var


# ======== Pre / post processing =========
@app.before_request
def log_request():
	logger.debug('====== Headers:\r\n{0}====== Data:\r\nQuery String Params: {1}\r\nForm Data: {2}\r\nJSON Data: {3}\r\nUnknown mimetype Data: {4}'
		.format(str(request.headers), str(request.args.to_dict()), str(request.form.to_dict(flat=False)), str(request.json), str(request.data)))


@app.after_request
def append_CORS_header(response):
	response.headers.add('Access-Control-Allow-Origin','*')
	response.headers.add('Access-Control-Allow-Headers','Origin, X-Requested-With, Content-Type, Accept')
	return response


# ======== Routes =====================
@app.route("/scan", methods=['POST'])
def start_new_scan():
	return scanOps.start_new_scan(request)


@app.route("/scanstatus", methods=['GET'])
def get_job_status():
	return scanOps.get_job_status(request)


if __name__ == "__main__":

	logger = fileLogger.get_file_logger()
	logger.info('Starting Scanner server...' + app.config['SERVER']+':'+str(app.config['PORT']))

	try:
		app.run(host=app.config['SERVER'], port=app.config['PORT'])

	except:
		# The server has stopped serving requests!
		exc_type, exc_value	= sys.exc_info()[:2]
	
		stk_trc_entries = ''.join(traceback.format_list(traceback.extract_tb(sys.exc_info()[2])))
		logger.error('type = '+str(exc_type) + ', value = '+str(exc_value) + ', traceback = '+stk_trc_entries)
		logger.critical('Scanner Server is down !')