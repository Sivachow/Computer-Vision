import os
import cv2 as cv
import numpy as np
from image_processing_utils import read_image, preprocess_image, adaptive_threshold
from extract_horizontal_lines import extract_horizontal_lines
from extract_vertical_lines import extract_vertical_lines
from filter_coordiantes import extract_line_coords
from split_images import split_image_at_lines, save_image_segments

def image_already_processed(folder_path, image_name):
    # Check if any segment of this image has already been processed
    prefix = os.path.splitext(image_name)[0]
    return any(fname.startswith(prefix) for fname in os.listdir(folder_path))


def draw_lines(image, vertical_coords, horizontal_coords):
    # Draw vertical lines
    for x in vertical_coords:
        cv.line(image, (x, 0), (x, image.shape[0]), (255, 0, 0), 2)  # Red lines for vertical
    # Draw horizontal lines
    for y in horizontal_coords:
        cv.line(image, (0, y), (image.shape[1], y), (0, 255, 0), 2)  # Green lines for horizontal
    return image

def confirm_or_modify_lines(image, vertical_coords, horizontal_coords):
    while True:
        img_with_lines = draw_lines(image.copy(), vertical_coords, horizontal_coords)
        cv.imshow('Line Confirmation', img_with_lines)
        print("Press 'y' to confirm, 'n' to skip, or 'd' to delete the top horizontal line.")
        key = cv.waitKey(0)

        if key == ord('y'):
            cv.destroyAllWindows()
            return horizontal_coords, True
        elif key == ord('n'):
            cv.destroyAllWindows()
            return None, False
        elif key == ord('d') and horizontal_coords:
            horizontal_coords.pop(0)  # Remove the top horizontal line

input_folder = '../Scoresheets/'
output_folder = '../TestImages/'
min_gap = 20

for image_name in os.listdir(input_folder):
    if image_already_processed(output_folder, image_name):
        print(f"Skipping already processed image: {image_name}")
        continue
    src = read_image(os.path.join(input_folder, image_name))
    gray_blurred = preprocess_image(src)
    bw = adaptive_threshold(gray_blurred)

    # Detect vertical and horizontal lines
    filtered_vertical = extract_vertical_lines(bw)
    vertical_coords = extract_line_coords(filtered_vertical, axis=0, min_gap=min_gap)
    filtered_horizontal = extract_horizontal_lines(bw)
    horizontal_coords = extract_line_coords(filtered_horizontal, axis=1, min_gap=min_gap)

    # Basic check: Ensure exactly 5 vertical lines are detected
    if len(vertical_coords) != 5:
        print(f"Expected 5 vertical lines, but found {len(vertical_coords)} in {image_name}. Skipping.")
        continue

    # Confirm or modify horizontal lines
    confirmed_horizontal, confirmed = confirm_or_modify_lines(src, vertical_coords, horizontal_coords)
    if not confirmed:
        print(f"Lines in {image_name} not confirmed. Skipping.")
        continue

    # Split and save segments
    base_file_name = os.path.splitext(image_name)[0]
    parts = split_image_at_lines(src, vertical_coords)
    last_index = 1
    for part in parts:
        last_index = save_image_segments(part, confirmed_horizontal, output_folder, base_file_name, last_index)


# import numpy as np
# from image_processing_utils import read_image, preprocess_image, adaptive_threshold
# from extract_horizontal_lines import extract_horizontal_lines  # For horizontal lines
# from extract_vertical_lines import extract_vertical_lines  # For vertical lines
# from filter_coordiantes import extract_line_coords
# from split_images import split_image_at_lines, save_image_segments # For vertical lines

# import cv2 as cv

# min_gap = 20
# src = read_image('../ScoreSheets/1.jpg')
# gray_blurred = preprocess_image(src)
# bw = adaptive_threshold(gray_blurred)

# # Vertical
# filtered_vertical = extract_vertical_lines(bw)
# vertical_coords = extract_line_coords(filtered_vertical, axis=0, min_gap=min_gap)

# parts = split_image_at_lines(src, vertical_coords)

# filtered_horizontal = extract_horizontal_lines(bw)

# horizontal_coords = extract_line_coords(filtered_horizontal, axis=1, min_gap=min_gap)

# folder_path = './TestImages/'  # Update this to your desired path

# # Save image segments
# whilte_last = save_image_segments(parts[0], horizontal_coords, folder_path + 'White', 'White', 1)
# black_last = save_image_segments(parts[1], horizontal_coords, folder_path + 'Black', 'Black', 1)
# save_image_segments(parts[2], horizontal_coords, folder_path + 'White', 'White', whilte_last + 1)
# save_image_segments(parts[3], horizontal_coords, folder_path + 'Black', 'Black', black_last + 1)