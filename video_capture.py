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

# Determine ROI sizes
roi_width = 200
roi_height = 200

# Determine cell size
num_columns = 3
num_rows = 3
cell_width = roi_width // num_columns
cell_height = roi_height // num_rows

# Define color ranges in HSV
color_ranges = {
    'Blue': (np.array([100, 80, 0]), np.array([140, 255, 255])),
    'Green': (np.array([40, 70, 70]), np.array([80, 255, 255])),
    'Orange': (np.array([0, 70, 50]), np.array([10, 255, 255])),
    'Red': (np.array([0, 50, 50]), np.array([10, 255, 255])),
    'Red2': (np.array([170, 50, 50]), np.array([180, 255, 255])),
    'Yellow': (np.array([25, 100, 200]), np.array([40, 255, 255])),
    'White': (np.array([30, 0, 150]), np.array([90, 20, 255]))
}

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly, ret is true
    if not ret:
        print("Cannot receive frame (stream end?). Exiting...")
        break

    frame_height, frame_width = frame.shape[:2]

    # Calculate position for ROI
    x_center = frame_width // 2
    y_center = frame_height // 2

    x1 = x_center - roi_width // 2
    y1 = y_center - roi_height // 2
    x2 = x_center + roi_width // 2
    y2 = y_center + roi_height // 2

    # Extract ROI
    roi = frame[y1:y2, x1:x2]

    # Convert frame to HSV
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

    # Initialize a mask for the entire ROI
    combined_roi_mask = np.zeros((roi_height, roi_width), dtype=np.uint8)

    # Loop through each cell in the 3x3 grid
    for row in range(num_rows):
        for col in range(num_columns):
            # Define cell boundaries
            cell_x1 = col * cell_width
            cell_y1 = row * cell_height
            cell_x2 = (col + 1) * cell_width
            cell_y2 = (row + 1) * cell_height

            # Extract cell from ROI
            cell = roi[cell_y1:cell_y2, cell_x1:cell_x2]
            hsv_cell = hsv_roi[cell_y1:cell_y2, cell_x1:cell_x2]

            # Initialize masks
            combined_cell_mask = np.zeros(hsv_cell.shape[:2], dtype=np.uint8)

            # Create masks for each color
            for color, (lower, upper) in color_ranges.items():
                mask = cv.inRange(hsv_cell, lower, upper)
                combined_cell_mask = cv.bitwise_or(combined_cell_mask, mask)

            # Update the combined mask for the ROI
            combined_roi_mask[cell_y1:cell_y2, cell_x1:cell_x2] = combined_cell_mask

            # Find contours in the cell
            cnts = cv.findContours(combined_cell_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # Draw contours and add text
            for c in cnts:
                area = cv.contourArea(c)
                if area > 500:
                    cv.drawContours(roi, [c + np.array([cell_x1, cell_y1])], -1, (0, 255, 0), 2)
                    M = cv.moments(c)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])

                        # Determine color
                        color_detected = "Unknown"
                        for color, (lower, upper) in color_ranges.items():
                            if cv.inRange(np.array([[hsv_cell[cy, cx]]]), lower, upper).any():
                                color_detected = color
                                break

                        # Draw centroid and text
                        cv.circle(roi, (cx + cell_x1, cy + cell_y1), 7, (255, 255, 255), -1)
                        cv.putText(roi, color_detected, (cx + cell_x1 - 20, cy + cell_y1 - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Apply the combined mask to the ROI
    result_roi = cv.bitwise_and(roi, roi, mask=combined_roi_mask)

    # Update the frame with the processed ROI
    frame[y1:y2, x1:x2] = roi

    # Draw rectangle around ROI
    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the video
    cv.imshow("Live", frame)
    cv.imshow("Masked", result_roi)
    if cv.waitKey(1) == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv.destroyAllWindows()