import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from skimage.io import imread

from text_detector import detect_text_regions

image_sample = 'sample_images/image6.jpg'
image = imread(image_sample)
box_groups = detect_text_regions(image)

fig, ax = plt.subplots()
for box in box_groups:
    minr = box[0]
    minc = box[1]
    maxr = box[2]
    maxc = box[3]
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)

ax.add_patch(rect)
ax.imshow(image)
ax.set_axis_off()
plt.tight_layout()
plt.show()
