from pypylon import pylon
import numpy as np
import cv2
import datetime, os, csv

camera_serial_to_name = {
    "40580664": "front_left",
    "40580656": "front_mid",
    "40580658": "front_right",
    "40580666": "mid_left",
    "40580651": "mid_right",
    "40580657": "rear_left",
    "40542479": "rear_mid",
    "40539559": "rear_right"
}

# Set recording name here (change this to whatever name you want)
recording_name = "2025_02_25_round_1"

# Set the base folder path using the recording name
base_folder = f"/media/bmw/data01/{recording_name}"

# Connecting to the first available camera
devices = pylon.TlFactory.GetInstance().EnumerateDevices()
camera_array = pylon.InstantCameraArray(len(devices))
for camera, device in zip(camera_array, devices):
    camera.Attach(pylon.TlFactory.GetInstance().CreateDevice(device))

camera_array.Open()

# Set cameras to 30 FPS
for camera in camera_array:
    camera.AcquisitionFrameRate.SetValue(30.0)
    camera.ExposureTime.SetValue(1500.0)

camera_array.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# VideoWriter object for saving video (MJPEG, 30 FPS, 640x480 resolution)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(f"{base_folder}/video_output.avi", fourcc, 30, (640, 480))

# Metadata file
metadata_file = f"{base_folder}/metadata.csv"
with open(metadata_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'camera_name', 'exposure_time'])

i = 0
while True:
    if camera_array.IsGrabbing():
        grab_result = camera_array.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grab_result.GrabSucceeded():
            camera = camera_array[grab_result.GetCameraContext()]
            camera_name = camera_serial_to_name[camera.GetDeviceInfo().GetSerialNumber()]

            image = pylon.ImageFormatConverter().Convert(grab_result)
            img = image.GetArray()

            img2 = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)

            timestamp = datetime.datetime.now().isoformat()

            # Create a folder for each camera if it doesn't exist
            camera_folder = f"{base_folder}/{camera_name}"
            os.makedirs(camera_folder, exist_ok=True)

            # Save image as PNG
            cv2.imwrite(f"{camera_folder}/{timestamp}.png", img2)

            # Write to video
            out.write(img2)

            # Save metadata
            with open(metadata_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, camera_name, camera.ExposureTime.GetValue()])

            i += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        grab_result.Release()
    else:
        raise Exception("Camera is not grabbing!")

# Stop capturing and release video
camera_array.StopGrabbing()
out.release()
cv2.destroyAllWindows()
