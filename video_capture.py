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

    #define range of wanted colors in HSV
    #x
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    #x
    lower_green = np.array([40, 70, 70])
    upper_green = np.array([80, 255, 255])
    #x
    lower_orange = np.array([0, 70, 50])
    upper_orange = np.array([10, 255, 255])

    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    lower_yellow = np.array([25, 100, 200])
    upper_yellow = np.array([40, 255, 255])

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([90, 20, 255])

    #threshold the HSV image
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv.inRange(hsv, lower_green, upper_green)
    mask_red1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv.inRange(hsv, lower_red2, upper_red2)
    mask_yellow = cv.inRange(hsv, lower_yellow, upper_yellow)
    mask_orange = cv.inRange(hsv, lower_orange, upper_orange)
    mask_white = cv.inRange(hsv, lower_white, upper_white)

    #combine masks
    mask = cv.bitwise_or(mask_blue, mask_green)
    mask = cv.bitwise_or(mask, mask_red2)
    mask = cv.bitwise_or(mask, mask_red1)
    mask = cv.bitwise_or(mask, mask_yellow)
    mask = cv.bitwise_or(mask, mask_orange)
    mask = cv.bitwise_or(mask, mask_white)



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

    #processing colors
    # input("What face are you displaying?")
    # rubiks_face = []
    # for i in range(3):
    #     row = []
    #     for j in range(3):
    #         #extract range of interest
    #         roi = 



    # displaying the video
    cv.imshow("Live", colored)
    cv.imshow("Blue only", result)
    if cv.waitKey(1) == ord('q'):
        break

#when everything is done, release the capture
cap.release()
cv.destroyAllWindows()