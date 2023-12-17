# Computer-Vision

This project is a computer vision application that processes images from the `Scoresheets` folder and segments them into the `TestImages` folder. It also provides a GUI for labeling these segments.

## Usage

This project is composed of two main parts:

1. **Image Processing**: This part can be run using the `main.py` script. This script picks each image from the `Scoresheets` folder, processes it if it hasn't been processed already, and puts the segments into the `TestImages` folder. To run this part, use the following command:

```sh
python main.py
```

2. **GUI for Labeling**: This part can be run using the `gui.py` script. This script provides an interface for labeling the segments in the `TestImages` folder and stores them in the `labels.csv` file. To run this part, use the following command:

```sh
python gui.py
```

## Requirements

This project requires the following Python libraries:

- numpy
- opencv-python
- Pillow

You can install these requirements using pip