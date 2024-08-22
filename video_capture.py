import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    #capture frame-by-frame
    ret, frame = cap.read()

    #if frame is read correctly, ret is true
    if not ret:
        print("Cannot receive frame (stream end?). Exiting...")
        break

    # converting to color format
    colored = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    # external processing in RGB
    colored = cv.cvtColor(colored, cv.COLOR_RGB2BGR)
    # displaying the video
    cv.imshow("Live", colored)
    if cv.waitKey(1) == ord('q'):
        break

#when everything is done, release the capture
cap.release()
cv.destroyAllWindows()