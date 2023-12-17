import cv2 as cv
import os

def split_image_at_lines(src, vertical_coords):
    # Check if there are at least 4 vertical lines to use indices 2, 3, and 4
    if len(vertical_coords) < 4:
        print("Not enough vertical lines detected to find the specified indices.")
        return None, None, None, None
    
    parts = []
    # Use the 2nd, 3rd, and 4th lines (indexing from 0)
    x_coord1 = vertical_coords[1]  # 2nd line
    x_coord2 = vertical_coords[2]  # 3rd line
    x_coord3 = vertical_coords[3]  # 4th line

    # Split the image into four parts
    parts.append(src[:, :x_coord1])
    parts.append(src[:, x_coord1:x_coord2])
    parts.append(src[:, x_coord2:x_coord3])
    parts.append(src[:, x_coord3:])

    return parts


def crop_image_between_horizontal_lines(src, horizontal_coords):
    # Check if there are enough horizontal lines
    if len(horizontal_coords) < 2:
        print("Not enough horizontal lines detected.")
        return None

    # Get the Y coordinates of the first and last horizontal lines
    first_line_y = horizontal_coords[0]
    last_line_y = horizontal_coords[-1]

    # Crop the image between these two lines
    cropped_image = src[first_line_y:last_line_y, :]

    return cropped_image

def save_image_segments(src, horizontal_coords, folder_path, base_file_name, start_number):
    # Check if there are enough horizontal lines
    if len(horizontal_coords) < 1:
        print("Not enough horizontal lines detected.")
        return start_number

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Keep track of the last number used
    last_number = start_number

    # Iterate through horizontal coordinates to create and save segments
    for i in range(len(horizontal_coords) - 1):
        # Define the start and end Y coordinates for the current segment
        start_y = horizontal_coords[i]
        end_y = horizontal_coords[i + 1]

        # Crop the segment from the source image
        segment = src[start_y:end_y, :]

        # Construct the file name with the original image name and current number
        segment_filename = os.path.join(folder_path, f'{base_file_name}_{last_number}.jpg')

        # Save the segment
        cv.imwrite(segment_filename, segment)

        print(f'Segment {last_number} saved as "{segment_filename}".')

        # Increment the last number for the next segment
        last_number += 1

    return last_number



