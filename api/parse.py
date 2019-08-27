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

    def do_GET(self):
        url = None
        query = urlparse(self.path).query
        if query:
            query_components = dict(qc.split('=') for qc in query.split('&'))
            url = query_components.get('url')
        if not url:
            self.send_error(400, 'Missing url GET parameter')
            return
        data = self.get_metadatas(url)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Cache-Control', 'maxage=0, s-maxage=86400')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        return
