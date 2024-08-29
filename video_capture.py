import cv2 as cv
import numpy as np
import imutils 
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

    # creating contours for each mask

    cnts1 = cv.findContours(mask_blue_roi, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts1 = imutils.grab_contours(cnts1)

    cnts2 = cv.findContours(mask_green_roi, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)

    cnts3 = cv.findContours(mask_red1_roi, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts3 = imutils.grab_contours(cnts3)

    cnts4 = cv.findContours(mask_red2_roi, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts4 = imutils.grab_contours(cnts4)
    
    cnts5 = cv.findContours(mask_yellow_roi, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts5 = imutils.grab_contours(cnts5)

    cnts6 = cv.findContours(mask_orange_roi, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts6 = imutils.grab_contours(cnts6)

    cnts7 = cv.findContours(mask_white_roi, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts7 = imutils.grab_contours(cnts7)

    for c in cnts1:
        area1 = cv.contourArea(c)
        if area1 > 5000:
            cv.drawContours(frame, [c + np.array([x1, y1])], -1, (0,255,0), 3)

            M = cv.moments(c)

            cx = int(M["m10"]/ M["m00"])
            cy = int(M["m01"]/ M["m00"])

            cv.circle(frame, (cx + x1, cy + y1), 7, (255, 255, 255), -1)
            cv.putText(frame, "Blue", (cx + x1-20, cy + y1 -20), cv.FONT_HERSHEY_SIMPLEX,2.5, (255,255,255),3)

    for c in cnts2:
        area2 = cv.contourArea(c)
        if area2 > 5000:
            cv.drawContours(frame, [c + np.array([x1, y1])], -1, (0,255,0), 3)

            M = cv.moments(c)

            cx = int(M["m10"]/ M["m00"])
            cy = int(M["m01"]/ M["m00"])

            cv.circle(frame, (cx + x1, cy + y1), 7, (255,255,255), -1)
            cv.putText(frame, "Green", (cx + x1-20, cy + y1 -20), cv.FONT_HERSHEY_SIMPLEX,2.5, (255,255,255),3)

    for c in cnts3:
        area3 = cv.contourArea(c)
        if area3 > 5000:
            cv.drawContours(frame, [c + np.array([x1, y1])], -1, (0,255,0), 3)

            M = cv.moments(c)

            cx = int(M["m10"]/ M["m00"])
            cy = int(M["m01"]/ M["m00"])

            cv.circle(frame, (cx + x1, cy + y1), 7, (255,255,255), -1)
            cv.putText(frame, "Red", (cx + x1-20, cy + y1 -20), cv.FONT_HERSHEY_SIMPLEX,2.5, (255,255,255),3)

    for c in cnts4:
        area4 = cv.contourArea(c)
        if area4 > 5000:
            cv.drawContours(frame, [c + np.array([x1, y1])], -1, (0,255,0), 3)

            M = cv.moments(c)

            cx = int(M["m10"]/ M["m00"])
            cy = int(M["m01"]/ M["m00"])

            cv.circle(frame, (cx + x1, cy + y1), 7, (255,255,255), -1)
            cv.putText(frame, "Red", (cx + x1-20, cy + y1 -20), cv.FONT_HERSHEY_SIMPLEX,2.5, (255,255,255),3)

    for c in cnts5:
        area5 = cv.contourArea(c)
        if area5 > 5000:
            cv.drawContours(frame, [c + np.array([x1, y1])], -1, (0,255,0), 3)

            M = cv.moments(c)

            cx = int(M["m10"]/ M["m00"])
            cy = int(M["m01"]/ M["m00"])

            cv.circle(frame, (cx + x1, cy + y1), 7, (255,255,255), -1)
            cv.putText(frame, "Yellow", (cx + x1-20, cy + y1 -20), cv.FONT_HERSHEY_SIMPLEX,2.5, (255,255,255),3)

    for c in cnts6:
        area6 = cv.contourArea(c)
        if area6 > 5000:
            cv.drawContours(frame, [c + np.array([x1, y1])], -1, (0,255,0), 3)

            M = cv.moments(c)

            cx = int(M["m10"]/ M["m00"])
            cy = int(M["m01"]/ M["m00"])

            cv.circle(frame, (cx + x1, cy + y1), 7, (255,255,255), -1)
            cv.putText(frame, "Orange", (cx + x1-20, cy + y1 -20), cv.FONT_HERSHEY_SIMPLEX,2.5, (255,255,255),3)

    for c in cnts7:
        area7 = cv.contourArea(c)
        if area7 > 5000:
            cv.drawContours(frame, [c + np.array([x1, y1])], -1, (0,255,0), 3)

            M = cv.moments(c)

            cx = int(M["m10"]/ M["m00"])
            cy = int(M["m01"]/ M["m00"])

            cv.circle(frame, (cx + x1, cy + y1), 7, (255,255,255), -1)
            cv.putText(frame, "White", (cx + x1-20, cy + y1 -20), cv.FONT_HERSHEY_SIMPLEX,2.5, (255,255,255),3)
    

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