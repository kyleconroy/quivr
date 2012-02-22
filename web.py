import os
import requests
import json
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

FLICKR_BASE = "http://api.flickr.com/services/rest/"

def url(path):
    return request.url_root + path

def flickr_api(method, **kwargs):
    kwargs.update({
        "method": "flickr.{}".format(method),
        "api_key": os.environ["FLICKR_KEY"],
        "format": "json",
        "nojsoncallback": "1",
        })

    resp = requests.get(FLICKR_BASE, params=kwargs)
    return json.loads(resp.content)

def not_found(message="Resource Not Found"):
    return make_response(json.dumps({
        "message": message,
        "url": request.url,
        }), 404)

def bad_request(message="Bad Request"):
    return make_response(json.dumps({
        "message": message,
        "url": request.url,
        }), 400)


def photo(data):
    data["url"] = url("photos/{}".format(data["id"]))

    if "urls" in data:
        print data
        data["links"] = {
            "favorites": url("photos/{}/favorites".format(data["id"])),
            "sizes": url("photos/{}/sizes".format(data["id"])),
            "photopage": data["urls"]["url"][0]["_content"],
        }
        del data["urls"]

    return data


@app.route("/")
def api_root():
    print os.environ
    return jsonify({
        "links": {
            "photos": url("photos"),
            },
        })


@app.route("/photos/<photo_id>/favorites")
def photo_favorites(photo_id):
    data = flickr_api("photos.getFavorites", photo_id=photo_id)

    print data

    if data["stat"] == "fail" and data["code"] == 1:
        return not_found("The requested photo could not be found")

    return jsonify({
        "items": data["photo"]["person"],
        })



@app.route("/photos/<photo_id>/sizes")
def photo_sizes(photo_id):
    data = flickr_api("photos.getSizes", photo_id=photo_id)

    if data["stat"] == "fail" and data["code"] == 1:
        return not_found("The requested photo could not be found")

    return jsonify({
        "items": data["sizes"]["size"],
        })


@app.route("/photos/<photo_id>")
def photo_resource(photo_id):
    data = flickr_api("photos.getInfo", photo_id=photo_id)

    if data["stat"] == "fail" and data["code"] == 1:
        return not_found("The requested photo could not be found")

    return jsonify(photo(data["photo"]))


@app.route("/photos")
def photos_resource():
    data = flickr_api("photos.search", **request.args)

    if data["stat"] == "fail" and data["code"] == 3:
        return bad_request("Flickr requires search parameters")

    resp = {
        "items": [photo(d) for d in data["photos"]["photo"]],
        "url": request.url,
        "links": {
            "next": "",
            "previous": "",
            }
        }

    return jsonify(resp)

@app.errorhandler(404)
def no_resource(e):
    return not_found()



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

