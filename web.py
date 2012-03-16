import os
import flickr
from flask import Flask, jsonify, abort, make_response, request

# Reddit 6837818396
# Me 6839706724

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"links": {"photos": request.url + "photos"}})


@app.route("/photos")
def photos():
    data = flickr.api("photos.getRecent", page=request.args.get("page", 1))
    next_page = int(data["photos"]["page"]) + 1
    prev_page = max(int(data["photos"]["page"]) - 1, 1)

    return jsonify({
        "photos": data["photos"]["photo"],
        "paging": {
            "next": "{}?page={}".format(request.base_url, next_page),
            "prev": "{}?page={}".format(request.base_url, prev_page),
        }
        })

@app.route("/photos/<photo_id>", methods=["GET", "POST", "DELETE"])
def photo(photo_id):

    if request.method == "DELETE":
        flickr.api("photos.delete", photo_id=photo_id)
        return make_response("", 204)

    if request.method == "POST":
        if "tags" in request.form:
            flickr.api("photos.setTags", photo_id=photo_id,
                                         tags=request.form["tags"])

    return jsonify(flickr.api("photos.getInfo", photo_id=photo_id))

@app.route("/photos/<photo_id>/sizes")
def photo_sizes(photo_id):
    return jsonify(flickr.api("photos.getSizes", photo_id=photo_id))

@app.route("/photos/<photo_id>/favorites")
def photo_favs(photo_id):
    return jsonify(flickr.api("photos.getFavorites", photo_id=photo_id))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

