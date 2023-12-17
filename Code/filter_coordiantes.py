import numpy as np
import cv2 as cv

def extract_line_coords(filtered_lines, axis, min_gap):
    coords = np.where(np.max(filtered_lines, axis=axis) == 255)[0]

    # Group lines and select the middle line in each group
    filtered_coords = []
    start_index = 0  # Start index of a group of lines

    for i in range(1, len(coords)):
        if coords[i] - coords[i - 1] > min_gap:
            # If the gap is larger than min_gap, process the previous group
            middle_index = start_index + (i - start_index) // 2
            filtered_coords.append(coords[middle_index])
            start_index = i  # Start a new group

    # Process the last group of lines
    if start_index < len(coords):
        middle_index = start_index + (len(coords) - start_index) // 2
        filtered_coords.append(coords[middle_index])

    return sorted(filtered_coords)

def draw_lines(src, horizontal_coords, vertical_coords):
    # Draw horizontal lines
    for y in horizontal_coords:
        cv.line(src, (0, y), (src.shape[1], y), (255, 0, 0), 3) 

    # Draw vertical lines
    for x in vertical_coords:
        cv.line(src, (x, 0), (x, src.shape[0]), (0, 0, 255), 3)  

    return src

