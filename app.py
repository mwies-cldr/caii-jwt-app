import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class EchoRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Capture Environment Variables
        env_vars = dict(os.environ)

        # 2. Capture HTTP Headers
        # self.headers behaves like a dictionary
        headers = dict(self.headers)

        # 3. Capture the POST Payload
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            payload = self.rfile.read(content_length).decode('utf-8')
        else:
            payload = ""

        # Construct the response dictionary
        response_data = {
            "environment_variables": env_vars,
            "headers": headers,
            "payload": payload
        }

        # Send HTTP status code 200 (OK)
        self.send_response(200)
        
        # Send HTTP headers
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Write the JSON response
        self.wfile.write(json.dumps(response_data, indent=4).encode('utf-8'))

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, EchoRequestHandler)
    print(f"Server is running on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
