import os.path
from abc import ABC, abstractmethod


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