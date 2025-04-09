from typing import Union
from fastapi import FastAPI
from video_capture import run_capture
from twophase import solve

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



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