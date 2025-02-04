import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import cv2
import threading
from typing import AsyncGenerator
from contextlib import asynccontextmanager
import uvicorn

class VideoFileReader:
    """
    A class to handle video capture from a video file.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the video file reader.

        :param file_path: Path to the video file.
        """
        self.file_path = file_path
        self.cap = cv2.VideoCapture(file_path)
        self.lock = threading.Lock()

    def get_frame(self) -> bytes:
        """
        Capture a frame from the video file.

        :return: JPEG encoded image bytes.
        """
        with self.lock:
            ret, frame = self.cap.read()
            if not ret:
                # Restart the video if it reaches the end
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
                if not ret:
                    return b''

            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                return b''

            return jpeg.tobytes()

    def release(self) -> None:
        """
        Release the video file resource.
        """
        with self.lock:
            if self.cap.isOpened():
                self.cap.release()


video_file_reader: VideoFileReader | None = None  # Global placeholder

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    global video_file_reader
    video_file_reader = VideoFileReader("C:/Users/kuoyi/Downloads/D-Day_360.mp4")  # Set your video path
    print("Video file reader initialized.")
    
    try:
        yield
    except asyncio.CancelledError as error:
        print("Lifespan error:", error.args)
    finally:
        if video_file_reader:
            video_file_reader.release()
            print("Video resource released.")


app = FastAPI(lifespan=lifespan)


async def gen_frames() -> AsyncGenerator[bytes, None]:
    """
    An asynchronous generator function that yields video frames.

    :yield: JPEG encoded image bytes.
    """
    global video_file_reader
    try:
        while True:
            frame = video_file_reader.get_frame() if video_file_reader else b''
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break
            await asyncio.sleep(0.03)  # Adjust the delay to control the frame rate
    except (asyncio.CancelledError, GeneratorExit):
        print("Frame generation cancelled.")
    finally:
        print("Frame generator exited.")


@app.get("/video")
async def video_feed() -> StreamingResponse:
    """
    Video streaming route.

    :return: StreamingResponse with multipart JPEG frames.
    """
    return StreamingResponse(
        gen_frames(),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )


@app.get("/")
async def index() -> HTMLResponse:
    """
    Serve an HTML page with an <img> tag to stream video.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Live Video Stream</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #000;
            }
            img {
                max-width: 100%;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
            }
        </style>
    </head>
    <body>
        <img src="/video" alt="Live Video Stream">
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == '__main__':
    # Run FastAPI on the local network
    uvicorn.run(app, host="0.0.0.0", port=5000)
