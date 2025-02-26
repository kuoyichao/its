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
recording_name = "2025_02_25_round_3"

# Set the base folder path using the recording name
base_folder = f"/media/bmw/data01/{recording_name}"
os.makedirs(base_folder, exist_ok=True)

# Connect to available cameras
devices = pylon.TlFactory.GetInstance().EnumerateDevices()
camera_array = pylon.InstantCameraArray(len(devices))
for camera, device in zip(camera_array, devices):
    camera.Attach(pylon.TlFactory.GetInstance().CreateDevice(device))

camera_array.Open()

# Configure cameras (e.g., 30 FPS and exposure time)
for camera in camera_array:
    camera.AcquisitionFrameRate.SetValue(30.0)
    camera.ExposureTime.SetValue(30000.0)

# Start grabbing images (using the latest image only)
camera_array.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# Set up metadata CSV file
metadata_file = f"{base_folder}/metadata.csv"
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
with open(metadata_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'camera_name', 'exposure_time'])

while True:
    if camera_array.IsGrabbing():
        grab_result = camera_array.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grab_result.GrabSucceeded():
            # Identify which camera captured this image
            camera = camera_array[grab_result.GetCameraContext()]
            serial = camera.GetDeviceInfo().GetSerialNumber()
            camera_name = camera_serial_to_name[serial]
            
            # Get raw buffer data
            buffer_size = grab_result.GetBufferByteCount()
            raw_data = np.frombuffer(grab_result.GetBuffer(), dtype=np.uint8, count=buffer_size)
            
            # Create timestamp and folder for this camera
            timestamp = datetime.datetime.now().isoformat()
            print(timestamp)
            camera_folder = f"{base_folder}/{camera_name}"
            os.makedirs(camera_folder, exist_ok=True)
            
            # Save raw data to a file (e.g. using .raw extension)
            raw_filename = f"{camera_folder}/{timestamp}.raw"
            raw_data.tofile(raw_filename)
            
            # Save metadata
            with open(metadata_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, camera_name, camera.ExposureTime.GetValue()])
            
            # Press 'q' to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        grab_result.Release()
    else:
        raise Exception("Camera is not grabbing!")

# Stop capturing and clean up
camera_array.StopGrabbing()
cv2.destroyAllWindows()