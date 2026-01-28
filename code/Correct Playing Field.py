import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd

# Load the map image (Map2.png)
image_path = "Map2.png"
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define a range to exclude white-ish pixels (i.e., keep everything that is NOT white)
white_lower = np.array([245, 245, 245])
white_upper = np.array([255, 255, 255])

# Create a mask where non-white (colored) pixels = valid playable area
white_mask = cv2.inRange(image_rgb, white_lower, white_upper)
mask = cv2.bitwise_not(white_mask)  # invert so white = 0, playable = 1

# Optional: Show the mask
plt.imshow(mask, cmap='gray')
plt.title("Playable Area Mask (White = Valid)")
plt.axis('off')
plt.show()

# Function to check if a given (x, y) is in the playable area
def is_valid(x, y, mask):
    h, w = mask.shape
    xi, yi = int(round(y)), int(round(x))  # y = row, x = column
    if 0 <= xi < h and 0 <= yi < w:
        return mask[xi, yi] > 0
    return False

# Example: test a coordinate
test_x, test_y = 600, 400
print(f"Is ({test_x}, {test_y}) valid? ", is_valid(test_x, test_y, mask))