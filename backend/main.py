from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route("/api/songs", methods=['GET'])
def songs():
  return jsonify (
    {
      "tabs": [
        {"string": 0, "time": 5, "fret": 3},
        {"string": 0, "time": 10, "fret": 2},
        {"string": 0, "time": 20, "fret": 4},
        {"string": 0, "time": 30, "fret": 5},
        {"string": 1, "time": 8, "fret": 1},
        {"string": 1, "time": 15, "fret": 3},
        {"string": 1, "time": 24, "fret": 2},
        {"string": 1, "time": 32, "fret": 4},
        {"string": 1, "time": 35, "fret": 5},
        {"string": 2, "time": 7, "fret": 0},
        {"string": 2, "time": 18, "fret": 2},
        {"string": 2, "time": 25, "fret": 1},
        {"string": 2, "time": 28, "fret": 3},
        {"string": 2, "time": 35, "fret": 4},
        {"string": 3, "time": 5, "fret": 3},
        {"string": 3, "time": 12, "fret": 1},
        {"string": 3, "time": 15, "fret": 2},
        {"string": 3, "time": 23, "fret": 5},
        {"string": 3, "time": 29, "fret": 4},
        {"string": 4, "time": 0, "fret": 1},
        {"string": 4, "time": 11, "fret": 0},
        {"string": 4, "time": 16, "fret": 3},
        {"string": 4, "time": 24, "fret": 2},
        {"string": 4, "time": 27, "fret": 5},
        {"string": 5, "time": 6, "fret": 0},
        {"string": 5, "time": 17, "fret": 2},
        {"string": 5, "time": 26, "fret": 3},
        {"string": 5, "time": 31, "fret": 1},
        {"string": 5, "time": 36, "fret": 4},
        {"string": 5, "time": 42, "fret": 5}
      ],
      "maxTime": 78,
    }
  )

if __name__ == "__main__":
  app.run(debug=True, port=60000)