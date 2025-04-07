import cv2 as cv
import numpy as np
import imutils

ROI_WIDTH = 200
ROI_HEIGHT = 200

NUM_COLUMNS = 3
NUM_ROWS = 3

CELL_WIDTH = ROI_WIDTH // NUM_COLUMNS
CELL_HEIGHT = ROI_HEIGHT // NUM_ROWS

GRID_COLOR = (0, 255, 0)

COLOR_RANGE = {
        'Blue': (np.array([95, 100, 80]), np.array([125, 255, 255])),
        'Green': (np.array([50, 120, 100]), np.array([70, 255, 255])),
        'Orange': (np.array([11, 140, 120]), np.array([18, 255, 255])),
        'Red': (np.array([0, 150, 120]), np.array([8, 255, 255])),
        'Red2': (np.array([170, 150, 120]), np.array([180, 255, 255])),
        'Yellow': (np.array([20, 150, 180]), np.array([30, 255, 255])),
        'White': (np.array([0, 0, 200]), np.array([180, 40, 255]))
    }

COLOR_MAP = {
        'Red': (0, 0, 255),
        'Blue': (255, 0, 0),
        'Green': (0, 255, 0),
        'Orange': (0, 165, 255),
        'Yellow': (0, 255, 255),
        'White': (255, 255, 255),
        'Unknown': (50, 50, 50)
    }

COLOR_TO_FACE = {
    'White': 'U',
    'Green': 'F',
    'Red': 'R',
    'Red2': 'R',
    'Orange': 'L',
    'Blue': 'B',
    'Yellow': 'D',
}

REFERENCE_COLORS = {}

