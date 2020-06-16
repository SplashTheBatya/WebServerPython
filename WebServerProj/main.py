import signal

from Server import WebServer


#def hadle_decorator():



server = WebServer(8080)
server.start()
server._listen()
server.shutdown()

