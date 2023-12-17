import cv2 as cv
import numpy as np

def extract_horizontal_lines(image, scale_factor=0.05, close_scale_factor=0.9, min_line_length_ratio=0.9):
    size = image.shape[1]

    line_size = int(size * scale_factor)
    structuring_element = cv.getStructuringElement(cv.MORPH_RECT, (line_size, 1))

    processed = cv.erode(image, structuring_element)
    processed = cv.dilate(processed, structuring_element)

    close_size = int(size * close_scale_factor)
    close_structure = cv.getStructuringElement(cv.MORPH_RECT, (close_size, 1))
    processed_closed = cv.morphologyEx(processed, cv.MORPH_CLOSE, close_structure)

    num_labels, labels, stats, _ = cv.connectedComponentsWithStats(processed_closed, connectivity=8, ltype=cv.CV_32S)
    min_length = min_line_length_ratio * size
    filtered_lines = np.zeros_like(processed_closed)
    
    
    for i in range(1, num_labels):
        if (stats[i, cv.CC_STAT_WIDTH]) >= min_length:
            component_mask = (labels == i).astype(np.uint8) * 255
            filtered_lines = cv.bitwise_or(filtered_lines, component_mask)

    return filtered_lines
