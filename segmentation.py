import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import cca

# Find the region with the place (If all went ok the only region left in the list should be the plate, this is improvable of course)
license_plate = np.invert(cca.plate_like_objects[0])

# Find the label connected regions of the place image
labelled_plate = measure.label(license_plate)

fig, ax1 = plt.subplots(1)
ax1.imshow(license_plate, cmap="gray")

# Define the acceptable dimensions for the characters in the plate
character_dimensions = (0.5*license_plate.shape[0], 0.8*license_plate.shape[0], 0.05*license_plate.shape[1], 0.2*license_plate.shape[1])
min_height, max_height, min_width, max_width = character_dimensions

characters = []
counter = 0
column_list = []

for regions in regionprops(labelled_plate):
    y0, x0, y1, x1 = regions.bbox
    region_height = y1 - y0
    region_width = x1 - x0
    
    # Find the regions of the plate image that fit the acceptable dimensions
    if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
        roi = license_plate[y0:y1, x0:x1]

        # Draw a rectangle around the region
        rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red", linewidth=2, fill=False)
        ax1.add_patch(rect_border)

        # Resize the character to 20px by 20px
        resized_char = resize(roi, (20, 20))
        characters.append(resized_char)

        # Save the first column (from left to right) of the region (for ordering later)
        column_list.append(x0)

plt.savefig("plate.png")