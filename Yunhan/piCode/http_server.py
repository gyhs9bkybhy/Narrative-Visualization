import io
from picamera import PiCamera
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler
from threading import Condition


class FrameBuffer(object):
    def __init__(self):
        # store each frame
        self.frame = None
        # buffer to hold incoming frame
        self.buffer = io.BytesIO()
        # synchronize between threads
        self.condition = Condition()

    def write(self, buf):
        # if it's a JPEG image
        if buf.startswith(b'\xff\xd8'):
            with self.condition:
                # write to buffer
                self.buffer.seek(0)
                self.buffer.write(buf)
                # extract frame
                self.buffer.truncate()
                self.frame = self.buffer.getvalue()   
                self.condition.notify_all()



def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


class StreamingHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        global frame_buffer
        if (self.path == '/stream.mjpg') or (self.path == 'http://192.168.3.14:8000/stream.mjpg'):
            # response
            self.send_response(200)
            # header
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()

            try:
                while True:
                    with frame_buffer.condition:
                        # wait for a new frame
                        frame_buffer.condition.wait()
                        frame = frame_buffer.frame # need frame_buffer as global
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')

            except Exception as e:
                print(str(e))
        else:
            super().do_GET()


frame_buffer = FrameBuffer()

camera = PiCamera(resolution='640x480', framerate=24)
camera.start_recording(frame_buffer, format='mjpeg')

server_address = ('', 8000)
handler_class = StreamingHandler # alias
try:
    httpd = HTTPServer(server_address, handler_class)
    httpd.serve_forever()
finally:
    camera.stop_recording()