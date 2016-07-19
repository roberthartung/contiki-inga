import SocketServer
from Queue import Queue
import time


class LoggingServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    handlers = list()
    node_list = []
    listen_list = Queue()
    listen_node = False
    byte_buffer = 0
    allow_reuse_address = True
    handlers_dict = {}    
    
    def dispListenNodes(self):
        print listen_node
        
class LoggingHandler(SocketServer.StreamRequestHandler):
    node_id = 0
    running = True
    node_log_file = False 
    buffered_bytes = 0
    def writeData(self, data):
        self.wfile.write(data)
    def setup(self):
        LoggingServer.handlers.append(self)
        print "LoggingHandler added."
        print LoggingServer.handlers
        return SocketServer.StreamRequestHandler.setup(self)
    def handle(self):
        while self.running:
            line = self.rfile.readline()
            if not line:
                print("Read error. finish.")
                #self.finish()
                break
            packet = line.split(':',2) 
            if len(packet) >= 2:
                command = packet[1].strip()
                if len(packet) > 2:
                    data = packet[2].strip()
                else:
                    data = False
            else:
                print("PACKET too short: %s" % (line,))
                continue
            if not packet[0].strip():
                print("NO node_id: %s \n" % (packet[0]))
                continue
            if self.node_id == 0:
                self.node_id = packet[0].strip()
            elif self.node_id != packet[0].strip():
                print("WRONG node_id: %s \n" % (packet[0]))
                continue
            if not command:    # EOF
                print("NO command in packet: %s \n" % (line,))
                continue
            if command == "log":
#                print(packet[2])
                if self.node_log_file and data:
                    self.node_log_file.write(("%.10f,"%time.time()) + packet[2])
                    if self.node_id == LoggingServer.listen_node:
                        ThreadedTCPServer.listen_list.put(packet[2])
                    if self.buffered_bytes == LoggingServer.byte_buffer:
                        self.buffered_bytes = 0
                        self.node_log_file.flush()
                    else:
                        self.buffered_bytes+=len(data)
                elif not self.node_log_file:
                    print("log file not opened")
                elif not data:
                    print("no data given")    
            if command == "setup":
                if LoggingServer.node_list.__contains__(self.node_id):
                    print("warning: node %s already connected"% (self.node_id))
                    print("replacing old connection...")
                else:
                    LoggingServer.node_list.append(self.node_id)
                LoggingServer.handlers_dict[self.node_id] = self
                if not self.node_log_file:
                    try:
                        self.node_log_file = open("%s.log"%(self.node_id),'a')
                        print("open file: %s.log\n"% (self.node_id))
                    except:
                        print("COULD not open file: %s.log\n"% (self.node_id))
                    continue
                else:
                    print("log file already opened: %s.log\n"% (self.node_id))
                    continue
            if command == "exit":
                try:
                    LoggingServer.node_list.remove(self.node_id)
                    self.node_log_file.close()
                    print("closed file: %s\n"% (self.node_id))
                    self.node_log_file = False
                except:
                    print("COULD not close file: %s.log\n"% (self.node_id))
                    continue
                break
        return
    def finish(self):
        print "finish..."
        print LoggingServer.handlers
        self.running = False
        if self.node_id in LoggingServer.node_list:
            LoggingServer.node_list.remove(self.node_id)
        if self.node_log_file:
            try:
                self.node_log_file.close()
                self.node_log_file = False 
            except:
                pass
        LoggingServer.handlers.remove(self)
        print "end"
