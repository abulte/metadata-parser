import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

import metadata_parser


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        url = None
        query = urlparse(self.path).query
        if query:
            query_components = dict(qc.split('=') for qc in query.split('&'))
            url = query_components.get('url')
        if not url:
            self.send_error(400, 'Missing url GET parameter')
            return
        page = metadata_parser.MetadataParser(url=url)
        data = {
            'title': page.get_metadatas('title')[0],
            'description': page.get_metadatas('description')[0],
            'image': page.get_metadatas('image')[0]
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Cache-Control', 'maxage=0, s-maxage=86400')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        return
