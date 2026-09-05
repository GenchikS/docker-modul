from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes
from urllib.parse import urlparse, parse_qs
import uuid
import re

# пошук, вичитування та завантаження index.html
# file = open("static/index.html", "r")
# html = file.read()
# file.close()
file = None
file_upload = None
file_local_path = None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        if parsed_url.path == "/":
            if "uploaded" in params:
               file_path = "./static/uploaded.html"
            elif "error" in params:
                file_path = "./static/error.html"
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
        # print("Розмір:", len(body), flush=True)

        size_photo = len(body)
        if size_photo > 5000000:
            self.send_response(303)
            self.send_header("Location", "/?error=1")
            self.end_headers()
            return

        # код опрацювання завантаження файлу
        boundary = self.headers["Content-Type"].split("boundary=")[-1].encode()
        # відділення headers від body
        start = body.find(b"\r\n\r\n") + 4
        end = body.find(b"\r\n--" + boundary, start)

        data = body[start:end]


        # отримання імені файлу
        upload_name = re.search(
            rb'filename="([^"]+)"', body).group(1).decode()
        # print(upload_name, flush=True)

        # отримання розширення файлу
        expansion_name = str(upload_name.split(".")[-1])

        # перевірка на розширення
        if expansion_name in {"jpg", "jpeg", "png", "gif"}:
            file_name = uuid.uuid4().hex + "." + expansion_name
        else:
            self.send_response(303)
            self.send_header("Location", "/?error=1")
            self.end_headers()
        
        path_local = f"./images/{file_name}"
                
        # запис унікальної назви файлу
        # with open(f"{path_local}", "wb") as file_upload:
        #     file_upload.write(data)


        f = open(path_local, "wb")
        f.write(data)
        f.close()

        # print(f"f", f, flush=True)

        
        self.send_response(303)
        # self.send_header("Location", f"/?uploaded=1")
        self.send_header("Location", f"/?uploaded=1&file={path_local}")
        self.end_headers()
  
        # self.send_response(200)
        # self.send_header("Content-Type", "text/plain")
        # self.end_headers()
        
        # self.wfile.write(f"http://locolhost:8080/{path_local}".encode())

   
server = HTTPServer(("0.0.0.0", 8000), Handler)
server.serve_forever()
