import socket
import tkinter
import ssl

"""
Telnet in Python***
extracting the host name and the URL
creating a socket, sending a request
receiving a response
"""

# show's html body

def lex(body):
    text = ""
    in_tag = False
    for t in body:
        if t == "<":
            in_tag = True
        elif t == ">":
            in_tag = False
        elif not in_tag:
            text += t
    return text

class URL:
    # extracting the host name and the URL
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]

        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url

        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443

    # creating a socket

    def request(self):
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP, )
        s.connect((self.host, self.port))  # connecting to the host and the port
        # creating a request and receiving a response
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        request = "GET {} HTTP/1.0\r\n".format(self.path)  # creating the request
        request += "Host: {}\r\n".format(self.host)  # adding to the request
        request += "\r\n"  # add to the request
        msg = request.encode("utf8")  # encode the message
        s.send(msg)  # send the message
        response = s.makefile("r", encoding="utf-8", newline="\r\n")
        status_line = response.readline()
        version, status, explanation = status_line.split(" ", 2)

        r_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            r_headers[str(header).lower()] = value.strip()

        assert "transfer-encoding" not in r_headers
        assert "content-encoding" not in r_headers

        content = response.read()
        s.close()

        return content

    # displaying the html text


# python's version of main function run only when executing commands on the main terminal

# Browser Class
WIDTH, HEIGHT = 800, 600

HSTEP, VSTEP = 13, 18
class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()

    def load(self, url):
        self.canvas.create_rectangle(10, 20, 400, 300)
        self.canvas.create_oval(100, 100, 150, 150)
        body = url.request()
        text = lex(body)
        cursor_x, cursor_y = HSTEP, VSTEP
        for c in text:
            self.canvas.create_text(100, 100, text=c)
            cursor_x += HSTEP
            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP


if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
