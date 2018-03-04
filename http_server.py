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
1.2
"""

from HttpServer import HttpServer
from Constants import *


def main():
    my_server = HttpServer(IP, PORT, ROOT_DIR)
    # able to have endless connections!!!
    while True:
        my_server.run_server()


if __name__ == "__main__":
    main()
