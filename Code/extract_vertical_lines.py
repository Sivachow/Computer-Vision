import cv2 as cv
import numpy as np

def extract_vertical_lines(image, scale_factor=0.05, close_scale_factor=0.29, min_line_length_ratio=0.5, add_edge_columns=True, edge_column_thickness=8):
    rows = image.shape[0]

    line_size = int(rows * scale_factor)
    structuring_element = cv.getStructuringElement(cv.MORPH_RECT, (1, line_size))

    processed = cv.erode(image, structuring_element)
    processed = cv.dilate(processed, structuring_element)

    close_size = int(rows * close_scale_factor)
    close_structure = cv.getStructuringElement(cv.MORPH_RECT, (1, close_size))
    processed_closed = cv.morphologyEx(processed, cv.MORPH_CLOSE, close_structure)

    num_labels, labels, stats, _ = cv.connectedComponentsWithStats(processed_closed, connectivity=8, ltype=cv.CV_32S)
    min_length = min_line_length_ratio * rows
    filtered_vertical = np.zeros_like(processed_closed)

    for i in range(1, num_labels):
        if stats[i, cv.CC_STAT_HEIGHT] >= min_length:
            component_mask = (labels == i).astype(np.uint8) * 255
            filtered_vertical = cv.bitwise_or(filtered_vertical, component_mask)

    # Adding thicker columns on the leftmost and rightmost sides
    if add_edge_columns:
        filtered_vertical[:, 0:edge_column_thickness] = 255
        filtered_vertical[:, -edge_column_thickness:] = 255

    return filtered_vertical
