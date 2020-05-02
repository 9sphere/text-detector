import numpy as np


# minr, minc, maxr, maxc
# https://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other
def is_overlapping(box1, box2):
    #     if (RectA.minc < RectB.maxc && RectA.maxc > RectB.minc &&
    #      RectA.minr > RectB.maxr && RectA.maxr < RectB.minr )
    if box1[1] < box2[3] and box1[3] > box2[1] and box1[0] < box2[2] and box1[2] > box2[0]:
        return True
    return False


def is_almost_in_line(box1, box2):
    centroid_b1 = [int((box1[0] + box1[2]) / 2), int((box1[1] + box1[3]) / 2)]
    centroid_b2 = [int((box2[0] + box2[2]) / 2), int((box2[1] + box2[3]) / 2)]
    if centroid_b2[0] - centroid_b1[0] == 0:
        return True

    angle = (np.arctan(np.abs((centroid_b2[1] - centroid_b1[1]) / (centroid_b2[0] - centroid_b1[0]))) * 180) / np.pi
    if angle > 70:
        return True

    return False


def combine_boxes(box1, box2):
    minr = np.min([box1[0], box2[0]])
    minc = np.min([box1[1], box2[1]])
    maxr = np.max([box1[2], box2[2]])
    maxc = np.max([box1[3], box2[3]])
    return [minr, minc, maxr, maxc]


def group_the_bounding_boxes(bounding_boxes):
    grouped = []
    box_groups = []
    for iindex, box1 in enumerate(bounding_boxes):
        if iindex in grouped:
            continue

        bigger_box = box1
        group_size = 0
        for jindex, box2 in enumerate(bounding_boxes):
            if jindex in grouped:
                continue

            if iindex != jindex and is_overlapping(bigger_box, box2) and is_almost_in_line(bigger_box,
                                                                                           box2):
                bigger_box = combine_boxes(bigger_box, box2)

                grouped.append(iindex)  # gets added multiple times, still better than checking everytime.source
                grouped.append(jindex)
                group_size += 1

        if group_size > 1:
            box_groups.append(bigger_box)

    return box_groups
