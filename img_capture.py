import cv2 as cv
import numpy as np
import base64

ROI_WIDTH = 200
ROI_HEIGHT = 200

NUM_COLUMNS = 3
NUM_ROWS = 3

CELL_WIDTH = ROI_WIDTH // NUM_COLUMNS
CELL_HEIGHT = ROI_HEIGHT // NUM_ROWS

GRID_COLOR = (0, 255, 0)

COLOR_RANGE = {
    'Red':    (np.array([0, 150, 150]), np.array([9, 255, 255])),
    'Red2':   (np.array([170, 150, 150]), np.array([180, 255, 255])),
    'Green':  (np.array([50, 100, 50]), np.array([85, 255, 255])),
    'Yellow': (np.array([25, 120, 150]), np.array([40, 255, 255])),
    'Orange': (np.array([8, 140, 140]), np.array([22, 255, 255])),
    'Blue':   (np.array([100, 150, 50]), np.array([130, 255, 255])),
    'White':  (np.array([0, 0, 200]), np.array([180, 40, 255]))
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

def quant_image(image, k):
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv.kmeans(Z, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    quantized_image = centers[labels.flatten()]
    quantized_image = quantized_image.reshape(image.shape)

    return quantized_image, centers

def scan_center_cell(base64_str):
    image_data = base64.b64decode(base64_str)
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)

    height, width = img.shape[:2]
    x_center, y_center = width // 2, height // 2
    x1 = x_center - ROI_WIDTH // 2
    y1 = y_center - ROI_HEIGHT // 2
    x2 = x1 + ROI_WIDTH
    y2 = y1 + ROI_HEIGHT
    roi = img[y1:y2, x1:x2]

    center_cell = roi[CELL_HEIGHT:CELL_HEIGHT*2, CELL_WIDTH:CELL_WIDTH*2]
    buffer = 5
    center_cell = center_cell[buffer:-buffer, buffer:-buffer]

    center_cell = cv.GaussianBlur(center_cell, (5, 5), 0)
    hsv_center = cv.cvtColor(center_cell, cv.COLOR_BGR2HSV)

    h, s, v = cv.split(hsv_center)
    s = np.clip(s.astype(np.float32) * 2, 0, 255).astype(np.uint8)
    v = np.clip(v.astype(np.float32) * 2, 0, 255).astype(np.uint8)
    hsv_center = cv.merge([h, s, v])

    ch, cw = hsv_center.shape[:2]
    cropped = hsv_center[5:ch-5, 5:cw-5]
    mask = (cropped[...,1] > 80) & (cropped[...,2] > 80)
    filtered = cropped[mask]

    if filtered.size > 0:
        mean_hsv = np.mean(filtered, axis=0).astype(np.uint8)
    else:
        mean_hsv = np.mean(cropped.reshape(-1, 3), axis=0).astype(np.uint8)

    hsv_for_bgr = np.uint8([[mean_hsv]])
    mean_bgr = cv.cvtColor(hsv_for_bgr, cv.COLOR_HSV2BGR)[0][0].tolist()

    return mean_hsv, mean_bgr

def analyze_image(base64_str, reference_colors=None):
    image_data = base64.b64decode(base64_str)
    nparr = np.frombuffer(image_data, np.uint8)

    img = cv.imdecode(nparr, cv.IMREAD_COLOR)

    height, width = img.shape[:2]
    x_center, y_center = width // 2, height // 2
    x1 = x_center - ROI_WIDTH // 2
    y1 = y_center - ROI_HEIGHT // 2
    x2 = x1 + ROI_WIDTH
    y2 = y1 + ROI_HEIGHT
    roi = img[y1:y2, x1:x2]
    center_cell = roi[CELL_HEIGHT:CELL_HEIGHT*2, CELL_WIDTH:CELL_WIDTH*2]
    buffer = 5
    center_cell = center_cell[buffer:-buffer, buffer:-buffer]
    # Blur + convert to HSV
    roi = cv.GaussianBlur(roi, (5, 5), 0)  # Light blur to smooth noise
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

    # Boost saturation and brightness
    h, s, v = cv.split(hsv_roi)
    s = np.clip(s.astype(np.float32) * 2, 0, 255).astype(np.uint8)
    v = np.clip(v.astype(np.float32) * 2, 0, 255).astype(np.uint8)
    hsv_roi = cv.merge([h, s, v])

    debug_bgr = cv.cvtColor(hsv_roi, cv.COLOR_HSV2BGR)
    cv.imwrite("debug_roi_original.jpg", roi)  # before saturation/brightness
    cv.imwrite("debug_roi.jpg", debug_bgr)
    detected_colors = [['Unknown' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS):
            cell_x1 = col * CELL_WIDTH
            cell_y1 = row * CELL_HEIGHT
            cell_x2 = (col + 1) * CELL_WIDTH
            cell_y2 = (row + 1) * CELL_HEIGHT

            cell = hsv_roi[cell_y1:cell_y2, cell_x1:cell_x2]
            # Mask out pixels with low saturation or brightness across full cell
            mask = (cell[...,1] > 80) & (cell[...,2] > 80)
            filtered = cell[mask]
            if filtered.size > 0:
                mean_hsv = np.mean(filtered, axis=0).astype(np.uint8)
            else:
                mean_hsv = np.mean(cell.reshape(-1, 3), axis=0).astype(np.uint8)

            if reference_colors:
                best_match = get_best_color_match(mean_hsv, reference_colors)
                if best_match != "Unknown":
                    color_label = best_match
                else:
                    color_label = get_color_label(mean_hsv)
            else:
                color_label = get_color_label(mean_hsv)
            detected_colors[row][col] = color_label

    return detected_colors

def get_color_label(hsv):
    for label, (lower, upper) in COLOR_RANGE.items():
        if cv.inRange(np.uint8([[hsv]]), lower, upper).any():
            return label
    return "Unknown"

def get_best_color_match(hsv, reference_colors):
    best_match = "Unknown"
    min_distance = float('inf')
    for label, ref_hsv in reference_colors.items():
        # dist = np.linalg.norm(np.array(hsv, dtype=np.float32) - np.array(ref_hsv, dtype=np.float32))
        dist = hsv_distance(hsv, ref_hsv)
        if dist < min_distance:
            min_distance = dist
            best_match = label
    return best_match

def grid_to_face_string(grid):
    result = ""
    for row in grid:
        for color in row:
            face = COLOR_TO_FACE.get(color, '?')
            result += face
    return result

def hsv_distance(hsv1, hsv2):
    # Hue is circular: 0 and 179 are adjacent
    h1, s1, v1 = hsv1
    h2, s2, v2 = hsv2
    dh = min(abs(h1 - h2), 180 - abs(h1 - h2)) / 90.0  # hue normalized to [0, 2]
    ds = abs(s1 - s2) / 255.0
    dv = abs(v1 - v2) / 255.0
    return 2.0 * dh**2 + ds**2 + dv**2  # weight hue more