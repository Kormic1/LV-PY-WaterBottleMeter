import cv2
import numpy as np

def nothing(x):
	pass

glass_top_px = 45
glass_bottom_px = 310

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

    img_canny = cv2.Canny(img_gray, 100, 255)
    #_, thresh = cv2.threshold(img_gray, thresh_val1, thresh_val2, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    glass_contour = max(contours, key=cv2.contourArea)
    #cv2.drawContours(img, contours, -1, (0,255,0), 4)

    x, y, w, h = cv2.boundingRect(glass_contour)

    mask = np.zeros_like(img_gray, dtype=np.uint8)
    cv2.drawContours(mask, contours, -1, 255, -1) 

    roi = cv2.bitwise_and(img_gray, img_gray, mask=mask)

    roi = roi[y+round(0.05*h):y+h, x:x+w]

    sobel_y = cv2.Sobel(roi, cv2.CV_64F, 0, 1, ksize=3)  # tylko zmiany w pionie (czyli linie poziome)
    sobel_y = cv2.convertScaleAbs(sobel_y)  
    _, thresh = cv2.threshold(sobel_y, 50, 255, cv2.THRESH_BINARY)
    histogram = np.sum(thresh, axis=1)
    line_y = np.argmax(histogram) + y + round(0.05 * h)
    raw_fill_level = (line_y - glass_top_px) / (glass_bottom_px - glass_top_px)
    fill_percentage = 100 * (1 - raw_fill_level)
    
    return fill_percentage