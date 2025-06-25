import cv2
import numpy as np

def nothing(x):
    pass

# Przetwarzanie wideo lub obrazu
camera_capture = True

img_path = 'test5.png'

# Plik wideo do testowania
video_path = 'test_video2.mp4'

if camera_capture:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    wait_time = int(1000 / fps)
else:
    img = cv2.imread(img_path)
    wait_time = 1

cv2.namedWindow('Image')
cv2.namedWindow('Detection')
cv2.createTrackbar('Top Cut', 'Image', 50, 200, nothing)
cv2.createTrackbar('Bottom Cut', 'Image', 44, 200, nothing)
cv2.createTrackbar('Top Threshold', 'Image', 255, 255, nothing)
cv2.createTrackbar('Bottom Threshold', 'Image', 32, 255, nothing)
cv2.createTrackbar('Detection Start', 'Image', 242, 250, nothing)
cv2.createTrackbar('Left Cut', 'Image', 723, 1400, nothing)
cv2.createTrackbar('Right Cut', 'Image', 191, 800, nothing)

while True:
    if camera_capture:
        ret, img = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    top_cut = 80
    bottom_cut = 136
    top_thresh = 255
    bottom_thresh = 50

    top_cut = cv2.getTrackbarPos('Top Cut', 'Image')
    bottom_cut = cv2.getTrackbarPos('Bottom Cut', 'Image')
    top_thresh = cv2.getTrackbarPos('Top Threshold', 'Image')
    bottom_thresh = cv2.getTrackbarPos('Bottom Threshold', 'Image')
    left_cut = cv2.getTrackbarPos('Left Cut', 'Image')
    right_cut = cv2.getTrackbarPos('Right Cut', 'Image')
    detection_start = cv2.getTrackbarPos('Detection Start', 'Image')

    vessel = img_gray.copy()
    w,h = img.shape[1], img.shape[0]
    vessel = vessel[top_cut:h-bottom_cut, 0:w]

    vessel_height, vessel_width = vessel.shape

    roi = vessel[0:h-detection_start, left_cut:vessel_width-right_cut]
    sobel_y = cv2.Sobel(roi, cv2.CV_64F, 0, 1, ksize=3)
    sobel_y = cv2.convertScaleAbs(sobel_y)
    _, edge_thresh = cv2.threshold(sobel_y, bottom_thresh, top_thresh, cv2.THRESH_BINARY)

    histogram = np.sum(edge_thresh, axis=1)
    line_y = np.argmax(histogram)

    fill = round((vessel_height - line_y) / vessel_height, 2)
    y_line_global =  line_y + top_cut
    print(f"{fill * 100:.1f}, {y_line_global}")

    cv2.line(img, (0, y_line_global), (img.shape[1], y_line_global), (0, 0, 255), 2)
    cv2.putText(img,
            f"{fill * 100:.0f}%",                  
            (40, max(y_line_global - 10, 20)),      
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,                            
            (0, 0, 255),
            2)
    cv2.imshow('Image', img)
    cv2.imshow('Detection', edge_thresh)

    cv2.waitKey(wait_time)

