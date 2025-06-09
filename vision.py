import cv2
import numpy as np

def nothing(x):
    pass

camera_capture = False

if camera_capture:
    cap=cv2.VideoCapture(0)
else:
    img = cv2.imread('water.jpg')

if img is None:
    print("Nie udało się załadować obrazu")
    exit()

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#img_gray = cv2.GaussianBlur(img_gray, (5, 5), 0)

cv2.namedWindow("Controls")
cv2.namedWindow("Mask")

cv2.createTrackbar("Threshold low limit", "Controls", 100, 255, nothing)
cv2.createTrackbar("Threshold high limit", "Controls", 255, 255, nothing)
cv2.createTrackbar("Bottom cut", "Controls", 40, 220, nothing)
cv2.createTrackbar("Top cut", "Controls", 5, 220, nothing)

while True:
    if camera_capture:
        ret, img = cap.read()
        if not ret:
            print("Nie udało się odczytać obrazu z kamery")
            break
    else:
        img = cv2.imread('water.jpg')

    thresh_val1 = cv2.getTrackbarPos("Threshold low limit", "Controls")
    thresh_val2 = cv2.getTrackbarPos("Threshold high limit", "Controls")
    top_cut = cv2.getTrackbarPos("Top cut", "Controls")
    bottom_cut = cv2.getTrackbarPos("Bottom cut", "Controls")
    
    img_canny = cv2.Canny(img_gray, thresh_val1, thresh_val2)
    #_, thresh = cv2.threshold(img_gray, thresh_val1, thresh_val2, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    glass_contour = max(contours, key=cv2.contourArea)
    #cv2.drawContours(img, contours, -1, (0,255,0), 4)

    x, y, w, h = cv2.boundingRect(glass_contour)

    mask = np.zeros_like(img_gray, dtype=np.uint8)
    cv2.drawContours(mask, contours, -1, 255, -1) 

    roi = cv2.bitwise_and(img_gray, img_gray, mask=mask)

    roi = roi[y+top_cut:y+h-bottom_cut, x:x+w]

    roi_height, roi_width = roi.shape

    sobel_y = cv2.Sobel(roi, cv2.CV_64F, 0, 1, ksize=3)
    sobel_y = cv2.convertScaleAbs(sobel_y)  
    _, thresh = cv2.threshold(sobel_y, 50, 255, cv2.THRESH_BINARY)
    histogram = np.sum(thresh, axis=1)
    line_y = np.argmax(histogram)
    
    # show results in roi (region of interest)
    cv2.line(thresh, (0, line_y), (img.shape[1], line_y), (0, 255, 0), 2)
    fill = round((roi_height - line_y)/roi_height,2)
    # show results in original image
    line_y = line_y + y + top_cut 
    cv2.line(img, (0, line_y), (img.shape[1], line_y), (0, 255, 0), 2)
    
    cv2.putText(img, f"Fill: {fill}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imshow("Mask", thresh)

    cv2.imshow("Controls", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break
    
cv2.destroyAllWindows()
