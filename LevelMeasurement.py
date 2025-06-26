import cv2
import numpy as np

def measure_level(use_glass_image, image_name):
    # Należy dobrać parametry w zależności od obrazu i naczynia
    # -----------------------
    top_cut = 50            # obcięcie konturu od góry
    bottom_cut = 44         # obcięcie konturu od dołu
    top_thresh = 255        # górny próg detekcji krawędzi
    bottom_thresh = 32      # dolny próg detekcji krawędzi
    left_cut = 723          # obcięcie obrazu od lewej
    right_cut = 191         # obcięcie obrazu od prawej
    detection_start = 242   # dodatkowe obcięcie od dołu obrazu, aby uniknąć detekcji dna naczynia
    # -----------------------
    if not use_glass_image:
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        if not ret:
            return (-1.0, 0)
    else:
        img = cv2.imread(image_name)
        
    if img is None:
        return (-2.0, 0)
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
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

    fill = round((vessel_height - line_y) / vessel_height, 2) * 100
    y_line_global = line_y + top_cut
    
    return (fill, y_line_global)