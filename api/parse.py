import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

import metadata_parser


class handler(BaseHTTPRequestHandler):

    FIELDS = ('title', 'description', 'image')

    def get_metadatas(self, url):
        page = metadata_parser.MetadataParser(url=url)
        metadatas = {}
        for f in self.FIELDS:
            meta = page.get_metadatas(f)
            value = meta[0] if meta else None
            metadatas[f] = value
        return metadatas

    def add_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range')  # noqa
        self.send_header('Access-Control-Expose-Headers', 'Content-Length,Content-Range') # noqa

    def do_OPTIONS(self):
        self.send_response(204)
        self.add_cors_headers()
        self.send_header('Access-Control-Max-Age', 1728000)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', 0)
        self.end_headers()

    def do_GET(self):
        url = None
        query = urlparse(self.path).query
        if query:
            query_components = dict(qc.split('=') for qc in query.split('&'))
            url = query_components.get('url')
        if not url:
            self.send_error(400, 'Missing url GET parameter')
            return
        try:
            data = self.get_metadatas(url)
        except metadata_parser.NotParsable:
            self.send_response(500)
            data = {'error': 'Unable to parse url'}
        else:
            self.send_response(200)
            self.send_header('Cache-Control', 'maxage=0, s-maxage=86400')
        finally:
            self.send_header('Content-type', 'application/json')
            self.add_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
