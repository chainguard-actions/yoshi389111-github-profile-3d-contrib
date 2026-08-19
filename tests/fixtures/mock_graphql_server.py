#!/usr/bin/env python3
"""Mock GraphQL server for testing github-profile-3d-contrib action."""
import http.server
import json
import os
import sys


class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            self.rfile.read(content_length)
        response_file = os.environ.get('MOCK_RESPONSE_FILE', '/tmp/graphql_response.json')
        with open(response_file, 'rb') as f:
            body = f.read()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18080
    server = http.server.HTTPServer(('127.0.0.1', port), Handler)
    server.serve_forever()


if __name__ == '__main__':
    main()
