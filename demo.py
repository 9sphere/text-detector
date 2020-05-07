import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from skimage.io import imread

from text_detector import detect_text_regions

image_name = 'image6.jpg'
image_sample = 'sample_images/'+image_name
image = imread(image_sample)
box_groups = detect_text_regions(image)

fig, ax = plt.subplots()
for box in box_groups:
    minr = box[0]
    minc = box[1]
    maxr = box[2]
    maxc = box[3]
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=1)
    ax.add_patch(rect)

ax.imshow(image)
ax.set_axis_off()
plt.tight_layout()
plt.savefig('sample_images/outputs/'+image_name, bbox_inches='tight', transparent="True", pad_inches=0)
plt.show()
