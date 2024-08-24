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

    #convert frame to hsv
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    #define range of wanted color in HSV
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    
    upper_green = np.array([40, 50, 50])
    lower_green = np.array([80, 255, 255])

    lower_red = np.array([0, 150, 50])
    upper_red = np.array([10, 255, 255])

    #threshold the HSV image - blue -> white
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv.inRange(hsv, lower_green, upper_green)
    mask_red = cv.inRange(hsv, lower_red, upper_red)

    #combine masks
    mask = cv.bitwise_or(mask_blue, mask_green)
    mask = cv.bitwise_or(mask, mask_red)


    #any white pixels on mask, sum will be > 0
    # hasBlue = np.sum(mask)
    # if hasBlue > 0: 
    #     print("blue detected")

    #result 
    result = cv.bitwise_and(frame, frame, mask=mask)


    # converting to color format
    colored = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    # external processing in RGB
    colored = cv.cvtColor(colored, cv.COLOR_RGB2BGR)
    # displaying the video
    cv.imshow("Live", colored)
    cv.imshow("Blue only", result)
    if cv.waitKey(1) == ord('q'):
        break

#when everything is done, release the capture
cap.release()
cv.destroyAllWindows()