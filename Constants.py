"""
Part of http_server.py
"""

import os.path

IP = '0.0.0.0'
PORT = 55556
ROOT_DIR = r'C:\Users\gefen\PycharmProjects\NewProjects\HttpServer' + \
           os.path.sep + 'webroot'
REQUEST_LENGTH = 1024  # bytes
SOCKET_TIMEOUT = 1  # seconds to wait for sending/receiving

# Files that you don't want anyone to see!
# add them in here! Example: (os.path.abspath("file.txt")...)
FORBIDDEN = (
    # Example: os.path.abspath("file.txt")
)

# Files that moved temporarily.
# Key: path of file expected (add '/' in the beginning)
# Value: the new abspath of file
MOVED_TEMP = {
    # EXAMPLE: '/index.ori': '\\'
}
