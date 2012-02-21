import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)
auth = (os.environ["FLICKR_KEY"], os.environ["FLICKR_SECRET"]) 

@app.route("/")
def api_root():
    print os.environ
    return jsonify({
        "links": [
            "/photos",
            ]
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

