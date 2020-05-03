import numpy as np
import time


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
    if (centroid_b2[0] - centroid_b1[0]) == 0:
        return True

    angle = (np.arctan(np.abs((centroid_b2[1] - centroid_b1[1]) / (centroid_b2[0] - centroid_b1[0]))) * 180) / np.pi
    # print(angle)
    if angle > 70:
        return True


def combine_boxes(box1, box2):
    minr = np.min([box1[0], box2[0]])
    minc = np.min([box1[1], box2[1]])
    maxr = np.max([box1[2], box2[2]])
    maxc = np.max([box1[3], box2[3]])
    return [minr, minc, maxr, maxc]


def group_the_bounding_boxes(bounding_boxes):
    stime = time.time()
    number_of_checks = 0
    box_groups = []
    dont_check_anymore = []
    for iindex, box1 in enumerate(bounding_boxes):
        if iindex in dont_check_anymore:
            continue

        group_size = 0
        bigger_box = box1

        for jindex, box2 in enumerate(bounding_boxes):
            if jindex in dont_check_anymore:
                continue

            if jindex == iindex:
                continue

            number_of_checks+=1

            if is_overlapping(bigger_box, box2) and is_almost_in_line(bigger_box, box2):
                bigger_box = combine_boxes(bigger_box, box2)
                dont_check_anymore.append(jindex)
                group_size += 1

        if group_size > 0:
            # check if this group overlaps any other
            # and combine it there otherwise make a new box.
            combined_with_existing_box = False
            for kindex, box3 in enumerate(box_groups):
                if is_overlapping(bigger_box, box3):
                    bigger_box = combine_boxes(bigger_box, box3)
                    box_groups[kindex] = bigger_box
                    combined_with_existing_box = True
                    break

            if not combined_with_existing_box:
                box_groups.append(bigger_box)

        else:
            dont_check_anymore.append(iindex)

    print("number_of_checks:", number_of_checks)
    print("time_taken:", str(time.time() - stime))
    return box_groups
