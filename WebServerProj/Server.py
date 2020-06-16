import socket
import time
import threading
import RouteHandler


class WebServer(object):

    def __init__(self, port=8080):
        self.host = socket.gethostname().split('.')[0]
        self.port = port
        self.content_dir = 'Content'

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            print("Trying start server on {host}:{port}".format(host=self.host, port=self.port))
            self.socket.bind(("localhost", self.port))
            print("Succesed connection on {port}".format(port=self.port))

        except Exception as e:
            print("Error: Could not bind to port {port}".format(port=self.port))
            print(e)
            self.socket.close()

        self.socket.listen()

    def shutdown(self):
        try:
            print("Trying to shutdown server")
            self.socket.close()
            print("Success")
        except Exception as e:
            print("Server already off")
            pass

    def _generate_headers(self, response_code):
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Server: My Server\n'
        header += 'Connection: close\n\n'
        return header

    def _listen(self):
        self.socket.listen(2)
        while True:
            (client, address) = self.socket.accept()
            client.settimeout(60)
            print("Recieved connection from {addr}".format(addr=address))
            threading.Thread(target=self._handle_client, args=(client, address)).start()

# GET HANDLER

    def get_handler(self, request_method, request):
        print(request_method)
        file_requested = request.decode().split(' ')[1]

        file_requested = file_requested.split('?')[0]

        filepath_to_serve = self.content_dir + file_requested
        print("Serving web page [{fp}]".format(fp=filepath_to_serve))

        try:
            f = open(filepath_to_serve, 'rb')
            if request_method == "GET":
                response_data = f.read()
            f.close()
            response_header = self._generate_headers(200)

        except Exception as e:
            print("File not found. Serving 404 page.")
            response_header = self._generate_headers(404)

            if request_method == "GET":
                response_data = b"<html><body><center><h1>Error 404: File not found</h1></center></body></html>"

        response = response_header.encode()
        response += response_data
        return response

# CLIENT HANDLER
    def _handle_client(self, client, address):
        packet_size = 1024
        while True:
            print("CLIENT",client)
            request = client.recv(packet_size)
            request_method = request.decode().split(' ')[0]

            #print(request_method)

            if request_method == "GET":
                response = self.get_handler(request_method,request)
                client.send(response)
                client.close()
                break

            #else:

                #print("Unknown HTTP request method: {method}".format(method=request_method))

