import io
from picamera import PiCamera

global frame_buffer

class FrameBuffer(object):
    def __init__(self):
        # store each frame
        self.frame = None
        # buffer to hold incoming frame
        self.buffer = io.BytesIO()

    def write(self, buf):
        # if it's a JPEG imagee
        if buf.startswith(b'\xff\xd8'):
            # write to buffer
            self.buffer.seek(0)
            self.buffer.write(buf)
            # extract frame
            self.buffer.truncate()
            self.frame = self.buffer.getvalue()

frame_buffer = FrameBuffer()

camera = PiCamera(resolution='640x480', framerate=24)
camera.start_recording(frame_buffer, format='mjpeg')

server_address = ('', 65432)
handler_class = StreamingHandler # alias
try:
    httpd = HTTPServer(server_address, handler_class)
    httpd.serve_forever()
finally:
    camera.stop_recording()