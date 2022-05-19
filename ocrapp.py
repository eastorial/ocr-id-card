from imutils.perspective import four_point_transform
import easyocr
import math
import cv2
from difflib import SequenceMatcher


def detect_v2(img_path):

    # Load image, grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Find contours and sort for largest contour
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    displayCnt = None

    for c in cnts:
        # Perform contour approximation
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            displayCnt = approx
            break

    # Obtain birds' eye view of image
    warped = four_point_transform(image, displayCnt.reshape(4, 2))
    return warped
    # cv2.imshow("thresh", thresh)
    # cv2.imshow("warped", warped)
    # cv2.imshow("image", image)
    # cv2.waitKey()


def detect(img_path):
    # Load iamge, grayscale, adaptive threshold
    image = cv2.imread(img_path)
    result = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 51, 9)

    # Fill rectangular contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (255, 255, 255), -1)

    # Morph open
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)

    # Draw rectangles
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)

    crop_img = image[y: y + h, x: x + w]
    return crop_img


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# crop_field(reader, img, value[0][0][1], value[0][2][1], value[0][0][0], value[0][2][0], 125, 255)[0].upper()


def crop_field(reader, img, x_min, x_max, y_min, y_max, thresh, maxval):
    crop_img = img[int(x_min): int(x_max), int(y_min): int(y_max)]

    gray_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    ret, filtered_img = cv2.threshold(
        gray_img, thresh, maxval, cv2.THRESH_BINARY)
    blurred_img = cv2.GaussianBlur(filtered_img, (0, 0), 0.5)

#   cv2.imshow('img_', filtered_img)
#   cv2.imshow('img', blurred_img)
#   cv2.waitKey(0)
#   cv2.destroyAllWindows()

    return reader.readtext(blurred_img, paragraph=True, detail=0)


def get_count_digits(number: int):

    if number == 0:
        return 1

    number = abs(number)

    if number <= 999999999999997:
        return math.floor(math.log10(number)) + 1

    count = 0
    while number:
        count += 1
        number //= 10
    return count
