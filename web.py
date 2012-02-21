import os
import requests
import json
from flask import Flask, jsonify

app = Flask(__name__)

FLICKR_BASE = "http://api.flickr.com/services/rest/"

def url(path):
    return "https://quivr.herokuapp.com" + path

@app.route("/")
def api_root():
    print os.environ
    return jsonify({
        "links": [
            "https://quivr.herokuapp.com/photos",
            "https://quivr.herokuapp.com/panadas",
            ]
        })

@app.route("/photos")
def photos():
    return jsonify({
        "links": [
            "https://quivr.herokuapp.com/photos",
            ]
        })

def get_pandas():
    resp = requests.get(FLICKR_BASE, params={
        "method": "flickr.panda.getList",
        "api_key": os.environ["FLICKR_KEY"],
        "format": "json",
        "nojsoncallback": "1",
        })

    pandas = json.loads(resp.content)["pandas"]["panda"]

    return [get_panda(p["_content"]) for p in pandas]

def get_panda(name):
    return {
        "name": name ,
        "url": url("/pandas/{}".format(name.replace(" ", "+"))),
        }

@app.route("/pandas/<name>/photos")
def panda_photo(name):
    resp = requests.get(FLICKR_BASE, params={
        "method": "flickr.panda.getPhotos",
        "api_key": os.environ["FLICKR_KEY"],
        "format": "json",
        "nojsoncallback": "1",
        "panda_name": name.replace
        })

    return resp.content

@app.route("/pandas/<name>")
def panda(name):
    return jsonify({
        "name": name ,
        "url": url("/pandas/{}".format(name.replace(" ", "+"))),
        "links": [
            url("/pandas/{}/photos".format(name.replace(" ", "+"))),
            ]
        })

@app.route("/pandas")
def pandas():
    return jsonify({
        "items": get_pandas(),
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

