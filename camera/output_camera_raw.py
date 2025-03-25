from pypylon import pylon
import numpy as np
import datetime, os, csv
import cv2

# Mapping of camera serial numbers to human-readable names
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

# Generate a recording folder name based on the current date and start time
start_time = datetime.datetime.now()
recording_name = start_time.strftime("%Y_%m_%d_%H%M%S")
base_folder = f"/media/bmw/data01/{recording_name}"
os.makedirs(base_folder, exist_ok=True)

# Connect to available cameras
devices = pylon.TlFactory.GetInstance().EnumerateDevices()
camera_array = pylon.InstantCameraArray(len(devices))
for camera, device in zip(camera_array, devices):
    camera.Attach(pylon.TlFactory.GetInstance().CreateDevice(device))

camera_array.Open()

# Configure cameras (15 FPS, 30000µs exposure, Bayer format)
for camera in camera_array:
    camera.AcquisitionFrameRate.SetValue(30.0)
    camera.ExposureTime.SetValue(30000.0)
    
    # Set pixel format to Bayer (8-bit BayerRG8)
    camera.PixelFormat.SetValue("BayerRG8")  # "BayerRG8" for 8-bit Bayer format

camera_array.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# Setup metadata CSV with headers
metadata_file = f"{base_folder}/metadata.csv"
with open(metadata_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'camera_serial', 'camera_name', 'exposure_time', 'image_filename'])

while True:
    if camera_array.IsGrabbing():
        grab_result = camera_array.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grab_result.GrabSucceeded():
            # Get camera info
            camera = camera_array[grab_result.GetCameraContext()]
            serial = camera.GetDeviceInfo().GetSerialNumber()
            cam_name = camera_serial_to_name.get(serial, "unknown")
            
            # Create a subfolder for this camera if it doesn't exist
            camera_folder = f"{base_folder}/{cam_name}"
            os.makedirs(camera_folder, exist_ok=True)
            
            # Get full-resolution Bayer image (raw Bayer data)
            img = grab_result.Array  # Already in Bayer format
            
            # Convert Bayer image to RGB using OpenCV demosaicing (Bayer to BGR)
            bgr_image = cv2.cvtColor(img, cv2.COLOR_BayerRG2BGR)  # Adjust for Bayer format if necessary

            # Generate unique filename using timestamp
            file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            png_filename = f"{cam_name}_{file_timestamp}.png"
            timestamp_iso = datetime.datetime.now().isoformat()
            print(timestamp_iso, serial, cam_name)
            
            # Save image as PNG
            cv2.imwrite(f"{camera_folder}/{png_filename}", bgr_image)
            # cv2.imshow(f"RGB Image - {cam_name}", bgr_image)
            # Append metadata
            with open(metadata_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp_iso, serial, cam_name, camera.ExposureTime.GetValue(), png_filename])

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        grab_result.Release()
    else:
        raise Exception("Camera is not grabbing!")

# Stop capturing and clean up
camera_array.StopGrabbing()
cv2.destroyAllWindows()
