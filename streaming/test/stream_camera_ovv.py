from flask import Flask, Response
import cv2

app = Flask(__name__)

# # GStreamer pipeline for capturing video from a webcam
# # Adjust this pipeline based on your camera and requirements
# gst_pipeline = (
#     "dshowsrc ! video/x-raw,width=640,height=480,framerate=30/1 ! "
#     "videoconvert ! video/x-raw,format=BGR ! appsink"
# )

# # Initialize the GStreamer pipeline with OpenCV
# camera = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
camera = cv2.VideoCapture(0)  # Uses the default backend (e.g., DirectShow on Windows)


def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<html><body><h1>Live Stream</h1><img src='/video' width='640'></body></html>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)