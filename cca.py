import numpy as np
from skimage import morphology,measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import localization

# Remove small objects from the binary image
binary_clean = morphology.remove_small_objects(localization.binary_car_image, 50)

# Calculate the vertical and horizontal projection of the image
vertical_proj = np.sum(binary_clean, axis=0)
horizontal_proj = np.sum(binary_clean, axis=1)

# Retrieve the columns that have 96% of the max vertical and horizontal projection value of the image
threshold_v = np.max(vertical_proj) * 0.96
threshold_h = np.max(horizontal_proj) * 0.96
cols = np.where(vertical_proj > threshold_v)[0]
rows = np.where(horizontal_proj > threshold_h) [0]

# Define the limits of the portion of the image that more probably has the plate
if len(cols) > 0:
    x_min, x_max = cols[0], cols[-1]
    y_min, y_max = rows[0], rows[-1]

# Redefine the images to the region of intrest
localization.binary_car_image = localization.binary_car_image[y_min:y_max, x_min:x_max]
localization.gray_car_image = localization.gray_car_image[y_min:y_max, x_min:x_max]

# Find the Label connected regions of the images
label_image = measure.label(localization.binary_car_image)

# Define the dimensios for an acceptable label connected region
plate_dimensions = (0.15*label_image.shape[0], 0.5*label_image.shape[0], 0.3*label_image.shape[1], 0.8*label_image.shape[1])
min_height, max_height, min_width, max_width = plate_dimensions
plate_objects_cordinates = []
plate_like_objects = []

fig, (ax1) = plt.subplots(1)
ax1.imshow(localization.gray_car_image, cmap="gray")

for region in regionprops(label_image):
    # Ignore small objects from binary image
    if region.area < 50:
        continue

    minRow, minCol, maxRow, maxCol = region.bbox
    region_height = maxRow - minRow
    region_width = maxCol - minCol

    # Search for regions that fit the acceptable dimensions
    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        plate_like_objects.append(localization.binary_car_image[minRow:maxRow, minCol:maxCol])
        plate_objects_cordinates.append((minRow, minCol, maxRow, maxCol))

        # Draw a box indicating the region found in the image
        rectBorder = patches.Rectangle((minCol, minRow), maxCol-minCol, maxRow-minRow, edgecolor="red", linewidth=2, fill=False)
        ax1.add_patch(rectBorder)

plt.savefig("potential_regions.png")    