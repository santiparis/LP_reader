from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt

# Insert the image in  grayscale
car_image = imread("car.jpg", as_gray="gray")

print(car_image.shape)

# Recolor the image to gray scale
gray_car_image = car_image * 255
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(gray_car_image, cmap="gray")

# Make the imgage binary (only black or white pixels)
threshold_value = threshold_otsu(gray_car_image)
binary_car_image = gray_car_image > threshold_value
ax2.imshow(binary_car_image, cmap="gray")

plt.savefig("greyscale_vs_binary.png")