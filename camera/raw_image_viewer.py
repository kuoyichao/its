import cv2
import numpy as np

# Path to the Bayer 8-bit PNG image
bayer_png_path = "/media/bmw/data01/2025_02_26_145300/front_mid/front_mid_20250226_145306_675537.png"

# Read the Bayer image (8-bit)
bayer_image = cv2.imread(bayer_png_path, cv2.IMREAD_GRAYSCALE)

# Check if the image was read correctly
if bayer_image is None:
    print("Error: Unable to read the Bayer image.")
else:
    print(f"Image shape: {bayer_image.shape}")  # Print the shape to verify dimensions

    # Demosaic the Bayer image to RGB (BayerRG8 assumed here, change if necessary)
    rgb_image = cv2.cvtColor(bayer_image, cv2.COLOR_BayerRG2BGR)  # Change if using different Bayer format

    # Display the RGB image
    cv2.imshow("Converted RGB Image", rgb_image)

    # Wait until a key is pressed
    cv2.waitKey(0)

    # Close all OpenCV windows
    cv2.destroyAllWindows()
