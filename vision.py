import cv2
import numpy as np

def nothing(x):
    pass

cam = cv2.VideoCapture(0)
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

cv2.namedWindow("Controls")
cv2.resizeWindow("Controls", frame_width, frame_height)

cv2.createTrackbar("Threshold", "Controls", 0, 255, nothing)
cv2.createTrackbar("Blur", "Controls", 0, 255, nothing)

while True:
    thresh_val1 = cv2.getTrackbarPos("Threshold", "Controls")
    thresh_val2 = cv2.getTrackbarPos("Blur", "Controls")

    ret, frame = cam.read()

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_canny = cv2.Canny(frame_gray,thresh_val1, thresh_val2)
    cv2.imshow('Controls', frame_canny)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()