def quant_image(image, k):
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv.kmeans(Z, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    quantized_image = centers[labels.flatten()]
    quantized_image = quantized_image.reshape(image.shape)

    return quantized_image, centers

def get_best_color_match(hsv, color_ranges):
    best_match = "Unknown"
    min_distance = float('inf')

    for color, (lower, upper) in color_ranges.items():
        # Treat Red and Red2 as one color
        color_key = 'Red' if color in ['Red', 'Red2'] else color
        center = (np.mean([lower[0], upper[0]]), np.mean([lower[1], upper[1]]), np.mean([lower[2], upper[2]]))
        distance = np.linalg.norm(np.array(hsv) - np.array(center))

        if distance < min_distance:
            min_distance = distance
            best_match = color_key

    return best_match

def get_cube_string(detected_colors):
    res = ''
    for face in ['U', 'R', 'F', 'D', 'L', 'B']:
        converted_face = [[COLOR_TO_FACE.get(color, '?') for color in row] for row in detected_colors[face]]
        for row in converted_face:
            for face_label in row:
                res += face_label
    return res

def run_capture():
    faces = ['U', 'D', 'B', 'L', 'R', 'F']
    sides = ['White', 'Yellow', 'Green', 'Blue', 'Red', 'Orange']
    # Create video capture
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_AUTO_WB, 0)
    cap.set(cv.CAP_PROP_WB_TEMPERATURE, 4500)
    cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cap.set(cv.CAP_PROP_EXPOSURE, -6)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    detected_colors = {face: [['Unknown' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)] for face in faces}
    prompt_shown = False
    # Starts capture loop
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv.flip(frame, 1)
        frame_height, frame_width = frame.shape[:2]
        x_center = frame_width // 2
        y_center = frame_height // 2
        x1 = x_center - ROI_WIDTH // 2
        y1 = y_center - ROI_HEIGHT // 2
        x2 = x_center + ROI_WIDTH // 2
        y2 = y_center + ROI_HEIGHT // 2
        roi = frame[y1:y2, x1:x2]

        # If frame is read correctly, ret is true
        if not ret:
            print("Cannot receive frame. Exiting...")
            break

        frame_height, frame_width = frame.shape[:2]

        # Draw the ROI rectangle on the live feed
        cv.rectangle(frame, (x1, y1), (x2, y2), GRID_COLOR, 2)

        # Draw the 3x3 grid
        for row in range(1, NUM_ROWS):
            y_position = y1 + row * CELL_HEIGHT
            cv.line(frame, (x1, y_position), (x2, y_position), GRID_COLOR, 2) 

        for col in range(1, NUM_COLUMNS):
            x_position = x1 + col * CELL_WIDTH
            cv.line(frame, (x_position, y1), (x_position, y2), GRID_COLOR, 2)  

        cv.imshow("Live", frame)

        # Check if there are any remaining faces to scan
        if len(faces) == 0:
            return get_cube_string(detected_colors)

        # Take the first face 
        curr_face = faces[0]
        
        # Prompt user to scan the face
        if not prompt_shown:
            print(f"Scanning {curr_face}")
            print("Press C to capture frame or S to sample color.", flush=True)
            prompt_shown = True

        # Capture frame
        key = cv.waitKey(1)
        if key == ord('c'):
            print("Processing frame.", flush=True)
            frame_height, frame_width = frame.shape[:2]

            # Calculate position for ROI
            x_center = frame_width // 2
            y_center = frame_height // 2

            # Find corners for ROI
            x1 = x_center - ROI_WIDTH // 2
            y1 = y_center - ROI_HEIGHT // 2
            x2 = x_center + ROI_WIDTH // 2
            y2 = y_center + ROI_HEIGHT // 2

            # Create ROI
            # roi = frame[y1:y2, x1:x2]
            hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
            # Create mask of 0s for ROI
            combined_roi_mask = np.zeros((ROI_HEIGHT, ROI_WIDTH), dtype=np.uint8)

            # Compare cluster centers with COLOR_MAP
            for row in range(NUM_ROWS):
                for col in range(NUM_COLUMNS):

                    # Define cell boundary
                    cell_x1 = col * CELL_WIDTH
                    cell_y1 = row * CELL_HEIGHT
                    cell_x2 = (col + 1) * CELL_WIDTH
                    cell_y2 = (row + 1) * CELL_HEIGHT

                    # Extract cell from ROI
                    cell = roi[cell_y1:cell_y2, cell_x1:cell_x2]
                    hsv_cell = hsv_roi[cell_y1:cell_y2, cell_x1:cell_x2]

                    # Initialize masks
                    combined_cell_mask = np.zeros(hsv_cell.shape[:2], dtype=np.uint8)

                    # Create masks for each color
                    for color, (lower, upper) in COLOR_RANGE.items():
                        mask = cv.inRange(hsv_cell, lower, upper)
                        combined_cell_mask = cv.bitwise_or(combined_cell_mask, mask)

            # Update the combined mask for the ROI
            combined_roi_mask = combined_cell_mask

            # Draw rectangle around ROI
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Find contours in the cell
            cnts = cv.findContours(combined_cell_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # Draw contours and add text
            for row in range(NUM_ROWS):
                for col in range(NUM_COLUMNS):
                    cell_x1 = col * CELL_WIDTH
                    cell_y1 = row * CELL_HEIGHT
                    cell_x2 = (col + 1) * CELL_WIDTH
                    cell_y2 = (row + 1) * CELL_HEIGHT

                    # Extract cell from ROI
                    cell = roi[cell_y1:cell_y2, cell_x1:cell_x2]
                    mean_bgr = np.mean(cell.reshape(-1, 3), axis=0)

                    min_dist = float('inf')
                    closest_label = 'Unknown'
                    for label, ref in REFERENCE_COLORS.items():
                        dist = np.linalg.norm(mean_bgr - ref)
                        if dist < min_dist:
                            min_dist = dist
                            closest_label = label
                    detected_colors[curr_face][row][col] = closest_label

            # Apply the combined mask to the ROI
            result_roi = roi.copy()

            # Update the frame with the processed ROI
            frame[y1:y2, x1:x2] = roi

            # Draw rectangle around ROI
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.imshow("Masked", result_roi)

            # Ask for confirmation
            detected_colors[curr_face] = [row[::-1] for row in detected_colors[curr_face]]
            print(detected_colors[curr_face])
            print("Is this correct? Y/N", flush=True)
            key = cv.waitKey(0) 
            if key == ord("y"):
                print("Confirmed face. Removing from list...")
                removed_face = faces.pop(0)
                print(f"Removed face: {removed_face}")
                print(f"Faces remaining: {faces}")
                prompt_shown = False
                if len(faces) == 0:
                    return get_cube_string(detected_colors)

        elif key == ord('s'):
            center_cell = roi[CELL_HEIGHT:CELL_HEIGHT*2, CELL_WIDTH:CELL_WIDTH*2]
            mean_bgr = np.mean(center_cell.reshape(-1, 3), axis=0)
            label = input("Label this center color (e.g. Red, Green): ").capitalize()
            REFERENCE_COLORS[label] = mean_bgr
            if label in sides: 
                sides.remove(label)
            else:
                print('Side already scanned')
        
            print(sides)
            print(f"Stored {label} as {mean_bgr}")

        # Exit
        if key == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    run_capture()