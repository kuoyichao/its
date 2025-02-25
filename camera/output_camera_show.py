import cv2
import numpy as np
from pypylon import pylon
import datetime, os

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

# --- Load and resize your custom car image (e.g., top-down car) ---
# Replace this path with the actual location of your image.
car_image = cv2.imread("./top_view.png")
# Force a 640×480 size to match the other cells:
car_image = cv2.resize(car_image, (640, 480), interpolation=cv2.INTER_LINEAR)

# Initialize Basler cameras
tl_factory = pylon.TlFactory.GetInstance()
devices = tl_factory.EnumerateDevices()
camera_array = pylon.InstantCameraArray(len(devices))
for cam, dev in zip(camera_array, devices):
    cam.Attach(tl_factory.CreateDevice(dev))

camera_array.Open()
for cam in camera_array:
    cam.ExposureTime.SetValue(1500.0)

camera_array.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# Create directories for saving images.
for camera in camera_array:
    serial = camera.GetDeviceInfo().GetSerialNumber()
    # os.makedirs(f"/media/bmw/data01/2025_02_20_test2/{camera_serial_to_name[serial]}/", exist_ok=True)

# Dictionary to hold the latest image for each camera (keyed by serial).
latest_images = {}

# 3×3 grid layout:
# 1) front_left, front_mid, front_right
# 2) mid_left, [car image], mid_right
# 3) rear_left, rear_mid, rear_right
grid_order = [
    "front_left", "front_mid",  "front_right",
    "mid_left",   "car_image",  "mid_right",
    "rear_left",  "rear_mid",   "rear_right"
]

# Create a resizable window
cv2.namedWindow("All Cameras", cv2.WINDOW_NORMAL)

try:
    while True:
        # Retrieve one frame quickly to avoid blocking real-time display
        try:
            grab_result = camera_array.RetrieveResult(100, pylon.TimeoutHandling_Return)
            if grab_result is not None and grab_result.GrabSucceeded():
                cam = camera_array[grab_result.GetCameraContext()]
                serial = cam.GetDeviceInfo().GetSerialNumber()
                cam_name = camera_serial_to_name[serial]

                # Convert to OpenCV format
                image = converter.Convert(grab_result)
                img = image.GetArray()
                # Resize to 640×480 to keep a uniform grid cell
                img_resized = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)

                # Save the image with a timestamp.
                timestamp = datetime.datetime.now().isoformat()
                # cv2.imwrite(f"/media/bmw/data01/2025_02_20_test2/{cam_name}/{timestamp}.jpeg", img_resized)

                # Update the latest image for this camera.
                latest_images[serial] = img_resized.copy()
            if grab_result is not None:
                grab_result.Release()
        except Exception:
            # On timeout or error, just continue
            pass

        # Build a map from camera name to image
        name_to_image = {}
        for serial, frame in latest_images.items():
            cam_name = camera_serial_to_name.get(serial)
            if cam_name:
                name_to_image[cam_name] = frame

        # Collect each cell in the grid in order
        display_images = []
        for name in grid_order:
            if name == "car_image":
                # Use the custom car image for the center cell
                display_images.append(car_image)
            elif name in name_to_image:
                # Overlay camera name text
                img_copy = name_to_image[name].copy()
                text_label = name.replace("_", " ").title()
                cv2.putText(img_copy, text_label, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                display_images.append(img_copy)
            else:
                # If we have no image for this cell yet, use a black placeholder
                display_images.append(np.zeros((480, 640, 3), dtype=np.uint8))

        # Construct rows
        row1 = cv2.hconcat(display_images[0:3])
        row2 = cv2.hconcat(display_images[3:6])
        row3 = cv2.hconcat(display_images[6:9])
        grid = cv2.vconcat([row1, row2, row3])

        # Dynamically resize the final grid if it’s too wide
        max_width = 800
        if grid.shape[1] > max_width:
            scale = max_width / grid.shape[1]
            new_w = int(grid.shape[1] * scale)
            new_h = int(grid.shape[0] * scale)
            grid_display = cv2.resize(grid, (new_w, new_h))
        else:
            grid_display = grid

        # Show the result
        cv2.imshow("All Cameras", grid_display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    camera_array.StopGrabbing()
    cv2.destroyAllWindows()
