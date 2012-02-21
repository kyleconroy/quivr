import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)
auth = (os.environ["FLICKR_KEY"], os.environ["FLICKR_SECRET"]) 


@app.route("/")
def api_root(in_url):
    return jsonify({
        "links": [
            "/photos",
            ]
        })

@app.route("/photos")
def index():
    return render_template("index.html",
                source="http://responsivewebdesign.com/robot/",
                text="http://responsivewebdesign.com/robot/")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

