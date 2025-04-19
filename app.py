from fastapi import Request, FastAPI
from img_capture import analyze_image, grid_to_face_string, scan_center_cell
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    mean_hsv, mean_bgr = scan_center_cell(req.image)
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