#!/usr/bin/python3

from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import json
import request as rq
import binary as bn
import convolution as cv

SERVER_PORT = 24111


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in separate threads"""


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        # Get request content length
        content_length = int(self.headers.get('Content-Length', 0))

        # Parse content
        body = self.rfile.read(content_length).decode('utf-8')

        # Serialize content
        request_content = rq.ContentRequest.from_dict(json.loads(body))

        # Load image from bytes
        image_bytes = cv.bytes_to_image(
            request_content.input.content, request_content.grayscale)

        # Parse kernel from bytes
        parsed_kernel = cv.list_to_kernel(request_content.kernel)

        # Create convolution
        convolution = cv.convolute_image(
            image_bytes, parsed_kernel, request_content.times)

        # Transform to bytes
        image_bytes = bn.BinaryFile(cv.image_to_bytes(
            convolution, request_content.extension))

        # Regenerate response
        payload = image_bytes.encode()

        # Create response headers
        self.send_response(200)
        self.send_header('Content-type', 'plain/text')
        self.end_headers()

        # Send response body
        self.wfile.write(payload.encode('ascii'))


if __name__ == '__main__':
    # Server listening on port
    print(f"Server listening in port: {SERVER_PORT}")

    # Create HTTP server
    server = ThreadedHTTPServer(('localhost', SERVER_PORT), HTTPRequestHandler)
    server.serve_forever()
