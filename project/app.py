from http.server import HTTPServer, BaseHTTPRequestHandler

import os
import mimetypes

# пошук, вичитування та завантаження index.html

file = open("./static/index.html", "r")
html = file.read()
file.close()

# fileUpload = open("./static/upload.html", "r")
# htmlUpload = fileUpload.read()
# fileUpload.close()



class Handler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == "/":
            file_path = "./static/index.html"
        else:
            file_path = "./static" + self.path

        if os.path.isfile(file_path):

            with open(file_path, "rb") as file:
                content = file.read()

            content_type = mimetypes.guess_type(file_path)[0]

            if content_type is None:
                content_type = "application/octet-stream"

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.end_headers()

            self.wfile.write(content)

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

            self.wfile.write(b"404 - File not found")
        



# class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"POST OK!")
        # self.wfile.write(htmlUpload.encode())

        


server = HTTPServer(("0.0.0.0", 8000), Handler)
server.serve_forever()