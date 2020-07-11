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
    """
    Sauvola binarization method is well suited for ill illuminated or stained documents.

    :param img_array: image in grayscale format.
    :param white_text: set this to True if the text in your image is white.
    :return: Binary image after thresholding with True for all white looking pixels.
    """
    thresh_sauvola = threshold_sauvola(img_array, window_size=thresh_sauvola_window_size)
    binary_img = img_array > thresh_sauvola if white_text else img_array < thresh_sauvola
    return binary_img


def detect_text_regions(img_array, white_text=False):
    if len(img_array.shape) != 3 and len(img_array.shape) != 2:
        raise InputError(img_array, 'The image must either be RGB or Grayscale')

    # convert to grayscale if colored
    if len(img_array.shape) == 3:
        img_array = rgb2gray(img_array)

    # binarize the image using adaptive algorithm threshold_sauvola
    binary_img = __adaptive_threshold(img_array, white_text)

    # find connected components in the image.
    label_image = label(binary_img)
    region_props = regionprops(label_image)

    img_height, img_width = binary_img.shape

    # find possible text components
    bounding_boxes = []
    print("connected components found:", len(region_props))
    # ignore too small areas
    for index, region in enumerate(region_props):
        minr, minc, maxr, maxc = region.bbox
        height = maxr - minr
        width = maxc - minc

        aspect_ratio = width / height

        should_clean = region.area < (15 * (img_height * img_width / (600**2)))
        should_clean = should_clean or region.area > (img_height * img_width / 5)
        should_clean = should_clean or aspect_ratio < min_aspect_ratio or aspect_ratio > max_aspect_ratio
        should_clean = should_clean or region.eccentricity > max_eccentricity
        should_clean = should_clean or region.solidity < min_solidity
        should_clean = should_clean or region.extent < min_region_extent or region.extent > max_region_extent
        #     should_clean = should_clean or region.euler_number < -4

        strokeWidthValues = distance_transform_edt(region.image)
        strokeWidthMetric = np.std(strokeWidthValues) / np.mean(strokeWidthValues)
        should_clean = should_clean or strokeWidthMetric < 0.4

        if not should_clean:
            expansionAmountY = 0.02
            expansionAmountX = 0.03
            minr, minc, maxr, maxc = region.bbox

            minr = np.floor((1 - expansionAmountY) * minr)
            minc = np.floor((1 - expansionAmountX) * minc)
            maxr = np.ceil((1 + expansionAmountY) * maxr)
            maxc = np.ceil((1 + expansionAmountX) * maxc)

            bounding_boxes.append([minr, minc, maxr, maxc])

    print("bounding_boxes:", len(bounding_boxes))
    # now its time to merge the overlappiong bouding boxes.

    text_regions = group_the_bounding_boxes(bounding_boxes)
    return text_regions
