from http.server import HTTPServer, CGIHTTPRequestHandler

ADDRESS = ('', 8000)
httpd = HTTPServer(ADDRESS, CGIHTTPRequestHandler)
httpd.serve_forever()
