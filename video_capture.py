import cv2 as cv
import numpy as np
import rubiks_cube_class as rc

# Create instance
rubiks_cube = rc.RubiksCube()

# Create video capture
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Determine roi sizes
roi_width = 200
roi_height = 200

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly, ret is true
    if not ret:
        print("Cannot receive frame (stream end?). Exiting...")
        break

    frame_height, frame_width = frame.shape[:2]

    # calculate position for roi
    x_center = frame_width // 2
    y_center = frame_height // 2

    x1 = x_center - roi_width // 2
    y1 = y_center - roi_height // 2
    x2 = x_center + roi_width // 2
    y2 = y_center + roi_height // 2

    # extract roi
    roi = frame[y1:y2, x1:x2]

    # Convert frame to hsv
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

    # Define range of wanted colors in HSV
    lower_blue = np.array([100, 80, 0])
    upper_blue = np.array([140, 255, 255])

    lower_green = np.array([40, 70, 70])
    upper_green = np.array([80, 255, 255])

    lower_orange = np.array([0, 70, 50])
    upper_orange = np.array([10, 255, 255])

    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    lower_yellow = np.array([25, 100, 200])
    upper_yellow = np.array([40, 255, 255])

    lower_white = np.array([30, 0, 150])
    upper_white = np.array([90, 20, 255])
    

    # Threshold the HSV image to get only selected colors in the frame
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv.inRange(hsv, lower_green, upper_green)
    mask_red1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv.inRange(hsv, lower_red2, upper_red2)
    mask_yellow = cv.inRange(hsv, lower_yellow, upper_yellow)
    mask_orange = cv.inRange(hsv, lower_orange, upper_orange)
    mask_white = cv.inRange(hsv, lower_white, upper_white)

    # Combine masks for the entire frame
    mask = cv.bitwise_or(mask_blue, mask_green)
    mask = cv.bitwise_or(mask, mask_red1)
    mask = cv.bitwise_or(mask, mask_red2)
    mask = cv.bitwise_or(mask, mask_yellow)
    mask = cv.bitwise_or(mask, mask_orange)
    mask = cv.bitwise_or(mask, mask_white)

    # Result for the entire frame
    result = cv.bitwise_and(frame, frame, mask=mask)

    # Threshold the HSV image to get only selected colors in the ROI
    mask_blue_roi = cv.inRange(hsv_roi, lower_blue, upper_blue)
    mask_green_roi = cv.inRange(hsv_roi, lower_green, upper_green)
    mask_red1_roi = cv.inRange(hsv_roi, lower_red1, upper_red1)
    mask_red2_roi = cv.inRange(hsv_roi, lower_red2, upper_red2)
    mask_yellow_roi = cv.inRange(hsv_roi, lower_yellow, upper_yellow)
    mask_orange_roi = cv.inRange(hsv_roi, lower_orange, upper_orange)
    mask_white_roi = cv.inRange(hsv_roi, lower_white, upper_white)

    # Combine masks for the ROI
    mask_roi = cv.bitwise_or(mask_blue_roi, mask_green_roi)
    mask_roi = cv.bitwise_or(mask_roi, mask_red1_roi)
    mask_roi = cv.bitwise_or(mask_roi, mask_red2_roi)
    mask_roi = cv.bitwise_or(mask_roi, mask_yellow_roi)
    mask_roi = cv.bitwise_or(mask_roi, mask_orange_roi)
    mask_roi = cv.bitwise_or(mask_roi, mask_white_roi)

    # making roi have mask
    result_roi = cv.bitwise_and(roi, roi, mask=mask_roi)

    # roi after masking in orig frame 
    frame[y1:y2, x1:x2] = result_roi

    # Rectangle around roi in orig frame
    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # Displaying the video
    cv.imshow("Live", frame)
    cv.imshow("Masked", result)
    if cv.waitKey(1) == ord('q'):
        break

#when everything is done, release the capture
cap.release()
cv.destroyAllWindows()