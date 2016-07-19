import threading
import LoggingServer

class LogPusher(threading.Thread):
    running = True 
    wfile = False
    log = False
    def __init__(self,wfile): 
        threading.Thread.__init__(self)
        self.wfile = wfile
    def run(self):
        while self.running:
            self.wfile.write(LoggingServer.LoggingServer.listen_list.get())
        print "end log handler"
        return
    def stop(self):
        LoggingServer.LoggingServer.listen_node = False
        while LoggingServer.listen_list.qsize() > 0:
            LoggingServer.LoggingServer.listen_list.get()
        self.running = False
        print "stopping"
