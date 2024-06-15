import socket
import threading

#create URL class and initialize parameters
#url example: http://example.org/index.html
PORT = 80
class URL:
    #separting Url into its three components, scheme, hostname, path
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme == "http"

        if "/" not in url:
            url = url + "/"
            self.host, url = url.split("/", 1)
            self.path = "/" + url


    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )

        s.connect((self.host, PORT))

        request = "GET {} HTTP.1.0\r'n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        s.send(request.encode("utf-8"))







if __name__ == "__main__":

