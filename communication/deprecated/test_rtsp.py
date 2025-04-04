#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  20 02:07:13 2019

@author: prabhakar
"""
# import necessary argumnets
import gi
import cv2
import argparse
import datetime

# import required library like Gstreamer and GstreamerRtspServer
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject, GLib


# Sensor Factory class which inherits the GstRtspServer base class and add
# properties to it.
class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(SensorFactory, self).__init__(**properties)
        self.number_frames = 0
        self.fps = opt.fps
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width={},height={} ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96' \
            .format(opt.image_width, opt.image_height) #, self.fps ,framerate={}/1

    # method to capture the video feed from the camera and push it to the
    # streaming buffer.
    def on_need_data(self, src, length):
        now = datetime.datetime.now()
        frame = cv2.imread(
            '/home/lukas/src/its/data/camera_simulator/s110_s_cam_8/s110_s_cam_8_images_distorted/1690366190213.jpg')
        frame = cv2.putText(frame, str(now), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # It is better to change the resolution of the camera
        # instead of changing the image shape as it affects the image quality.
        frame = cv2.resize(frame, (opt.image_width, opt.image_height), interpolation=cv2.INTER_LINEAR)
        data = frame.tobytes()
        buf = Gst.Buffer.new_allocate(None, len(data), None)
        buf.fill(0, data)
        buf.duration = self.duration
        timestamp = self.number_frames * self.duration
        buf.pts = buf.dts = int(timestamp)
        buf.offset = timestamp
        self.number_frames += 1
        retval = src.emit('push-buffer', buf)
        print('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.number_frames,
                                                                               self.duration,
                                                                               self.duration / Gst.SECOND))
        if retval != Gst.FlowReturn.OK:
            print(retval)

    # attach the launch string to the override method
    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    # attaching the source element to the rtsp media
    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


# Rtsp server implementation where we attach the factory sensor with the stream uri
class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)
        self.factory = SensorFactory()
        self.factory.set_shared(True)
        self.set_service(str(opt.port))
        self.get_mount_points().add_factory(opt.stream_uri, self.factory)
        self.attach(None)


# getting the required information from the user
parser = argparse.ArgumentParser()
parser.add_argument("--fps", default=15, help="fps of the camera", type=int)
parser.add_argument("--image_width", default=1920, help="video frame width", type=int)
parser.add_argument("--image_height", default=1200, help="video frame height", type=int)
parser.add_argument("--port", default=8554, help="port to stream video", type=int)
parser.add_argument("--stream_uri", default="/video_stream", help="rtsp video stream uri")
opt = parser.parse_args()

# initializing the threads and running the stream on loop.
Gst.init(None)
server = GstServer()
loop = GLib.MainLoop()
loop.run()
