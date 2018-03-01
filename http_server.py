"""
Description:
This is a simple http server that supports requests of html, jpeg
JS and css files.

To work with this server, run it, go to your browser and surf to
127.0.0.1:PORT (changes according to the PORT variable,
defined down here).

It will open a simple website that shows the capabilities of the server.

Author:
Gefen Hajaj

Excersice Number:
4.4

File Name:
http_server

Date:
27.02.2018

Version:
1.1
"""

import socket
import os.path
from abc import ABC, abstractmethod

IP = '0.0.0.0'
PORT = 55558
ROOT_DIR = 'D:' + os.path.sep + 'wwwroot'
REQUEST_LENGTH = 1024  # bytes


class GeneralServer(ABC):
    """
    Abstract class that every server class should implement.
    """

    def __init__(self, ip, port):
        super(GeneralServer, self).__init__()
        self.ip = ip
        self.port = port

    @abstractmethod
    def run_server(self):
        """
        Start connection using sockets and the given ip and port.
        :return: None
        """
        pass

    @abstractmethod
    def get_request(self, client_socket):
        """
        Get request from client and return a tuple.
        If valid - (1, request)
        Not valid - (0, What kind of not valid?):
            connection lost - (0, 0)
            invalid requst - (0,1)
        :return: str
        """
        pass

    @abstractmethod
    def create_response(self, *more_vars):
        """
        Given enough data, creating the respond and returning it.
        :return: str
        """
        pass


class HttpServer(GeneralServer):
    """
    Simple HTTP server that can handle css, html, JS and jpeg.
    """

    ok_response = "HTTP/1.1 200 OK\r\n"
    not_found_response = "HTTP/1.1 404 Not Found"
    internal_server_error = "HTTP/1.1 500 Internal Server Error"

    # Different content types:
    ct_txt_html = "Content-Type: text/html; charset=utf-8\r\n"  # .txt or .html
    ct_jpg = "Content-Type: image/jpeg\r\n"  # .jpg
    ct_js = "Content-Type: text/javascript; charset=utf-8\r\n"  # .js
    ct_css = "Content-Type: text/css\r\n"  # .css

    def __init__(self, ip, port, root_dir):
        super(HttpServer, self).__init__(ip, port)
        self.root_dir = root_dir

    def run_server(self):
        # Starting connection with client
        print("Starting a new connection...")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((IP, PORT))
        server_socket.listen(10)
        # initial connection:
        client_socket, address = server_socket.accept()
        server_socket.settimeout(1)

        while True:  # make sure to get out of here somehow
            client_socket.settimeout(1)
            print("connected to {}".format(str(address)))

            print("waiting for request...")
            url_file = self.get_request(client_socket)

            if url_file[0]:
                # making the url itself into something readable by WINDOWS.
                url_file = self.root_dir + os.path.sep + HttpServer.\
                    make_url_address(url_file[1]) if url_file[1] != '/' \
                    else url_file[1]

                response = self.create_response(url_file)

                try:
                    client_socket.send(response)
                except socket.timeout:
                    break

            else:
                print("invalid request")
                if url_file[1] == 1:  # Got something, but not good
                    try:
                        client_socket.send(HttpServer.internal_server_error.
                                           encode())
                    except socket.timeout:
                        break
                else:
                    break

            # continue accepting requests
            try:
                client_socket, address = server_socket.accept()
            except socket.timeout:
                break

        # Closing connection after client left
        print("connection closed")
        client_socket.close()
        server_socket.close()

    def get_request(self, client_socket):
        """
            Receive the request sent by the client.
            Checks if it is an HTTP request.
            If yes - returns the file name the user wants (URL).
            If not - returns an empty string.

            :param client_socket: socket.socket
            :return: str
            """

        try:
            request = client_socket.recv(REQUEST_LENGTH).decode()
            # the different parts of the request:
            request_parts = request.splitlines()
            request_parts = request_parts[0].split(" ")

            if request_parts[0] == "GET" and request_parts[2] == "HTTP/1.1":
                # The actual path to what was requests:
                return 1, request_parts[1]

            print("invalid request")
            return 0, 1
        except IndexError:
            print("index error")
            return 0, 1
        except socket.timeout:
            print("socket timeout")
            return 0, 0

    def create_response(self, file_path):
        """
            This func gets a url from the GET request and returns a valid
            response.
            :param file_path: str
            :return: str
            """

        # checking - maybe index?
        if file_path == '/':
            file_path = self.root_dir + os.path.sep + "index.html"

        # creating http responses
        if check_if_file_exists(file_path):

            data = get_content_file(file_path)

            # response line:
            http_response = HttpServer.ok_response

            # headers:
            http_response += "Content-Length: {}".format(len(data)) + "\r\n"
            http_response = HttpServer.add_content_type(http_response,
                                                        file_path)
            # finishing up:
            http_response += "\r\n"
            # content itself - the data
            http_response = http_response.encode()
            http_response += data

            return http_response
        else:
            return HttpServer.not_found_response
            # This is where we would add a cool 404 error page...

    @staticmethod
    def add_content_type(http_response, file_path):
        """
            Gets a (half-built) http response in the right time of building
            and adds a Content-Type header to it.
            Of courese, we nned the path to the file, as well, to know the
            contents type...
            It returns the half-built http_response with that header.

            For now: if we don't know the type of file we want, we just don't
            add the Content-Type line.

            :param http_response: str
            :param file_path: str
            :return: str
            """

        # getting the file type!
        file_path = file_path.split(".")[-1]

        # Adding the wanted line and returning the updated response:
        if file_path == "txt" or file_path == "html":
            return http_response + HttpServer.ct_txt_html
        if file_path == "jpg" or file_path == "jpeg":
            return http_response + HttpServer.ct_jpg
        if file_path == "js":
            return http_response + HttpServer.ct_js
        if file_path == "css":
            return http_response + HttpServer.ct_css

        # If nothing we know...
        return http_response

    @staticmethod
    def make_url_address(url):
        """
        takes a url from a GET request and turns it to something WINDOWS
        can read.
        :param url: str
        :return: str
        """

        return url.replace("/", os.path.sep)


# Some general methods:
def check_if_file_exists(file):
    """
    checks if files exists. returns True or False accordingly.
    :param file: str (path to file)
    :return: bool
    """

    if os.path.isfile(file):
        return True

    return False


def get_content_file(file_path):
    """
    Gets a full path to a file and returns the content of it.
    file_path must be a valid path.
    :param file_path: str (path)
    :return: str (data)
    """

    file = open(file_path, 'rb')
    data = file.read()
    file.close()
    return data


def main():
    my_server = HttpServer(IP, PORT, ROOT_DIR)
    # able to have endless connections!!!
    while True:
        my_server.run_server()


if __name__ == "__main__":
    main()
