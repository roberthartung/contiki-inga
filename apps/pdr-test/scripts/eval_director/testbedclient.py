import socket
import ast
import time
class testbedclient:
	def __init__(self, host="127.0.0.1", port=4243, autoconnect=True):
		print("constructor")
		print("connecting to " + host + ":" + str(port))
		self.host = host
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.settimeout(0.1)
		if(autoconnect):
			self.connect()
	
	def connect(self):
		print("connecting")
		self.s.connect((self.host, self.port))

	def write(self, node, data):
		print("write \""+data+"\" to " + node)
		self.s.send("write " + node + " " + data+"\n")
		try:
			tmp = self.s.recv(2048)
		except:
			pass
		
	def getnodes(self):
		self.s.send("nodes\n")
		data = ""
		while data != "":
			data = self.s.recv(1024)
			if not data:
				print("kaputt!")
				self.s.close()
				return
			data = data.strip()
			data = data.strip('\n')
		print data
		nodes = ast.literal_eval(data)
		nodes = [n.strip() for n in nodes]
		return nodes
