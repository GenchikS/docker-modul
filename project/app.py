from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes
from time import sleep
from urllib.parse import urlparse, parse_qs

# пошук, вичитування та завантаження index.html
# file = open("static/index.html", "r")
# html = file.read()
# file.close()
file = None
file_upload = None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        if parsed_url.path == "/":
            if "uploaded" in params:
               file_path = "./static/uploaded.html"
            else: 
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
  
  
    def do_POST(self):

        length = int(self.headers.get("Content-Length"))
        body = self.rfile.read(length)
        # flush=True - вивід відразу, щоб не було буферізації
        # print(body, flush=True)

        # код опрацювання завантаження файлу
        boundary = self.headers["Content-Type"].split("boundary=")[-1].encode()
        # відділення headers від body
        start = body.find(b"\r\n\r\n") + 4
        end = body.find(b"\r\n--" + boundary, start)

        data = body[start:end]

        with open("./images/example.jpg", "wb") as file_upload:
            file_upload.write(data)

        self.send_response(303)
        self.send_header("Location", "/?uploaded=1")
        self.end_headers()

         
    # def extract_file_data(handler):
    #     length = int(handler.headers.get("Content-Length"))
    #     body = handler.rfile.read(length)
    #     boundary = handler.headers["Content-Type"].split("boundary=")[-1].encode()
    #     start = body.find(b"\r\n\r\n") + 4
    #     end = body.find(b"\r\n--" + boundary, start)
    #     data = body[start:end]
    # return data


    #  def extract_file_data(handler):
    #  length = int(handler.headers.get("Content-Length"))
    #  body = handler.rfile.read(length)
    #  boundary = handler.headers["Content-Type"].split("boundary=")[-1].encode()
    #  start = body.find(b"\r\n\r\n") + 4
    #  end = body.find(b"\r\n--" + boundary, start)
    #  data = body[start:end]

    #  upload_name = re.search(
    #  rb'filename="([^"]+)"',
    #  body
    #  ).group(1).decode()

    #  return data, upload_name


        


server = HTTPServer(("0.0.0.0", 8000), Handler)
server.serve_forever()
