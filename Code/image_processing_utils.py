import cv2 as cv

def read_image(image_path):
    return cv.imread(image_path, cv.IMREAD_COLOR)

def preprocess_image(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.bitwise_not(gray)
    gray_blurred = cv.GaussianBlur(gray, (5, 5), 0)
    gray_blurred = cv.medianBlur(gray_blurred, 5)
    return gray_blurred

def adaptive_threshold(image):
    _, bw = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return cv.adaptiveThreshold(bw, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 15, -2)
