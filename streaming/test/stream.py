import threading
from flask import Flask, Response, render_template_string
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

app = Flask(__name__)

def gstreamer_pipeline():
    return (
        "v4l2src device=/dev/video0 ! "
        "videoconvert ! "
        "video/x-raw,format=YUY2 ! "
        "jpegenc quality=85 ! "
        "multipartmux boundary=spionisto ! "
        "tcpserversink host=0.0.0.0 port=5000"
    )

def run_gstreamer():
    pipeline = Gst.parse_launch(gstreamer_pipeline())
    pipeline.set_state(Gst.State.PLAYING)
    
    # Wait for pipeline to end
    bus = pipeline.get_bus()
    bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)
    pipeline.set_state(Gst.State.NULL)

@app.route('/')
def index():
    return render_template_string('''
        <html>
            <body>
                <h1>Webcam Stream</h1>
                <img src="/stream" />
            </body>
        </html>
    ''')

@app.route('/stream')
def stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=spionisto')

def generate_frames():
    # Connect to the GStreamer TCP server
    import socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))
    
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            yield data
    finally:
        client.close()

if __name__ == '__main__':
    # Start GStreamer in a separate thread
    threading.Thread(target=run_gstreamer, daemon=True).start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=8000, debug=False)