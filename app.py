from fastapi import Request, FastAPI
from img_capture import analyze_image, grid_to_face_string
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import cv2 as cv
import numpy as np

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


REFERENCE_COLORS = {}
sides = set(["Red", "Green", "Blue", "Yellow", "White", "Orange"])

ROI_WIDTH = 200
ROI_HEIGHT = 200

NUM_COLUMNS = 3
NUM_ROWS = 3

CELL_WIDTH = ROI_WIDTH // NUM_COLUMNS
CELL_HEIGHT = ROI_HEIGHT // NUM_ROWS

class ScanRequest(BaseModel):
    image: str
    label: str

@app.post("/cube-state")
async def get_cube_state(request: Request):
    try:
        data = await request.json()
        base64_image = data.get("image")
        if not base64_image:
            return {"error": "No image provided"}
        cube_string = analyze_image(base64_image, reference_colors=REFERENCE_COLORS)
        face_string = grid_to_face_string(cube_string)
        return {"cube": cube_string}
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/scan-center")
def scan_center(req: ScanRequest):
    image_data = base64.b64decode(req.image)
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)

    height, width = img.shape[:2]
    x_center, y_center = width // 2, height // 2
    x1 = x_center - ROI_WIDTH // 2
    y1 = y_center - ROI_HEIGHT // 2
    x2 = x1 + ROI_WIDTH
    y2 = y1 + ROI_HEIGHT
    roi = img[y1:y2, x1:x2]

    # Extract and post-process center cell
    center_cell = roi[CELL_HEIGHT:CELL_HEIGHT*2, CELL_WIDTH:CELL_WIDTH*2]
    buffer = 5
    center_cell = center_cell[buffer:-buffer, buffer:-buffer]

    # Blur + convert to HSV
    center_cell = cv.GaussianBlur(center_cell, (5, 5), 0)
    hsv_center = cv.cvtColor(center_cell, cv.COLOR_BGR2HSV)

    # Boost saturation + brightness
    h, s, v = cv.split(hsv_center)
    s = np.clip(s.astype(np.float32) * 2, 0, 255).astype(np.uint8)
    v = np.clip(v.astype(np.float32) * 2, 0, 255).astype(np.uint8)
    hsv_center = cv.merge([h, s, v])

    # Compute mean HSV using inner 10x10 region with masking for low saturation/brightness
    ch, cw = hsv_center.shape[:2]
    buffer = 5
    cropped = hsv_center[buffer:ch-buffer, buffer:cw-buffer]
    mask = (cropped[...,1] > 80) & (cropped[...,2] > 80)
    filtered = cropped[mask]
    if filtered.size > 0:
        mean_hsv = np.mean(filtered, axis=0).astype(np.uint8)
    else:
        mean_hsv = np.mean(cropped.reshape(-1, 3), axis=0).astype(np.uint8)

    # Convert mean_hsv back to BGR just for debugging/display
    hsv_for_bgr = np.uint8([[mean_hsv]])
    mean_bgr = cv.cvtColor(hsv_for_bgr, cv.COLOR_HSV2BGR)[0][0].tolist()

    label = req.label.capitalize()

    REFERENCE_COLORS[label] = mean_hsv.tolist()
    sides.discard(label)
    print(f"Scanned {label} → HSV: {mean_hsv.tolist()}")
    return {
        "message": f"Stored {label}",
        "mean_bgr": mean_bgr,
        "remaining_sides": list(sides)
    }


# @app.route('/capture-and-solve', methods=['GET'])
# def update_cube():
#     try:
#         cube_string = run_capture()
#         print("Captured cube string:", cube_string)
#         if len(cube_string) != 54:
#             raise ValueError(f"Incomplete cube string: expected 54 characters, got {len(cube_string)}")
#         solution = solve(cube_string)
#         print("Solution:", solution)
#         return jsonify({'cube': cube_string, 'solution': solution})
#     except Exception as e:
#         print("Error in /capture-and-solve:", e)
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host="localhost")