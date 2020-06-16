import socketserver
import socket


def create_string_header(content_type: str, response_code: str, content_len: int = None):
    string_builder: str = ""

    string_builder += "HTTP/1.1 "
    string_builder += response_code
    string_builder += "\r\n"

    string_builder += "Server: Cherkasov Simple Web Server\r\n"
    if content_len is not None:
        string_builder += "Content-Length: "
        string_builder += str(content_len)
        string_builder += "\r\n"

    string_builder += "Connection: close\r\n"
    string_builder += "Content-Type: "
    string_builder += content_type
    string_builder += "\r\n\r\n"

    return string_builder


endpoint = ('localhost', 1489)

server = socket.socket()
server.bind(endpoint)

server.listen(2)
while True:
    client, _ = server.accept()

    request = client.recv(1024)

    path = request.decode().split(' ')[1]

    print(path)

    hello = "HELLO HTTP"

    my_response = create_string_header("text/plain", "200 ok shit", len(bytearray(hello, encoding="utf-8")))

    print(my_response)

    client.send(bytearray(my_response, encoding="utf-8"))  # send header
    client.send(bytearray(hello, encoding="utf-8"))  # send content

server.close()