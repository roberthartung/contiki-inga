import SocketServer
import LoggingServer
import LogPusher

class AdminServer(SocketServer.TCPServer):
    handlers = list()
    allow_reuse_address = True
    loggingServer = False
    def __init__(self, addr, handler, ls):
        SocketServer.TCPServer.__init__(self, addr, handler)
        AdminServer.loggingServer = ls

class AdminHandler(SocketServer.StreamRequestHandler):
    running = True
    log_pusher = False
       
    def setup(self):
        AdminServer.handlers.append(self)
        return SocketServer.StreamRequestHandler.setup(self)
    def handle(self):
        while self.running:
            line = self.rfile.readline()
            if not line:
                self.running = False
                return
            
            commandstr = line.split(' ', 1)
            command = commandstr[0].strip()
            if not command:
                continue
            if command == 'exit':
                self.wfile.write("bye\n")
                self.running = False
            elif command == 'nodes':
                self.wfile.write(AdminServer.loggingServer.node_list)
                self.wfile.write("\n")
            elif command == 'listen':
                if not self.log_pusher:
                    self.log_pusher = LogPusher.LogPusher(self.wfile)
                AdminServer.loggingServer.listen_node = line.split(' ',2)[1].strip()
                AdminServer.loggingServer.dispListenNodes()
                print('listen to %s' % (AdminServer.loggingServer.listen_node))
                self.log_pusher.start()
            elif command == 'write':
                dest, data = commandstr[1].split(' ', 1)        
                if not dest in AdminServer.loggingServer.node_list:
                    print 'no such node connected'
                    continue
                AdminServer.loggingServer.handlers_dict[dest].writeData(data)
            elif command == 'stop':
                self.log_pusher.stop()
                self.log_pusher.join()
                self.log_pusher = False
                print "stop done"
            else:
                self.wfile.write("unknown command.\n")
        print "end admin handler"
        return
                
    def finish(self):
        AdminServer.handlers.remove(self)
        self.running = False
        if self.log_pusher:
            self.log_pusher.stop()
            self.log_pusher.join()
        print "gone"
