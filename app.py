from flask import Flask, jsonify
from flask_cors import CORS
from video_capture import run_capture
from twophase import solve

app = Flask(__name__)
CORS(app)

@app.route('/capture-and-solve', methods=['GET'])
def capture_and_solve():
    try:
        cube_string = run_capture()
        solution = solve(cube_string)
        return jsonify({'cube': cube_string, 'solution': solution})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
