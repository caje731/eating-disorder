import logging

def get_file_logger(log_level=logging.DEBUG, log_file='scanner.log'):

	logging.basicConfig(	format='%(asctime)s [%(levelname)s] %(message)s',
				datefmt='%m/%d/%Y %I:%M:%S %p',
				filename=log_file,
				level=log_level	)
	logger = logging.getLogger('scanner')
	return logger

if __name__ == "__main__":
	print "Use this module's get_file_logger function to log to a file"
