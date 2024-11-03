from flask import Flask, jsonify
from flask_cors import CORS
from processing.main import make_tabs

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route("/api/songs/<path:url>", methods=['GET'])
def songs(url):
    # return jsonify (

    # )
  tabs = make_tabs(url)

  return jsonify (
    {
      "tabs": tabs,
      "maxTime": 42,
      "len": len(url),
      "url": url,
    }
  )

if __name__ == "__main__":
  app.run(debug=True, port=60000)
