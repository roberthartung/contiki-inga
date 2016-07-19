#!/usr/bin/python2
import SocketServer
import os
import subprocess
import sys
import threading
from time import sleep
from yaml import safe_load

#from _socket import SHUT_RDWR
from AdminServer import *
from LoggingServer import *
import LogPusher

def daemonize():
	if os.fork() != 0:
		os._exit(0)

	os.setsid()

	if os.fork() != 0:
		os._exit(0)

	os.chdir("/")
	os.umask(022)
	[os.close(i) for i in xrange(3)]
	os.open(os.devnull, os.O_RDWR)
	os.dup2(0, 1)
	os.dup2(0, 2)


class Log_server(threading.Thread):
	server = False
	
	def __init__(self,server_conf):
		print "init log"
		threading.Thread.__init__(self)
		port = int(server_conf.get("port"))
		self.server = LoggingServer(("0.0.0.0", port), LoggingHandler)
		LoggingServer.byte_buffer = server_conf.get("byte_buffer")
		self.server.socket.settimeout(5)
		return
		
	def run(self):
		print "run log"
		self.server.serve_forever()
		print "end log"
		return
	def stop(self):
		print "stopping log"
		self.server.shutdown()
		print "log stoped"
		return
		
class AdminServerThread(threading.Thread):
	server = False
	log = False
	def __init__(self, server_conf, logServer):
		print "init admin"
		threading.Thread.__init__(self)
		admin_port = int(server_conf.get('admin_port'))
		self.server = AdminServer(("0.0.0.0", admin_port), AdminHandler, logServer)
		self.server.socket.settimeout(5)
		return
		
	def run(self):
		print "run admin"
		self.server.serve_forever()
		print "end admin"
		return
	def stop(self):
		print "stoppen admin"
		self.server.shutdown()
		print "admin stoped"
		return


def main(args):
	#daemonize()
	server_conf_file = open("testbed.yaml")
	server_conf = safe_load(server_conf_file).get("server_conf")

	try:
		log = Log_server(server_conf)
		log.start()

		admin = AdminServerThread(server_conf, log.server)
		admin.start()

		while True:
			sleep(1)
			
	except KeyboardInterrupt:
		print "exiting by user request"
		print LoggingServer.handlers
		for handler in LoggingServer.handlers:
			handler.finish()
		for handler in AdminServer.handlers:
			handler.finish()
		admin.stop()
		admin.join(timeout=2)
		log.stop()
		log.join(timeout=2)
		print "shutdown"
		exit(0)

if __name__ == "__main__":
	sys.exit(main(sys.argv))
