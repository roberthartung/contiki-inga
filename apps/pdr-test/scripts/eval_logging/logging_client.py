#!/usr/bin/python2
import socket
import serial
#import netifaces
import select
import AdminServer
from gethwaddr import *

from yaml import safe_load



client_conf_file = open('testbed.yaml')
client_conf = safe_load(client_conf_file)
server_ip = client_conf.get("server_conf").get("ip")
server_port = client_conf.get("server_conf").get('port')


def get_mac(dev):
	return getHwAddr(dev)
#	if not dev in netifaces.interfaces():
#		return False
#	if  netifaces.ifaddresses(dev)[netifaces.AF_PACKET][0]["addr"]:
#		mac = netifaces.ifaddresses(dev)[netifaces.AF_PACKET][0]["addr"]
#	else:
#		mac = "gibts nicht"
#	return mac
			

# read and parse config files
try:
	server_port = int(server_port)
except:
	print("server_port is not a number: %s" % (server_port))
	exit(1)

#
tty_port = False
tty_baud = False
node_id = False
configured = False

# node is determined by:
#        hostname
#          -OR-
#  mac_dev and mac_addr
# in config file

for node in client_conf.get('nodes'):
	host = node.get('hostname')
	dev = node.get('mac_dev')
	mac = node.get('mac_addr')
 
	if host:
		if node.get('hostname') == socket.gethostname():
			configured = True
	else:
		if dev and mac:
			if get_mac(dev) == mac:
				configured = True
		else:
			print("neither host, nor mac/dev specified")
			
	if configured:
		node_id = node.get('node_id')
		tty = node.get('tty')
		if not tty:
			print("no serial port configured.")
			exit(2)
		tty_port = tty.get('port')
		tty_baud = tty.get('baud')
		try:
			tty_baud = int(tty_baud)
		except:
			print("baud invalid")
			exit(2)
		break
		
			
if not node_id:
	print("no node_id configured for host: %s" % (socket.gethostname()))
	exit(1)
if not tty_baud and not tty_port:
	print("no tty config")
	exit(1)

# config has been successfully read
# open serial port
try:
	s = serial.Serial(tty_port, tty_baud, timeout=1, xonxoff=1)
except:
	print("failed to connect to tty: %s" % (tty_port))
	exit(2)
try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((server_ip, server_port))
except:
	print("failed to connect to server: %s:%d" % (server_ip,server_port))
	exit(3)
	
# connect to server
try:
	sock.sendall("%s:setup\n" % (node_id))
	while True:
		l = select.select([s, sock], [], [])
		#todo: what if server dies?
		if s in l[0]:
			# read data from serial port
			data = False
			data = s.readline()
			# send data via tcp to server 
			if data:
				if data[-1] != '\n':
					data = data + '\n'
				sock.sendall("%s:log:%s" % (node_id,data))
		if sock in l[0]:
			data = sock.recv(4096)
			if not data:
				print "something's gone terribly wrong."
				break
			s.write(data)
	sock.sendall("%s:exit\n" % (node_id))
except:
	sock.sendall("%s:exit\n" % (node_id))
	sock.close()
finally:
	sock.close()
