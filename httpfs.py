import argparse
import socket
from http.server import BaseHTTPRequestHandler
from io import StringIO


class response_code(enumerate):
    NOT_FOUND = 404
    OKAY = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401


class server:
    debugging = None
    port = None
    directory = None

    def configure_and_start_server(self):
        server.port = args.port
        server.debugging = args.debugging
        server.directory = args.directory
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind(('localhost', self.port))
        tcp_socket.listen(5)

        while True:
            connection, client_address = tcp_socket.accept()
            self.print_if_debugging_is_enabled("client connected from ", str(client_address))
            httpfs().handle_client_request(connection, client_address)

    @staticmethod
    def print_if_debugging_is_enabled(message):
        if server.debugging:
            print("debug: " + message)


class httpfs:

    def __init__(self):
        self._request_type = None
        self._request_path = None
        self._request_headers = {}
        self._request_query_parameters = None
        self._request_body = None

        self._response_code = None
        self._response_headers = {}
        self._response_body = None

    @property
    def request_type(self):
        return self._request_type

    @request_type.setter
    def set_request_type(self, request_type):
        self._request_type = request_type

    @property
    def request_path(self):
        return self._request_path

    @request_path.setter
    def set_request_path(self, request_path):
        self._request_path = request_path

    @property
    def request_headers(self):
        return self._request_headers

    @request_headers.setter
    def set_request_headers(self, request_headers):
        self._request_headers = request_headers

    @property
    def request_query_parameters(self):
        return self._request_query_parameters

    @request_query_parameters.setter
    def set_request_query_parameters(self, request_query_parameters):
        self._request_query_parameters = request_query_parameters

    @property
    def request_body(self):
        return self._request_body

    @request_body.setter
    def set_request_body(self, request_body):
        self._request_body = request_body

    @property
    def response_code(self):
        return self._response_code

    @response_code.setter
    def set_response_code(self, response_code):
        self._response_code = response_code

    @property
    def response_headers(self):
        return self._response_headers

    @response_headers.setter
    def set_response_headers(self, response_headers):
        self._response_headers = response_headers

    @property
    def response_body(self):
        return self._response_body

    @response_body.setter
    def response_body(self, response_body):
        self._response_body = response_body

    def handle_client_request(self, connection, client_address):
        while True:
            request = connection.recv(4096)
            request = request.decode('utf-8')
            self.parse_request(request)

    """
        For HTTP Request Parsing 
        see (https://stackoverflow.com/questions/2115410/does-python-have-a-module-for-parsing-http-requests-and-responses)
    """

    def parse_request(self, request):
        request = HTTPRequest(request)
        if not request.error_code:
            self.set_request_type = request.command  # "GET"
            self.set_request_path = request.path  # "/who/ken/trust.html"
            self.set_response_headers = request.headers
        else:
            self._response_code = response_code.BAD_REQUEST
            self._response_body = "Invalid Request Format"
            server.print_if_debugging_is_enabled("Invalid Request Format: " + request.error_code)
            self.send_response()
            raise SyntaxError("Invalid Request Format: " + request.error_code)

    def send_response(self):
        # TODO: check for the request type and accordingly send the response to client.
        return ""


class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


parser = argparse.ArgumentParser(description="http server")

parser.add_argument("-v", dest="debugging",
                    help="Prints debugging messages if enabled",
                    action="store_true")
parser.add_argument("-p",
                    dest="PORT",
                    default="8080",
                    type=int,
                    help="Specifies the port number that the server will listen and serve at \
                            Default is 8080.",
                    action="store")
parser.add_argument("-d",
                    dest="DIRECTORY",
                    help="Specifies the directory that the server will use to read/write requested files. Default is "
                         "the current directory when launching the application.",
                    default="./")
#
# print("current directory: " + os.getcwd())
# print("Parent of current directory: " + os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

args = parser.parse_args()
