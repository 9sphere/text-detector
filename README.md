# text-detector (algorithm accuracy work in progress)
Locating texts in images using machine vision algorithms

This project aims to use only image processing techniques to locate text regions in the image. More detailed information about the approach is given this link  
https://muthu.co/?p=1367&preview=true

## Installation
```
pip install -r requirements.txt
```

## Usage
```

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from skimage.io import imread

from text_detector import detect_text_regions

image_sample = 'sample_images/image7.jpg'
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

```

## Sample Results
| Original | Detected Text Regions |
|:----------------------------------------|:------------------------------------------------|
| <img src="https://raw.githubusercontent.com/muthuspark/text-detector/master/sample_images/image1.jpg" width="300" height="auto"> | <img src="https://raw.githubusercontent.com/muthuspark/text-detector/master/sample_images/outputs/image1.jpg" width="300" height="auto"> |
| <img src="https://raw.githubusercontent.com/muthuspark/text-detector/master/sample_images/image2.jpg" width="300" height="auto"> | <img src="https://raw.githubusercontent.com/muthuspark/text-detector/master/sample_images/outputs/image2.jpg" width="300" height="auto"> |
| <img src="https://raw.githubusercontent.com/muthuspark/text-detector/master/sample_images/image3.jpg" width="300" height="auto"> | <img src="https://raw.githubusercontent.com/muthuspark/text-detector/master/sample_images/outputs/image3.jpg" width="300" height="auto"> |
| <img src="https://raw.githubusercontent.com/muthuspark/text-detector/master/sample_images/image5.jpg" width="300" height="auto"> | <img src="https://raw.githubusercontent.com/muthuspark/text-detector/master/sample_images/outputs/image5.jpg" width="300" height="auto"> |
| <img src="https://raw.githubusercontent.com/muthuspark/text-detector/master/sample_images/image6.jpg" width="300" height="auto"> | <img src="https://raw.githubusercontent.com/muthuspark/text-detector/master/sample_images/outputs/image6.jpg" width="300" height="auto"> |

## Notebook
All my experiments are in this notebook also part of the project where I make changes to the algorithm and them move it to the detector file.
[Text Segmentation in Image.ipynb](https://github.com/muthuspark/text-detector/blob/master/notebooks/Text%20Segmentation%20in%20Image.ipynb)

## Accuracy
The accuracy depends a lot of the threshold parameters in the `utils.thresholds.py` file which may need tweaking for different kinds of datasets.

## References
B. Epshtein, E. Ofek and Y. Wexler, "Detecting text in natural scenes with stroke width transform," 2010 IEEE Computer Society Conference on Computer Vision and Pattern Recognition, San Francisco, CA, 2010, pp. 2963-2970.

Tran, Tuan Anh Pham et al. “Separation of Text and Non-text in Document Layout Analysis using a Recursive Filter.” TIIS 9 (2015): 4072-4091.

Chen, Huizhong, et al. "Robust Text Detection in Natural Images with Edge-Enhanced Maximally Stable Extremal Regions." Image Processing (ICIP), 2011 18th IEEE International Conference on. IEEE, 2011.