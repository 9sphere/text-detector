import numpy as np
from scipy.ndimage.morphology import distance_transform_edt
from skimage.color import rgb2gray
from skimage.filters import threshold_sauvola
from skimage.io import imread
from skimage.measure import label, regionprops

from utils.bbox import group_the_bounding_boxes
from utils.exceptions import InputError
from utils.thresholds import *


def detect_text_regions_from_image_file(img_file, white_text=False):
    return detect_text_regions(imread(img_file), white_text)


def __adaptive_threshold(img_array, white_text=False):
    window_size = 9
    thresh_sauvola = threshold_sauvola(img_array, window_size=window_size)
    binary_img = img_array > thresh_sauvola if white_text else img_array < thresh_sauvola
    return binary_img


def detect_text_regions(img_array, white_text=False):
    if len(img_array.shape) != 3 and len(img_array.shape) != 2:
        raise InputError(img_array, 'The image must either be RGB or Grayscale')

    original_image = np.copy(img_array)

    # convert to grayscale if colored
    if len(img_array.shape) == 3:
        img_array = rgb2gray(img_array)

    # binarize the image using adaptive algorithm threshold_sauvola
    binary_img = __adaptive_threshold(img_array, white_text)

    # find connected components in the image.
    label_image = label(binary_img)
    region_props = regionprops(label_image)

    # find possible text components
    bounding_boxes = []
    # ignore too small areas
    for index, region in enumerate(region_props):
        minr, minc, maxr, maxc = region.bbox
        height = maxr - minr
        width = maxc - minc

        aspect_ratio = width / height

        should_clean = region.area < min_region_area
        should_clean = should_clean or aspect_ratio < min_aspect_ratio or aspect_ratio > max_aspect_ratio
        should_clean = should_clean or region.eccentricity > max_eccentricity
        should_clean = should_clean or region.solidity < min_solidity
        should_clean = should_clean or region.extent < min_region_extent or region.extent > max_region_extent
        should_clean = should_clean or region.euler_number < min_euler_number

        # find the stroke width uniformity of the region
        stroke_width_values = distance_transform_edt(region.image)
        stroke_width_metric = np.std(stroke_width_values) / np.mean(stroke_width_values)
        should_clean = should_clean or stroke_width_metric < min_stroke_width_metric

        if not should_clean:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            minr = int((1 - expansion_amount) * minr)
            minc = int((1 - expansion_amount) * minc)
            maxr = int((1 + expansion_amount) * maxr)
            maxc = int((1 + expansion_amount) * maxc)

            bounding_boxes.append([minr, minc, maxr, maxc])

    # now its time to merge the overlappiong bouding boxes.

    # step 1: sort the bounding_boxes by their distance from Y Axis
    bounding_boxes = np.array(bounding_boxes)
    bounding_boxes = bounding_boxes[bounding_boxes[:, 1].argsort()]

    text_regions = group_the_bounding_boxes(bounding_boxes)
    return text_regions
