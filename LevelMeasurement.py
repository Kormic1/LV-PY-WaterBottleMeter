import cv2
import numpy as np

# Należy dobrać parametry w zależności od obrazu i naczynia
# ------------------
top_cut = 530       # obcięcie konturu od góry
bottom_cut = 1480   # obcięcie konturu od dołu
top_thresh = 255   # górny próg detekcji krawędzi
bottom_thresh = 50 # dolny próg detekcji krawędzi
# ------------------

def nothing(x):
    pass

def measure_level(use_glass_image):
    if not use_glass_image:
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        if not ret:
            return -1.0
    else:
        img = cv2.imread('water.jpg')
        
    if img is None:
        return -2.0
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 60])
    thresh = cv2.inRange(img_hsv, lower_black, upper_black)

    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return -3.0

    glass_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(glass_contour)

    mask = np.zeros_like(img_gray, dtype=np.uint8)
    cv2.drawContours(mask, [glass_contour], -1, 255, -1)

    roi = cv2.bitwise_and(img_gray, img_gray, mask=mask)

    roi = roi[y+top_cut:y+h-bottom_cut, x:x+w]

    if roi.size == 0:
        return -4.0

    roi_height, roi_width = roi.shape

    sobel_y = cv2.Sobel(roi, cv2.CV_64F, 0, 1, ksize=3)
    sobel_y = cv2.convertScaleAbs(sobel_y)
    _, edge_thresh = cv2.threshold(sobel_y, bottom_thresh, top_thresh, cv2.THRESH_BINARY)

    histogram = np.sum(edge_thresh, axis=1)
    line_y = np.argmax(histogram)

    fill = round((roi_height - line_y) / roi_height, 2)
    if fill < 0 or fill > 1:
        fill = -0.03
        
    return fill * 100