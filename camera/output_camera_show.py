from pypylon import pylon
import numpy as np
import cv2
import datetime, os

# Mapping from camera serial numbers to names.
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

# Initialize Basler cameras.
devices = pylon.TlFactory.GetInstance().EnumerateDevices()
camera_array = pylon.InstantCameraArray(len(devices))
for camera, device in zip(camera_array, devices):
    camera.Attach(pylon.TlFactory.GetInstance().CreateDevice(device))

camera_array.Open()
for camera in camera_array:
    camera.ExposureTime.SetValue(1500.0)

# Start grabbing continuously.
camera_array.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# Create directories for saving images.
for camera in camera_array:
    serial = camera.GetDeviceInfo().GetSerialNumber()
    os.makedirs(f"/home/bmw/Documents/data/test/{camera_serial_to_name[serial]}/", exist_ok=True)

# Dictionary to hold the latest image for each camera (keyed by serial).
latest_images = {}

# Define the fixed grid layout (3x3).
# Row 1: front_left, front_mid, front_right.
# Row 2: mid_left, empty, mid_right.
# Row 3: rear_left, rear_mid, rear_right.
grid_order = [
    "front_left", "front_mid", "front_right",
    "mid_left",    "empty",     "mid_right",
    "rear_left",   "rear_mid",  "rear_right"
]

# Create a resizable window.
cv2.namedWindow("All Cameras", cv2.WINDOW_NORMAL)

try:
    while True:
        try:
            # Attempt to retrieve a single frame (up to 5000 ms timeout).
            grab_result = camera_array.RetrieveResult(5000, pylon.TimeoutHandling_Return)
            if grab_result is not None and grab_result.GrabSucceeded():
                cam = camera_array[grab_result.GetCameraContext()]
                serial = cam.GetDeviceInfo().GetSerialNumber()
                cam_name = camera_serial_to_name[serial]

                # Convert the grabbed image and resize it.
                image = converter.Convert(grab_result)
                img = image.GetArray()
                img_resized = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)

                # Save the image with a timestamp.
                timestamp = datetime.datetime.now().isoformat()
                cv2.imwrite(f"/home/bmw/Documents/data/test/{cam_name}/{timestamp}.jpeg", img_resized)

                # Update the latest image for this camera.
                latest_images[serial] = img_resized.copy()
            if grab_result is not None:
                grab_result.Release()
        except Exception:
            # On timeout or error, just continue.
            pass

        # Build a mapping from camera name to latest image.
        latest_by_name = {}
        for serial, img in latest_images.items():
            name = camera_serial_to_name.get(serial)
            if name:
                latest_by_name[name] = img

        # Build the list of images for our grid in the desired order.
        display_images = []
        for name in grid_order:
            if name == "empty":
                # Use a black placeholder for the empty cell.
                display_images.append(np.zeros((480, 640, 3), dtype=np.uint8))
            elif name in latest_by_name:
                # Overlay the camera name on the image.
                img_copy = latest_by_name[name].copy()
                cv2.putText(img_copy, name.replace("_", " ").title(), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                display_images.append(img_copy)
            else:
                # If no image is available, use a placeholder.
                display_images.append(np.zeros((480, 640, 3), dtype=np.uint8))

        # Manually construct a 3x3 grid.
        row1 = cv2.hconcat(display_images[0:3])
        row2 = cv2.hconcat(display_images[3:6])
        row3 = cv2.hconcat(display_images[6:9])
        grid = cv2.vconcat([row1, row2, row3])

        # Dynamically resize the grid if it is too wide.
        max_width = 800
        if grid.shape[1] > max_width:
            scaling_factor = max_width / grid.shape[1]
            new_width = int(grid.shape[1] * scaling_factor)
            new_height = int(grid.shape[0] * scaling_factor)
            grid_display = cv2.resize(grid, (new_width, new_height))
        else:
            grid_display = grid

        cv2.imshow("All Cameras", grid_display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    camera_array.StopGrabbing()
    cv2.destroyAllWindows()
