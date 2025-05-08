import cv2
import numpy as np

def nothing(x):
    pass

camera_capture = False

if camera_capture:
    cap=cv2.VideoCapture(0)
else:
    img = cv2.imread('LV-PY-WaterBottleMeter\water.jpg')

if img is None:
    print("Nie udało się załadować obrazu")
    exit()

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#img_gray = cv2.GaussianBlur(img_gray, (5, 5), 0)

cv2.namedWindow("Controls")
cv2.namedWindow("Mask")

cv2.createTrackbar("Threshold low limit", "Controls", 0, 255, nothing)
cv2.createTrackbar("Threshold high limit", "Controls", 0, 255, nothing)

while True:
    if camera_capture:
        ret, img = cap.read()
        if not ret:
            print("Nie udało się odczytać obrazu z kamery")
            break
    else:
        img = cv2.imread('LV-PY-WaterBottleMeter\water.jpg')

    thresh_val1 = cv2.getTrackbarPos("Threshold low limit", "Controls")
    thresh_val2 = cv2.getTrackbarPos("Threshold high limit", "Controls")
    
    img_canny = cv2.Canny(img_gray, thresh_val1, thresh_val2)
    #_, thresh = cv2.threshold(img_gray, thresh_val1, thresh_val2, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    glass_contour = max(contours, key=cv2.contourArea)
    cv2.drawContours(img, contours, -1, (0,255,0), 4)

    cv2.imshow("Controls", img)

    x, y, w, h = cv2.boundingRect(glass_contour)

    mask = np.zeros_like(img_gray, dtype=np.uint8)
    cv2.drawContours(mask, contours, -1, 255, -1) 

    roi = cv2.bitwise_and(img_gray, img_gray, mask=mask)

    roi = roi[y:y+h, x:x+w]

    sobel_y = cv2.Sobel(roi, cv2.CV_64F, 0, 1, ksize=3)  # tylko zmiany w pionie (czyli linie poziome)
    sobel_y = cv2.convertScaleAbs(sobel_y)  

    cv2.imshow("Mask", sobel_y)

    if cv2.waitKey(1) & 0xFF == 27:
        break
    
cv2.destroyAllWindows()
