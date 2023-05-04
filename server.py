from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from mra_control import mra_device, Gain

class MRARequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)

        if path == '/control':
            try:
                device = mra_device(path=f"{query['deviceid'][0]}")
                if 'standby' in query:
                    device.standby(query['standby'][0] == 'true')
                if 'mute' in query:
                    device.mute(query['mute'][0] == 'true')
                if 'gain' in query:
                    device.set_gain(Gain.from_string(query['gain'][0]))
            except Exception as e:
                print(f"Error opening device: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes("Error opening device", "utf-8"))
                return
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("OK", "utf-8"))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("Not found", "utf-8"))   

def run():
    print('starting server...')
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, MRARequestHandler)
    print('running server...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()