#!/usr/bin/env python

import os, sys, subprocess

UMASK 		= 0
MAXFD		= 1024
REDIRECT_TO = '/dev/null'

def createDaemon():
	try:
		pid = os.fork()
	except OSError, e:
		raise Exception, "%s [%d]" % (e.strerror, e.errno)

	if pid==0:
		os.setsid()
		try:
			pid = os.fork()
		except OSError, e:
			raise Exception, "%s [%d]" % (e.strerror, e.errno)
		
		if pid==0:
			os.umask(027)
		else:
			os._exit(0)
	else:
		os._exit(0)
	
	import resource		# Resource usage information.
	maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
	if (maxfd == resource.RLIM_INFINITY):
		maxfd = MAXFD
  
	# Iterate through and close all file descriptors.
	for fd in range(0, maxfd):
		try:
			os.close(fd)
		except OSError:	# ERROR, fd wasn't open to begin with (ignored)
			pass
		
	os.open(REDIRECT_TO, os.O_RDWR)
	os.dup2(0,1)
	os.dup2(0,2)
	
	return(0)
	

if __name__ == "__main__":

	retCode = createDaemon()

	procParams = """
	return code = %s
	process ID = %s
	parent process ID = %s
	process group ID = %s
	session ID = %s
	user ID = %s
	effective user ID = %s
	real group ID = %s
	effective group ID = %s
	""" % (retCode, os.getpid(), os.getppid(), os.getpgrp(), os.getsid(0),
	os.getuid(), os.geteuid(), os.getgid(), os.getegid())
	
	open("ScrapydDaemon.log", "w").write(procParams + "\n")
	subprocess.call(['scrapyd'])
	
	sys.exit(retCode)
	
